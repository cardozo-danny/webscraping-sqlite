import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import base
from models.db_models import Produto
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.common.exceptions import *
import os
import time
import itertools

def Iniciar():
    conexao = configurar_banco_de_dados()
    buscar_produtos(conexao)

def configurar_banco_de_dados():
#Para criar um banco de dados SQlite3
    engine = create_engine('sqlite:///produtos.db', echo=True)
    base.metadata.drop_all(bind=engine) 
    base.metadata.create_all(bind=engine) 
    Conexao = sessionmaker(bind=engine)
    conexao = Conexao()

    return conexao

def buscar_produtos(conexao):
    
    chrome_options = Options()
    chrome_options.add_argument('--lang=pt-BR')
    driver = webdriver.Chrome(executable_path=r'./chromedriver.exe', options=chrome_options)
    driver.get(f'https://cursoautomacao.netlify.app/produtos1.html')
    wait = WebDriverWait(
        driver,
        10,
        1,
        ignored_exceptions=[NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException]
    )

    encontrar_valores(driver, wait, conexao)
    
        

def encontrar_valores(driver, wait, conexao):
    try:
                    
        while True:

            nome = wait.until(CondicaoExperada.visibility_of_all_elements_located((By.XPATH,"//h5[@class='name']")))
            descricao = wait.until(CondicaoExperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='description']")))
            preco = wait.until(CondicaoExperada.visibility_of_all_elements_located((By.XPATH,"//span[starts-with(text(), '$')]")))
            

            for a, b, c in itertools.zip_longest(nome, descricao, preco):
                adicionar_novo_produto(a.text, b.text, c.text, conexao)
            proxima_pagina = wait.until(CondicaoExperada.element_to_be_clickable((By.ID, 'proxima_pagina')))
            proxima_pagina.click()
            time.sleep(2)
            encontrar_valores(driver,wait,conexao)
                                            
    except Exception as erro:
            
        print('Não há mais valores para serem extraídos')

        driver.quit()
            
def adicionar_novo_produto(nome, descricao, preco, conexao):
    novo_produto = Produto()
    novo_produto.nome = nome
    novo_produto.descricao = descricao
    novo_produto.preco = preco
    conexao.add(novo_produto)
    conexao.commit()

    

if __name__ == "__main__":
    Iniciar()
            
        
            

            
                    
        
  
