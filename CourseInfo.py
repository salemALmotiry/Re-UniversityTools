import io
import time
import os
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup


options = Options()
QuList = {
            'course':['menuForm:menuTable:1:categories','menuForm:menuTable:1:services:1:serTextStudSchedule'],
            'absences':['menuForm:menuTable:5:categories','menuForm:menuTable:5:services:3:serTextStudAbs'],
            'grades':['menuForm:menuTable:1:categories','menuForm:menuTable:1:services:2:serTextCrsRes'],
            'docum':['menuForm:menuTable:5:categories','menuForm:menuTable:5:services:6:stdReportsTxt']

    }
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-sh-usage")
options.add_argument("--disable-dev-shm-usage")

class qu :
    def urlQu(self):
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=options)
        self.driver.get("https://stu-gate.qu.edu.sa/qu/ui/home.faces")
        time.sleep(0.3)
    
    def login(self,user , pas):
        self.driver.find_element_by_id('loginForm:username').send_keys(user)
        self.driver.find_element_by_id('loginForm:password').send_keys(pas)
        self.driver.find_element_by_name("loginForm:loginLink").click()
        time.sleep(0.5)

    def reachOut(self,idf):  
        self.driver.find_element_by_id(idf[0]).click()
        time.sleep(0.5)
        self.driver.find_element_by_id(idf[1]).click()
        time.sleep(0.2)
   
    def getsCourses(self,user,pas):
            self.urlQu()
            self.login(user,pas)
            self.reachOut(QuList['course'])
            self.course = list()
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            s = soup.find('table',{'id' : 'j_id_id241:dataTbl'}).find('tbody')

            i = 1
            for f in s.find_all('tr'):
                try:
                    self.course.append([f.find('td', {'data-th': 'رمز المقرر'}).find('span', {'class': 'fontTextSmall'}).text
                                ,f.find('td', {'data-th': 'اسم المقرر'}).find('span', {'class': 'fontTextSmall'}).text
                                ,f.find('td', {'data-th': 'النشاط'}).text
                                , f.select('#j_id_id241\:dataTbl > tbody > tr:nth-child(%s) > td:nth-child(6) > center' % i)[0].text.strip()
                                ,f.select('#j_id_id241\:dataTbl > tbody > tr:nth-child(%s) > td:nth-child(9) > table > tbody > tr:nth-child(2) > td'%i)[0].text.strip()
                                , ''
                                , f.select('#j_id_id241\:dataTbl > tbody > tr:nth-child(%s) > td:nth-child(10) > center' % i)[ 0].text.strip()

                                ])
                    i = i  + 1
                except:
                    continue
                
            self.driver.find_element_by_id('j_id_id241:schdText').click()
            time.sleep(1)
            self.driver.set_window_size(1200, 990)
            self.driver.maximize_window()
            time.sleep(0.4)
            self.driver.execute_script("window.scrollTo(0, window.scrollY + 340)")

            self.element = self.driver.find_element_by_css_selector("#myForm").screenshot('{}.png'.format(user))
            return self.course
   
    def absences(self,user,pas):
                self.urlQu()
                self.login(user,pas)
                self.reachOut(QuList['absences'])
                self.driver.set_window_size(2550, 1900)
                self.driver.maximize_window()
                time.sleep(0.4)
                self.e = self.driver.find_element_by_css_selector('body > div.intrPage.main > div.container > div.content > div.sysContent.col-sm-9 > table > tbody > tr:nth-child(3)').screenshot_as_png
                self.image = Image.open(io.BytesIO(self.e))
                return self.image
    
    def Greads(self,user,pas):
                self.urlQu()
                self.login(user,pas)
                self.reachOut(QuList['grades'])
                self.driver.set_window_size(1500, 900)
                self.driver.maximize_window()
                time.sleep(0.4)
                self.e = self.driver.find_element_by_css_selector('body > div.intrPage.main > div.container > div.content > div.sysContent.col-sm-9 > table > tbody > tr:nth-child(3)').screenshot_as_png
                self.image = Image.open(io.BytesIO(self.e))
                return self.image
            
   
    def Eval(self,user,pas,course):
            self.urlQu()
            self.login(user,pas)
            self.auto(course)
            self.Evaluation()
            self.e = self.driver.find_element_by_css_selector('#frm').screenshot_as_png
            self.image = Image.open(io.BytesIO(self.e))
            return self.image
        
    def Evaluation(self) :
        self.driver.find_element_by_id("menuForm:menuTable:0:categories").click()
        time.sleep(0.5)

        self.driver.find_element_by_id("menuForm:menuTable:0:services:8:serTextEvaluation").click()
        time.sleep(0.5)

    def auto (self,course):



        for x in course :

                        self.Evaluation()
                        self.driver.find_element_by_link_text(x[0]).click()

                        tr = 2
                        table = 3
                        for j in range(24):
                            if (tr == 13):
                                self.driver.find_element_by_xpath("/html[1]/body[1]/div[11]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[3]/td[1]/form[1]/table[4]/tbody[1]/tr[3]/td[1]/table[1]/tbody[1]/tr[13]/td[4]/input[1]").click()
                                tr += 1
                            path0 = "/html[1]/body[1]/div[11]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[3]/td[1]/form[1]/table[{}]/tbody[1]/tr[3]/td[1]/table[1]/tbody[1]/tr[{}]/td[{}]/input[1]"

                            path = path0.format(table, tr, x[1])
                            self.driver.find_element_by_xpath(path).click()
                            tr += 1

                            if (j == 2):
                            #  ((IJavaScriptExecutor)driver).ExecuteScript("window.scrollTo(0,505)")
                                self.driver.execute_script("window.scrollTo(0,505)")
                                table = 4
                                tr = 2
                            if (j == 18):
                                    self.driver.execute_script("window.scrollTo(0,1000)")
                                    table = 5
                                    tr = 2
                                #//jump
                            if (j == 22):
                                    tr = 2
                                    table = 6
                                    time.sleep(0.4)
                        self.driver.execute_script("window.scrollTo(1000,1300)")
                        time.sleep(0.4) ##frm > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > a
                        self.driver.find_element_by_css_selector('#frm > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > a').click()
                        time.sleep(0.5)
                        # # //   driver.FindElement(By.CssSelector("a[href='javascript:submitForm(\\'/qu\')']")).Click()
                        # # //      driver.FindElement(By.Id("frm:saveEval")).Click()
                        # driver.FindElement(By.CssSelector("#frm > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > a")).Click()
                        # time.sleep(0.4)
   
    def clo(self):
        self.driver.close()
   

    
  
    
        
        
        
    
   