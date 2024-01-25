################ Requirements ######################

# You have to install the 'assets/pytesseract' folder in the directory where you are running the code - you can get this from the v3.0 release on my gihtub.

# The screenshots of the results would also be stored in the same directory

# pip install selenium
# pip install chromedriver_py
# pip install pytesseract
# pip install opencv-python

#####################################################


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from chromedriver_py import binary_path 

# Download the application available on GitHub to experience much faster speeds.

import pytesseract as ptes
import cv2
import multiprocessing
from multiprocessing import freeze_support
import sys
import os

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_argument("start-maximized")
# options.add_argument('headless')
# uncomment above line if you don't want chrome tabs to open up everytime , or for better perfoamance 
svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc,options=options)

###################### Required Changes #######################################

# Only uncomment that year whose result you want to find 

# 2020 
# link = "https://ntaresults.nic.in/resultservices/JEEMainP1-Apr20-auth"
# title = "NTA Result"
# accepted_alert = "Invalid Application Number/Date of Birth."

# 2021 
# link = "https://ntaresults.nic.in/resultservices/JEEMain2021auth"
# title = "JEE(Main): View Result"
# accepted_alert = "Invalid Exam Session/Application Number/Date of Birth."

# 2022 
# link = "https://ntaresults.nic.in/resultservices/JEEMAINauth22s2p1"
# title = "NTA Result"
# accepted_alert = "Invalid Application Number/Date of Birth."

# 2023
# link = "https://ntaresults.nic.in/resultservices/JEEMAINauth23s2p1"
# title = "NTA Result"
# accepted_alert = "Invalid Application Number/Date of Birth."

# User details - edit as per your needs

application_no = 000000000000
all_years = [2003,2002,2004,2001,2005,2000,2006,1999,1998]

# This is the sequence of years of birth, change it according to you
# All birth years will be checked in the order from left to right

#################################################################################

def regisno(inp):
    driver.get(link)
    while driver.title != title:
        driver.switch_to.new_window('window')
        driver.get(link)
        if len(driver.window_handles)>3:
            closeall()
    regno = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtRegNo")
    regno.send_keys(str(inp))


def dob(in_year,in_month,in_day):
    if len(str(in_day))==1:
        in_day='0'+str(in_day)
    if len(str(in_month))==1:
        in_month='0'+str(in_month)

    year_id = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlyear")
    month_id = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlmonth")
    day_id = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlday")

    yearselect = Select(year_id)
    monthselect = Select(month_id)
    dayselect = Select(day_id)

    yearselect.select_by_value(str(in_year))
    monthselect.select_by_value(str(in_month))
    dayselect.select_by_value(str(in_day))

# Download the application available on GitHub to experience much faster speeds.

def screenshot():
    try:
        os.remove('ss.png')
    except:
        pass
    finally:
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_captchaimg').screenshot('ss.png')

def read_captcha():
    ptes.pytesseract.tesseract_cmd = r'pytesseract/tesseract.exe'
    try:
        img = cv2.imread('ss.png', 0)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        imagetext = ptes.image_to_string(img)
    except TypeError:
        imagetext="a b"
    l = imagetext.split()
    s = ""
    for i in range(len(l)):
        s += l[i]
    if len(s)>0:
        return s
    else:
        return "a"

def fill_captcha_and_submit(captcha):
    captchainput = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_Secpin")
    captchainput.send_keys(captcha)
    submit = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_Submit1")
    submit.click()

def check_for_result():
    try:
        WebDriverWait(driver, 7).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        if alert_text == accepted_alert:
            alert.accept()
            return True
        alert.accept()
    except TimeoutException:
        try:
            name = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_cname")
        except:
            print("error occured")
            closeall()
        else:
            print("Result Success")
            name_text = name.text
            save_result(name_text)
            closeall()
            sys.exit()

# Download the application available on GitHub to experience much faster speeds.

def save_result(name_text):     
    # change the zoom size to get the perfect screenshot, for my screen's size 70% was best.
    driver.execute_script("document.body.style.zoom='70%'")
    file_name=name_text+'.png'
    result=driver.find_element(By.TAG_NAME,"body").screenshot(file_name)

def closeall():
    os.system("TASKKILL /F /IM chrome.exe")
    os.system("TASKKILL /F /IM chromedriver.exe")
    driver.quit()
    sys.exit()


def mainfunc(val,regno,allmonths,allyears):        
    regisno(regno)
    for i in range(len(allyears)):
        if (allyears[i]%100==0 and allyears[i]%400==0) or (allyears[i]%100!=0 and allyears[i]%4==0):
            allmonths[1]=29
        else:
            allmonths[1]=28

        for index in range(val+1,val-1,-1):
            for k in range(allmonths[index]):
                dob(allyears[i], index+1 , k + 1)
                while True:
                    screenshot()
                    captcha = read_captcha()
                    fill_captcha_and_submit(captcha)
                    if check_for_result():
                        break
            print(index+1,"/",allyears[i],"  checked ")
    else:
        driver.quit()

if __name__=="__main__":

    freeze_support()
    rno=application_no
    all_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for j in range(6):
        multiprocessing.Process(target=mainfunc, args=(2 * j,str(rno),all_months,all_years)).start()

# Download the application available on GitHub to experience much faster speeds.
