
from selenium import webdriver
from browsermobproxy import Server
import colorama
from termcolor import colored
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
from browsermobproxy.server import Client

def quit(server:Server,driver:webdriver):
    driver.quit()
    server.stop()
    exit(1)


def get_page_data(page_name:str,proxy:Client):
    entries = proxy.har['log']["entries"]

    for entry in entries:
        url:str = str(entry['request']['url'])
        if url.endswith(page_name) :
            response_content = entry['response']['content'].get('text', None)
            if response_content:
                return response_content
            else:
                return None
                
 


def msg_green(msg:str):
   
    print(colored(msg,'green'))

def msg_red(msg:str):
   
    print(colored(msg,'red'))


def timeout_selenium(server:Server,driver:webdriver,tours_de_boucle=0,nb_tours_accepte=3):
    if tours_de_boucle >= nb_tours_accepte:
        print(colored('Impossible de continuer delais d\'attente trop long','red'))
        driver.quit()
        server.stop()
        exit(1)
    else:
        time.sleep(2)



def click_on_button(driver:webdriver,path_name,n=None):
    cmpt=0
    elem=False
    while elem==False:
        try:
            driver.find_element(By.XPATH, f'//button[text()="{path_name}"]')
        except:
            if elem == False and cmpt>5:
                return None
            time.sleep(2)
        cmpt+=1
    return elem

def random_wait():
    i=random.randint(5, 10)
    print(f"attente de {i} seconde avant de continuer")
    time.sleep(i)


if __name__=='__main__':
    a={'n':1}
    print(type(a))
    exit(1)