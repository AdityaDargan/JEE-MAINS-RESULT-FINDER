from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pytesseract as ptes
import cv2
import multiprocessing
import sys
import os
import shutil
import time

# initializing code

c = webdriver.ChromeOptions()
c.add_argument("--incognito")

#enable or disable the headless command to control the windows of brave browser
c.add_argument('headless')          

brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"       
# path of brave.exe (may be different for your computer)

c.binary_location = brave_path

path = "D:/chrome driver/chromedriver.exe"      
# path of chromedriver.exe (may be different for your computer)
driver = webdriver.Chrome(path, options=c)

destination="C:/Users/adity/OneDrive/Desktop/Python/projects" # file destination folder
source="C:/Users/adity/OneDrive/Desktop/Python/"   # path where files are saved by default
start=time.time()
def errorsolve():
    driver.get("https://www.google.co.in/")
    driver.quit()

def regisno(inp):

    driver.get("https://ntaresults.nic.in/resultservices/JEEMain2021auth")
    while driver.title != "JEE(Main): View Result":
        driver.switch_to.new_window('window')
        driver.get("https://ntaresults.nic.in/resultservices/JEEMain2021auth")
        if len(driver.window_handles)>4:
            closeall()
    regno = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtRegNo")
    regno.send_keys(str(inp))

def dob(in_year,in_month,in_day):
    if len(str(in_day))==1:
        in_day='0'+str(in_day)
    if len(str(in_month))==1:
        in_month='0'+str(in_month)

    year_id = driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlyear")
    month_id = driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlmonth")
    day_id = driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlday")

    yearselect = Select(year_id)
    monthselect = Select(month_id)
    dayselect = Select(day_id)

    yearselect.select_by_value(str(in_year))
    monthselect.select_by_value(str(in_month))
    dayselect.select_by_value(str(in_day))

def screenshot():
    try:
        os.remove('ss.png')
    except:
        pass
    finally:
        driver.find_element_by_id('ctl00_ContentPlaceHolder1_captchaimg').screenshot('ss.png')

def read_captcha():
    ptes.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
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
    captchainput = driver.find_element_by_id("ctl00_ContentPlaceHolder1_Secpin")
    captchainput.send_keys(captcha)
    submit = driver.find_element_by_id("ctl00_ContentPlaceHolder1_Submit1")
    submit.click()

def check_for_result():
    try:
        WebDriverWait(driver, 7).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        if alert_text == "Invalid Exam Session/Application Number/Date of Birth.":
            alert.accept()
            return True
        alert.accept()
    except TimeoutException:
        try:
            name = driver.find_element_by_id("ctl00_ContentPlaceHolder1_cname")
        except:
            print("error occured")
            closeall()
        else:
            print("Result Success")
            name_text = name.text
            save_result(name_text)
            closeall()
            sys.exit()

def save_result(name_text):
    driver.execute_script("document.body.style.zoom='70%'")
    file_name=name_text+'.png'
    result=driver.find_element_by_tag_name("body").screenshot(file_name)
    print(file_name)
    src=source+file_name
    print(source)
    shutil.move(src,destination)

def closeall():
    print((time.time() - start)/60, " = time taken to find the result in minutes ")
    os.system("TASKKILL /F /IM brave.exe")
    os.system("TASKKILL /F /IM chromedriver.exe")

    sys.exit()

def mainfunc(val,regno,allmonths,allyears):
    regisno(regno)
    for i in range(len(allyears)):
        if allyears[i]==2004 or allyears[i]==2000:
            allmonths[1]=29
        else:
            allmonths[1]=28

        for index in range(val,val+2):
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
    
    # Here you have to write the application number of the candidate .
    rno="210310326520"
    

    all_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    all_years = [2003,2002,2001,2004,2000,2005,1999,2006,1998]
    # this is the sequence of checking various year ,can be changed as per needs
    

    #running the code in 6 threads simultaneously 
    multiprocessing.Process(target=errorsolve, args=()).start()
    for j in range(6):
        multiprocessing.Process(target=mainfunc, args=(2 * j,str(rno),all_months,all_years)).start()