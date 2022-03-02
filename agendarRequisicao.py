import time
from scraping import Scraping
from sendEmail import EmailController
from connection_db import Conector
from datetime import datetime

def update_movimentacoes():
        processos_atualizados = ""
        conn = Conector().connect()
        scrap = Scraping()

        try:
            query =  "SELECT * FROM processos  WHERE arquivada = 0"
            result_processos = conn.execute(query)
    
            for row in result_processos: 
                d = {}

                for column, value in row.items():
                    d.update({column: value})

                count,movs,atualizacao,atualizacao_tag,data,duracao = scrap.get_movimentacoes(row['protocolo'],row['data_atualizacao'],row['data_Entrada'])

                atualizacao_horario =  datetime.now().strftime('%d/%m/%Y - %H:%M')
                query_update_duracao = "UPDATE processos SET duracao = '{}',atualizacao = '{}',atualizacao_tag= '{}', data_atualizacao ='{}', log_atualizacao = '{}' WHERE protocolo = '{}'".format(duracao,atualizacao,atualizacao_tag,data,atualizacao_horario,row['protocolo'] )
                result_update_duracao = conn.execute(query_update_duracao) 
                result_update_duracao.close()
          
                if count == 0:
                    continue

                processos_atualizados += row['protocolo']+", "

                query = "INSERT INTO movimentacoes (movimentacoes.data,descricao,protocolo) VALUES "
                for mov in movs:
                    query += "('{}','{}','{}'),".format(mov['data'],mov['descricao'],row['protocolo'])
                try:
                    result_ = conn.execute(query[0:-1]) 
                    result_.close() 
                except Exception as e:
                    print("Tentando de novo")  
                    time.sleep(200)  

                
            if  processos_atualizados != "":
                e = EmailController()
                e.send_email(processos_atualizados)   

            conn.close()                  
                 
        except Exception as e:
            print(e)
            arquivo = open("log_falhas.txt", "a")
            arquivo.writelines(str(e) + " -- " + str(datetime.now())  + "\n")
            arquivo.close()
            return  ""
       
        return ''


while True:
    print("Update - ", datetime.now())
    update_movimentacoes()
    print("Sleep")
    time.sleep( 7200 )