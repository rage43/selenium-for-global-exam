
from selenium import webdriver
import yaml
import psutil
import time
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
chrome_options.add_argument('--headless') 
driver = webdriver.Chrome(options=chrome_options)

# Start capturing network requests
proxy.new_har("globalexam",options={'captureContent': True})
driver.get(global_exam_url)
time.sleep(4)


# Print all URLs that were requested
myfunction.get_page_data(proxy)
myfunction.quit(server,driver)






exit(1)
driver.quit()
proxy.qui()
# Setup proxy to point to our browsermob so that it can track requests
options.add_argument('--proxy-server=%s' % proxy.proxy)
#driver = webdriver.Chrome(chromedriver_location, optifoptions)
print(driver.title)
exit(1)
assert "GlobalExam" in driver.title
elem = driver.find_element(By.NAME, "email")
elem.clear()
elem.send_keys(global_exam_mail)
sleep(2)
elem= driver.find_element(By.NAME, "password")
elem.clear()
elem.send_keys(global_exam_password)
sleep(2)
#authentification
login_button=driver.find_element("xpath","/html/body/div[1]/main/div/div/div/div/div/form/div[3]/button")
login_button.click()
sleep(5)
driver.get("https://business.global-exam.com/stats")
sleep(5)

#debut traitements exercices
for i in range(16):
    driver.get("https://business.global-exam.com/industry/1933/content/6817")
    sleep(5)

    for url_to_next in (
                "/html/body/div[1]/div/main/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/button[2]",
                "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div[2]/button"
                ):
        try:
            driver.find_element("xpath",url_to_next).click()
            timings = driver.execute_script("return window.performance.getEntries();")
        except:
            print("Contenue cliquable non trouvé")
            pass
        sleep(5)

    #continue exercise

    sleep(15)
    terminer=False
    cmpt=1
    while terminer == False:
        try:
            driver.find_element(By.XPATH, '//button[text()="Terminer"]').click()
            terminer=True
            print("terminé")
            sleep(2)
            driver.get("https://business.global-exam.com/stats")
            sleep(10)

        except:
            terminer=False
        
        try:
            driver.find_element("xpath","/html/body/div[1]/div/div[2]/div[2]/button").click()
        except:
            try:
                driver.find_element("xpath","/html/body/div[1]/div[2]/div[2]/button").click()
            except:
                pass
        if cmpt % 2==0:
            sleep(3)
        else:
            sleep(50)
        cmpt+=1
        


try:
    os.remove("geckodriver.log")
except:
    pass
driver.close()
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
