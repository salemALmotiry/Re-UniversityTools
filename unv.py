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


options = Options()
reachOut = {
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






    def ule(self):
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=options)
        self.driver.get("https://stu-gate.qu.edu.sa/qu/ui/home.faces")
        time.sleep(0.4)


    def login(self,user , pas):
        self.driver.find_element_by_id('loginForm:username').send_keys(user)
        self.driver.find_element_by_id('loginForm:password').send_keys(pas)
        self.driver.find_element_by_name("loginForm:loginLink").click()
        time.sleep(0.5)

    def reachingPonit(self,reachOut ,user, access):
        self.driver.find_element_by_id(reachOut[0]).click()
        time.sleep(0.5)
        self.driver.find_element_by_id(reachOut[1]).click()
        time.sleep(0.5)
        if access == 0 :
            self.course = list()
            self.table = self.driver.find_element_by_id("j_id_id241:dataTbl")
            self.rows = self.table.find_elements_by_tag_name("tr")
            for self.row in self.rows:
                self.tds = self.row.find_elements_by_tag_name("td")
                if len(self.tds) > 20:
                    self.course.append([self.tds[0].text, self.tds[4].text,self.tds[8].text,self.tds[11].text ,self.tds[50].text,' ',self.tds[54].text])
            self.driver.find_element_by_id('j_id_id241:schdText').click()
            time.sleep(1)
            self.driver.set_window_size(1200, 990)
            self.driver.maximize_window()
            time.sleep(0.4)
            self.driver.execute_script("window.scrollTo(0, window.scrollY + 340)")

            self.element = self.driver.find_element_by_css_selector("#myForm").screenshot('{}.png'.format(user))
            return self.course
        if access == 1 :
                self.driver.set_window_size(2550, 1900)
                self.driver.maximize_window()
                time.sleep(0.4)
                self.e = self.driver.find_element_by_id('j_id_id241').screenshot_as_png
                self.image = Image.open(io.BytesIO(self.e))
                return self.image
        if access == 2 :
                self.driver.set_window_size(1024, 600)
                self.driver.maximize_window()
                time.sleep(0.4)
                self.e = self.driver.find_element_by_css_selector('#form1').screenshot_as_png
                self.image = Image.open(io.BytesIO(self.e))
                return self.image


    def setup (self,user,pas,reach,access,course=''):
        if access == "Evl":
            print(course)
            self.ule()
            self.login(user,pas)
            self.auto(course)
            self.Evaluation()
            self.e = self.driver.find_element_by_css_selector('#frm').screenshot_as_png
            self.image = Image.open(io.BytesIO(self.e))
            return self.image
             

        self.ule()
        self.login(user,pas)
        self.result = self.reachingPonit(reachOut[reach],user,access)
        # os.remove('{}.png'.format(user))
        self.driver.close()
        return self.result
