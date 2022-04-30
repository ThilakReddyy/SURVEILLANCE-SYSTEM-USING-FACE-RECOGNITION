from re import S
import requests
import os
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
def time_in_range(start, end, current):
    return start <= current <= end

def getTimeTable(k):
    url = urlmain+"ajax/Academics_TimeTableReport,App_Web_timetablereport.aspx.a2a1b31c.ashx?_method=getTimeTableReport&_session=r"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Accept': '*/*',
    'Cookie': k
    }
    response = requests.request("POST", url, headers=headers)
    soup=BeautifulSoup(response.content,"html.parser")
    soup=soup.find_all("table")[3].find_all("tr")
    current=datetime.datetime.now().time()
    p=datetime.datetime.today().weekday()
    if(time_in_range(datetime.time(9, 15, 0), datetime.time(10, 15, 0), current)):
        soup=soup[p+1].find_all("td")
        print(soup[1].contents[0])
    elif(time_in_range(datetime.time(10, 15, 0), datetime.time(11, 15, 0), current)):
        soup=soup[p+1].find_all("td")
        print(soup[2].contents[0])
    elif(time_in_range(datetime.time(11, 15, 0), datetime.time(12, 15, 0), current)):    
        soup=soup[p+1].find_all("td")
        print(soup[3].contents[0])
    elif(time_in_range(datetime.time(12, 15, 0), datetime.time(13, 0, 0), current)):     
        soup=soup[p+1].find_all("td")
        if(soup[4].contents[0]==""):
            print("Lunch")
        else:
            print(soup[4].contents[0])
    elif(time_in_range(datetime.time(13, 0, 0), datetime.time(14, 0, 0), current)):
        soup=soup[p+1].find_all("td")
        print(soup[5].contents[0])
    elif(time_in_range(datetime.time(14, 0, 0), datetime.time(15, 0, 0), current)):
        soup=soup[p+1].find_all("td")
        print(soup[6].contents[0])
    elif(time_in_range(datetime.time(15, 0, 0), datetime.time(16, 0, 0), current)):
        soup=soup[p+1].find_all("td")
        print(soup[7].contents[0])
    else:
        print("No")
        
def getpercentage(roll,k):
    url = urlmain+"ajax/StudentProfile,App_Web_studentprofile.aspx.a2a1b31c.ashx?_method=ShowStudentProfileNew&_session=rw"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Accept': '*/*',
    'Cookie': k
    }
    payload = "RollNo="+roll+"\r\nisImageDisplay=false"
    response = requests.request("POST", url, headers=headers, data=payload)
    soup=BeautifulSoup(response.content,"html.parser")
    # print(soup.prettify())
    s=soup.find_all("div")[0].find_all("table")[1].find_all("tr")[1].find_all("table")[1].find_all("table")[0].find_all("table")[0]
    percentage=""
    s=s.find_all("tr")
    for i in s:
        k=i.find_all("td")
        for j in k:
            percentage=j.contents[0]
    print(percentage)

def getBacklogs(k):
    url = urlmain+"Academics/studentbacklogs.aspx"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Accept': '*/*',
    'Cookie': k
    }
    response = requests.request("GET", url, headers=headers)
    soup=BeautifulSoup(response.content,"html.parser")
    soup=soup.body
    soup=soup.find_all("table")[0].find_all("table")[0].find_all("tr")
    print(len(soup)-1)
    l='0'
    for i in soup:
        if l=='0':
            l='1'
            continue
        so=i.find_all("td")[1].contents[0]
        print(so[2:])
    
def gettingthecookies():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    ser = Service(DRIVER_PATH)
    driver=webdriver.Chrome(service=ser,options=options) #loading the chrome driver
    url=urlmain
    driver.get(url) #loading the url
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "txtId2")) )
    username = driver.find_element(By.NAME,'txtId2')
    username.send_keys("18E51A0479")
    password = driver.find_element(By.NAME,'txtPwd2')
    password.send_keys("webcap")
    driver.find_element(By.NAME,'imgBtn2').click()
    try:
        alert = Alert(driver)
        alert.accept()
    except:
        pass
    r=driver.get_cookies()
    driver.quit()
    return 'ASP.NET_SessionId='+r[1]['value']+'; frmAuth='+r[0]['value']

DRIVER_PATH="C:/Users/tilak/Desktop/co/Face-Recognition-Attendance-Projects/chromedriver.exe"
pdf ='xlwt_example.xls'
print(DRIVER_PATH)
urlmain="https://webprosindia.com/hitam/"
k=gettingthecookies()
getpercentage("18E51A0454",k)
getTimeTable(k)
getBacklogs(k)