from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import json

dados_col =  { 1:"Nome_Urna",
               2:"Nome Completo", 	
               3:"Numero",
               4:"Situacao" ,
               5:"Sigla" ,
               6:"Partido/Coligacao",
               7: "Releicao"}

dados_vereadores_Teresina = {"Quantidade_Vereadores":"",
                             "Cidade":"Teresina", 	
                             "Vereadores":[]}

driver = webdriver.Chrome('c:/Users/samue/Desktop/Custo_piaui/chromedriver')
driver.set_page_load_timeout(100)

data = []
with open('nums.json', 'r') as f:
    data = json.load(f)

print(len(data))

#Request Pagina inicial
driver.get("http://divulgacandcontas.tse.jus.br/divulga/#/municipios/2020/2030402020/12190/candidatos")

delay = 60 # seconds
try:
    print("Loading....")
    #Esperando o site sair da tela de carregamento
    myElem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'dvg-link-list-mobile')))
    print ("Page is ready!")

    #Selecioando a lista de Vereadores
    seletor = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/section[3]/div/div/div/table/tbody/tr/td[1]/select/option[text()='Vereador']")
    seletor.click()

    time.sleep(30)
    
    #Quantidade de linha da  lista de Vereadores
    num_rows = len (driver.find_elements_by_xpath("/html/body/div[2]/div[1]/div/div/section[3]/div/div/table[1]/tbody/tr"))
    dados_vereadores_Teresina["Quantidade_Vereadores"] = num_rows
    print("Num_rows",num_rows)
    #Quantidade de colunas da  lista de Vereadores
    num_cols = len (driver.find_elements_by_xpath("/html/body/div[2]/div[1]/div/div/section[3]/div/div/table[1]/tbody/tr[1]/td"))

   
    before_XPath = "/html/body/div[2]/div[1]/div/div/section[3]/div/div/table[1]/tbody/tr["
    aftertd_XPath = "]/td["
    aftertr_XPath = "]"

    #Percorrendo a tabela
    for t_row in range(1, (num_rows+1)):
        dados_vereador_Teresina = { "Nome_Urna":"", "Nome Completo":"", "Numero":"", "Situacao":"" ,"Sigla":"" ,"Partido/Coligacao":"","Releicao":"","Imagem":""}
        print("Get Candidato:",t_row)
        for t_column in range(1, (num_cols+ 1 )):
            #print("\t\t collum:",t_column)
            FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
            cell = driver.find_element_by_xpath(FinalXPath)
            dados_vereador_Teresina[dados_col[t_column]] = cell.text           
        
        if dados_vereador_Teresina['Numero'] in data['Numeros']:
            continue

        ClickXPath = "/html/body/div[2]/div[1]/div/div/section[3]/div/div/table[1]/tbody/tr["+str(t_row)+"]/td[1]/a"

        cell_a = driver.find_element_by_xpath(ClickXPath)
        #Entrando no perfil do candidato
        cell_a.click()

        time.sleep(6)

        #Pegando o src da imagem
        img = driver.find_element_by_class_name("img-thumbnail")
        img_path = img.get_attribute('src')
        dados_vereador_Teresina["Imagem"] = img_path
        
        #Voltando a lista de candidatos
        driver.back()
        time.sleep(5)
        myElem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, FinalXPath)))
        dados_vereadores_Teresina["Vereadores"].append(dados_vereador_Teresina)

except Exception as e :
    print("ERRO:",e)

#Salvando Dados no formato json
with open('result_20_10.json', 'w',encoding='UTF-8') as fp:
    json.dump(dados_vereadores_Teresina, fp)

#Fianlizando o script e fechando o navegador
driver.close()