from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from selenium import webdriver

import sqlite3,time


start = time.time()
con = sqlite3.connect("myLinks.db")
cursor = con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS links(url1 TEXT,url2 TEXT,url3,saved TEXT)")   

url = "https://www.stepstone.de/5/job-search-simple.html?what=IT-Support&where=Bayern&radius=100&searchOrigin=Homepage_top-search&rsearch=1"

counter = 0
driver = webdriver.Firefox("")
driver.set_window_position(0, 0)
driver.set_window_size(1024, 768)

driver.get(url)

time.sleep(5)
driver.refresh()
time.sleep(10)


xpath = "/html/body/div[4]/section/div/section/div[2]/div[1]/div[2]/div/span"
driver.find_element(by=By.XPATH, value=xpath).click()
print("coockies eaten")

while True:    
    html_icerigi = driver.page_source
    soup = BeautifulSoup(html_icerigi, 'lxml')

    JobsList = soup.find_all('div',{"class":"Wrapper-sc-11673k2-0 fpBevf"} )


    #Looping alle link in Artikeln
    for Job in JobsList:
        counter =+  1
        JobArticle = Job.find("div").find('article')
        elementsA = JobArticle.find_all('a')

        if len(elementsA) == 3:
            href1= elementsA[0]['href']
            href2= elementsA[1]['href']
            href3= elementsA[2]['href']   
        else:
            print("\n\n\n\n\n\n not 3 links ")
            continue
        
        cursor.execute("INSERT INTO links VALUES(?,?,?,?)",(href1,href2,href3,"0"))
        con.commit()
    

    #Try to open next page
    try:
        xpath = "/html/body/div[3]/div[3]/div/div/div[2]/div/div[2]/div[3]/div/a[2]"
        driver.find_element(by=By.XPATH, value=xpath).click()
        print("going to next page")
    except:
        print("Next Button not clickable")
        try:
            xpath = "/html/body/div[3]/div[3]/div/div/div[2]/div/div[2]/div[3]/div/a[2]"
            element1 = driver.find_element(by=By.XPATH, value=xpath)
            href = element1.get_attribute("href")
            driver.get(href)    
        except: 
            print("second NEXT try failed\nor may we're done")
            break



    print((int(time.time()) - int(start))/60)
    
    time.sleep(5)




 