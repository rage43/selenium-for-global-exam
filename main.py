from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import os 

#configuration
global_exam_mail=""
global_exam_password=""

#begin navigation

driver = webdriver.Firefox()
driver.get("https://auth.global-exam.com/login")
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

login_button=driver.find_element("xpath","/html/body/div[1]/main/div/div/div/div/div/form/div[3]/button")
login_button.click()
sleep(5)
driver.get("https://business.global-exam.com/stats")
sleep(5)
for i in range(16):
    driver.get("https://business.global-exam.com/industry/1933/content/6817")
    sleep(5)

    for url_to_next in (
                "/html/body/div[1]/div/main/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/button[2]",
                "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div[2]/button"
                ):
        try:
            driver.find_element("xpath",url_to_next).click()
        except:
            print("error")
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
