import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import Select
from urllib3 import request

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
options = webdriver.ChromeOptions()

options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-sh-usage")
options.add_argument("--disable-dev-shm-usage")
class gpaUser:
        def login(self,user,pas):

            self.driver.find_element_by_id('loginForm:username').send_keys(user)
            self.driver.find_element_by_id('loginForm:password').send_keys(pas)
            self.driver.find_element_by_name("loginForm:loginLink").click()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, "#menuForm\\3AmenuTable\\3A 0\\3A categories span").click()
            time.sleep(0.5)
            self.driver.find_element(By.ID, "menuForm:menuTable:0:services:3:serTextTransAll").click()

            self.source = self.driver.page_source
            self.soup = BeautifulSoup(self.source, 'html.parser')
            # myForm\:j_id_id269\:1\:osama > tbody > tr.ROW2 > td:nth-child(3)
            self.Hour =  self.soup.select_one('#myForm\:j_id_id269\:1\:osama > tbody > tr.ROW2 > td:nth-child(3)').text
            self.Point =  self.soup.select_one('#myForm\:j_id_id269\:1\:osama > tbody > tr.ROW2 > td:nth-child(5)').text

            return self.Hour,self.Point

        def putGPA(self,GPAInfo):
            self.driver.find_element(By.ID, "prvCHour").send_keys(GPAInfo[0])
            self.driver.find_element(By.ID, "prvPoint").send_keys(GPAInfo[1])



        def format(self,gpaK):
            self.gpa={
                'gpaKnow':[],
                'gpanew':[],
                'gpaTerm':[]
            }

            self.gpa['gpaKnow']= gpaK

            self.source = self.driver.page_source
            self.soup = BeautifulSoup(self.source, 'html.parser')

            self.totalPoint = self.soup.find('label', {'id': 'totalPoint'}).text
            self.gpa['gpanew'].append(self.totalPoint.replace(' ',''))

            self.totalHour = self.soup.find('label', {'id': 'totalHour'}).text

            self.gpa['gpanew'].append(self.totalHour)

            self.totalRate = self.soup.find('label', {'id': 'totalRate'}).text
            self.gpa['gpanew'].append(self.totalRate)

            self.totalVal = self.soup.find('label', {'id': 'totalVal'}).text
            self.gpa['gpanew'].append(self.totalVal)


            self.totalTermPoint = self.soup.find('label', {'id': 'totalTermPoint'}).text
            self.gpa['gpaTerm'].append(self.totalTermPoint)

            self.totalTermHour = self.soup.find('label', {'id': 'totalTermHour'}).text
            self.gpa['gpaTerm'].append(self.totalTermHour)

            self.totalTermRate = self.soup.find('label', {'id': 'totalTermRate'}).text
            self.gpa['gpaTerm'].append(self.totalTermRate)

            self.totalTermVal = self.soup.find('label', {'id': 'totalTermVal'}).text
            self.gpa['gpaTerm'].append(self.totalTermVal)
            return self.gpa

        def GPA(self,course):

            self.length = len(course)
            self.source = self.driver.page_source
            self.soup = BeautifulSoup(self.source, 'html.parser')

            self.gpakwon =    []
            self.totalPoint = self.soup.find('label', {'id': 'totalPoint'}).text
            self.gpakwon.append(self.totalPoint.replace(' ',''))

            self.totalHour = self.soup.find('label', {'id': 'totalHour'}).text

            self.gpakwon.append(self.totalHour)

            self.totalRate = self.soup.find('label', {'id': 'totalRate'}).text
            self.gpakwon.append(self.totalRate)

            self.totalVal = self.soup.find('label', {'id': 'totalVal'}).text
            self.gpakwon.append(self.totalVal)

            for self.x in range(self.length):

                    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child({}) .subjectHour".format(self.x+1)).send_keys(course[self.x][2])
                    self.select = Select(self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child({}) .subjectRating".format(self.x+1)))
                    self.select.select_by_visible_text('{}'.format(course[self.x][3]))



            return self.format(self.gpakwon)


        def removeC(self,course , c,driver):
            for self.i in course:
                if self.c == self.i[0]:
                    driver.find_element(By.CSS_SELECTOR, "tr:nth-child({}) > td:nth-child(6) > input".format(course.index(self.i)+1)).click()

        
        def tg(self,p,t):
                        
            for x in t :
                if p >=x :
                     return (t[x])
                    
    

        def gg(self,cou,g):
            grades = {'A+':5,'A':4.75,'B+':4.5,'B':4,'C+':3.5,'C':3,'D+':2.5,'D':2,'F':1}
            tG = {4.5:'ممتاز',  
                  3.75:'جيد جداََ'
                  ,2.75:'جيد'
                  ,2 : 'مقبول'}
            self.gpa={
                'gpaKnow':[],
                'gpanew':[],
                'gpaTerm':[]
            }
            tt = 0 
            x = 0 
            for i in cou :
                x += grades[i[3]] * float(i[2])
                tt += int(i[2])
                
            term = x/tt
            gold = float(g[1])/int(g[0])
            gnew = (x+float(g[1])) / ( tt+int(g[0]) )
          
            p = str (round( float( g[1]) ,3))
            
            pp = self.tg(gold,tG)
            self.gpa['gpaKnow'].append (p) 
            self.gpa['gpaKnow'].append(g[0])
            g1 = round(gold,3)
           
            self.gpa['gpaKnow'].append(g1)
            self.gpa['gpaKnow'].append(pp)
            #_________________________
            
            p1 = str(round( ( x+ float(g[1]) ) , 3  ) )
            pp = self.tg(gnew,tG)
            self.gpa['gpanew'].append( p1 ) 
            self.gpa['gpanew'].append( (tt+int(g[0]) ))
           
            g2 = round(gnew,3)
           
            self.gpa['gpanew'].append( g2)
            self.gpa['gpanew'].append( pp)
            #__________________________
            pp = self.tg(term,tG)
            self.gpa['gpaTerm'].append( x)
            self.gpa['gpaTerm'].append(tt)
            g3 = round(term,3)
            self.gpa['gpaTerm'].append(g3)
            self.gpa['gpaTerm'].append(pp)
           
            return self.gpa
            
        def setup(self,cou,user,pas):
            self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=options)
            self.driver.get("https://stu-gate.qu.edu.sa/qu/ui/home.faces")
            time.sleep(0.5)
            self.GPAInfo= self.login(user,pas)
            
            # self.driver.get('https://qu.edu.sa/GPA.aspx')
            # time.sleep(1)
            # self.putGPA(self.GPAInfo)
            # time.sleep(0.5)
            self.ggpa = self.gg(cou,self.GPAInfo)
            # # removeC(cou,'MATH329')
            self.driver.close()
            return self.ggpa
            









    
