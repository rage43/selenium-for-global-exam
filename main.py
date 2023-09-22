
from selenium import webdriver
import yaml
import psutil
import re
import time
import json
from browsermobproxy import Server
import colorama 
from termcolor import colored
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import os 
import sys
import func as myfunction

#--------

colorama.init()
__WORKDIR__= os.path.dirname(os.path.abspath(sys.argv[0]))


#load config from yaml
with open("conf.yaml","r") as file:
    config= yaml.safe_load(file)


#set parmas and options for global exam
global_exam_url="https://auth.global-exam.com/login"
drvername= "chromedriver" if os.name == 'posix' else chromedriver 
chrome_driver_location = os.path.join(__WORKDIR__,drvername)
browsermobproxy_location =os.path.join(__WORKDIR__,"browsermob-proxy-2.1.4/bin/browsermob-proxy")


#check if  proxy process exist
for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == "browsermob-proxy":
        print("Process found ")
        proc.kill()
        print("Process killed ")

# Start proxy
server = Server(browsermobproxy_location)
server.start()
time.sleep(1)
proxy = server.create_proxy()

# Setup Selenium to use BrowserMob Proxy
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))

# To ignore certificate errors
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
#chrome_options.add_argument('--headless') 
driver = webdriver.Chrome(options=chrome_options)

# Start capturing network requests
proxy.new_har("globalexam",options={'captureContent': True})
driver.get(global_exam_url)

#declaration de variables
tour_de_boucle=0


#attendre le chargement de la page 
while "GlobalExam" not in driver.title:
    print("En attente de la page de connexion GlobalExxam....")
    tour_de_boucle+=1
    myfunction.timeout_selenium(server,driver,tour_de_boucle)


#Saisie des infos de connexion

global_exam_mail=config.get("global_exam_mail")
global_exam_password=config.get("global_exam_pass")
print(global_exam_mail)
if global_exam_mail is None or global_exam_password is None:
    myfunction.msg_red("Le mail ou le mot de passe doivent etres renseignés")
    myfunction.quit(server,driver)


#saisie du mail
elem=None
tour_de_boucle=0
while elem == None:
    elem = driver.find_element(By.NAME, "email")
    tour_de_boucle+=1
    myfunction.timeout_selenium(server,driver,tour_de_boucle)
elem.clear()
elem.send_keys(global_exam_mail)

#saisie du mot de passe
elem=None
tour_de_boucle=0
while elem == None:
    elem= driver.find_element(By.NAME, "password")
    tour_de_boucle+=1
    myfunction.timeout_selenium(server,driver,tour_de_boucle)
elem.clear()
elem.send_keys(global_exam_password)

#click sur authentification
elem=False
tour_de_boucle=0
while elem == False:
    try:
        #driver.find_element("xpath","/html/body/div[1]/main/div/div/div/div/div/form/div[3]/button").click()
        driver.find_element(By.XPATH, '//button[text()=" Se connecter "]')
        elem=True
    except:
        tour_de_boucle+=1
        myfunction.timeout_selenium(server,driver,tour_de_boucle)

print('#'*100)
print("Authentifié à GlobalExam")

continuer_xpath="Continuer"

suivant_xpath="Suivant"


modules = ("https://business.global-exam.com/industry/1933/content","https://business.global-exam.com/industry/2949/content")

#debut traitements exercices
#modlule
for module in modules:
    module_url=module
    liste_exercice_a_debuter=True
    #page d'exercices
    driver.get(module_url)
    #element de module  #and next_element_of_module==True
    #Avancer sur les elements de module
    next_element_of_module=True
    while liste_exercice_a_debuter== True :
        
        liste_exercice_a_debuter= myfunction.click_on_button(driver,continuer_xpath)

        #si exercice de module dispo
        exercice_terminer=None
        while exercice_terminer!=True:
            exercice_suivant=myfunction.click_on_button(driver,suivant_xpath,"suivant")
            if str(driver.current_url()).endswith("result"):
                exercice_terminer=True
                driver.get(module_url)

        if liste_exercice_a_debuter==None:
            current_url = driver.current_url
            numbers = re.findall(r'\d+', current_url.split('\\')[-1])[0]
            next_url=current_url.replace(numbers,int(numbers)+1)
            driver.get(next_url)
            next_element_of_module=myfunction.click_on_button(driver,continuer_xpath)
        if myfunction.click_on_button(driver,"Me certifier")==True:
            exercice_dispo =None 
            next_element_of_module=None 

'''



            if exercice_dispo==True:
                exercice_suivant=None
                while exercice_suivant  == True:
                    myfunction.random_wait()

                    
                    try:
                        driver.find_element(By.XPATH, '//button[text()="Terminer"]').click()
                        driver.get(module_url)
                    except:
                        exercice_suivant=None

                print("exo termine ?")
                print(exercice_terminer)

            #Retourn à la liste des exos
            driver.get(module_url)
     ''' 

myfunction.msg_green("TERMINER !!!!")
    
