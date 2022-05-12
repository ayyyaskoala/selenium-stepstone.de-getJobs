import sqlite3
import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

con = sqlite3.connect("myLinks.db")
cursor = con.cursor()

TimerStart = time.time()

cursor.execute("""CREATE TABLE IF NOT EXISTS datenTamam(firmenName TEXT,
                                                        articleName TEXT,
                                                        standort TEXT,
                                                        stelle TEXT,
                                                        vollzeit TEXT,
                                                        field1 TEXT,
                                                        field2 TEXT,
                                                        field3 TEXT,
                                                        field4 TEXT,
                                                        field5 TEXT)""")   

cursor.execute("""CREATE TABLE IF NOT EXISTS datenYok(  firmenName TEXT,    
                                                        articleName TEXT,
                                                        url TEXT)""")
con.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS aussnahmen( firmenName TEXT,    
                                                        articleName TEXT,
                                                        url TEXT)""")
con.commit()

cursor.execute("SELECT * FROM links")
links = cursor.fetchall()


driver =  webdriver.Firefox() 
driver.set_window_size(1024, 768)
driver.set_window_position(0,0)

print("browser açılıyor");time.sleep(5)

cookie_have_to_close = True

for url in links:
    print("***************************************** \n")
    url = "https://www.stepstone.de"+str(url[1])
    driver.get(url)
    time.sleep(2)


    

    while True:
        if driver.execute_script("return document.readyState") != "complete": 
            time.sleep(0.5) 
        else:              
            exec1 = driver.execute_script("return document.getElementsByClassName('sec-container').length")
            if exec1 == 1:
                print("Onloading Page") 
                time.sleep(10)
                
                exec2 = driver.execute_script("return document.getElementsByClassName('sec-container').length")
                if exec2 == 1:
                    print("still onloading page..have to F5")
                    driver.refresh()
                    time.sleep(5)

            exec3 = driver.execute_script("return document.getElementsByClassName('sec-container').length")
            if exec3 == 0:
                print("no loading")
                break

    contine = True

    while True:
        try:     
            time.sleep(2)
            html_icerigi = driver.page_source
            soup = BeautifulSoup(html_icerigi, 'lxml')

            if cookie_have_to_close:
                xpath = "/html/body/div[9]/section/div/section/div[2]/div[1]/div[2]/div/span"
                driver.find_element(by=By.XPATH, value=xpath).click()
                print("coockies eaten")
                cookie_have_to_close = False    
                time.sleep(2)  
            
            classpath = "sc-VigVT bSSguc"
            top = list(soup.find("div",{"class":"sc-VigVT bSSguc"}))

            articleName = top[0].find('a').text
            firmenName = top[1].find('h1').text
            thirdTop = list(top[2].find('ul'))
            
            
            if len(thirdTop) == 4:
                standort = thirdTop[0].text
                stelle = thirdTop[1].text
                vollzeit = thirdTop[2].text
                
                print(articleName)
                print(standort)
                print(stelle)
                print(vollzeit)

            elif len(thirdTop) == 5:
                standort = thirdTop[1].text
                stelle = thirdTop[2].text
                vollzeit = thirdTop[3].text
                
                print(articleName)
                print(standort)
                print(stelle)
                print(vollzeit)
            
            else:
                cursor.execute("INSERT INTO aussnahmen VALUES(?,?,?)",(articleName,firmenName,url))
                con.commit()
                break
                
            descriptions = soup.find("div",{"class":"js-app-ld-ContentBlock"}).find("div")

            if len(descriptions) == 5 : 
                c = 1 
                for e in descriptions:
                    exec("field{} = e.text".format(c))
                    c += 1

                cursor.execute("INSERT INTO datenTamam VALUES(?,?,?,?,?,?,?,?,?,?)",(firmenName,articleName,standort,stelle,vollzeit,field1,field2,field3,field4,field5))
                con.commit()

            elif len(descriptions) == 4:
                c = 1 
                for e in descriptions:
                    exec("field{} = e.text".format(c))
                    c += 1

                field5 = field4
                field4 = ""

                cursor.execute("INSERT INTO datenTamam VALUES(?,?,?,?,?,?,?,?,?,?)",(firmenName,articleName,standort,stelle,vollzeit,field1,field2,field3,field4,field5))
                con.commit()

            elif len(descriptions) == 3:
                c = 1 
                for e in descriptions:
                    exec("field{} = e.text".format(c))
                    c += 1
                
                field4 = ""
                field5 = ""

                cursor.execute("INSERT INTO datenTamam VALUES(?,?,?,?,?,?,?,?,?,?)",(firmenName,articleName,standort,stelle,vollzeit,field1,field2,field3,field4,field5))
                con.commit()

            else:
                cursor.execute("INSERT INTO datenYok VALUES(?,?,?)",(articleName,firmenName,url))
                con.commit()

            break

        except:
            if contine == False:
                cursor.execute("INSERT INTO datenYok VALUES(?,?,?)",("None","None",url))
                con.commit()
                contine = True
                print("Kayıt  YOK")
                break
            
            else:
                contine = False
                driver.refresh()  
                print("REFRESHING");time.sleep(10)    

        print((int(time.time()) - int(TimerStart))/60)

         






























