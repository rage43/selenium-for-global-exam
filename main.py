from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import os 
import sys

__WORKDIR__= os.path.dirname(os.path.abspath(sys.argv[0]))



#configuration
global_exam_mail=""
global_exam_password=""


# Start browsermob proxy
browsermobproxy_location =os.path.join(__WORKDIR__,"browsermob-proxy-2.1.4/bin/browsermob-proxy")

server = Server(browsermobproxy_location)
server.start()
print("proxy server started....")
exit(1)
proxy = server.create_proxy()

### OPTIONS ###
url="https://auth.global-exam.com/login"
firefox_driver_location = os.path.join(__WORKDIR__,"geckodriver")
print(firefox_driver_location)
exit(1)
options = webdriver.Firefox()
driver.get("https://auth.global-exam.com/login")
options = webdriver.ChromeOptions()
options.binary_location = chrome_location
# Setup proxy to point to our browsermob so that it can track requests
options.add_argument('--proxy-server=%s' % proxy.proxy)
driver = webdriver.Chrome(chromedriver_location, chrome_options=options)
print(driver.title)
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
