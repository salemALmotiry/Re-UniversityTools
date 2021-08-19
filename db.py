import io
from os import SEEK_CUR, replace
import absences
import re
import pymysql.cursors
from prettytable.prettytable import ALL
import CourseInfo
from prettytable import PrettyTable
from prettytable import PLAIN_COLUMNS
from PIL import Image
from hijri_converter import convert
import datetime
import encode
import htm
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pathlib
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-sh-usage")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--start-maximized")
# options.add_argument("window-size=2560,1440")



class data:

    def __init__(self):
        self._host='us-cdbr-east-04.cleardb.com'
        self._port=3306
        self._user="bc3ea75e9bafc2"
        self._passwd="55af81dd"
        self._database="heroku_df0465017476dce"
        self.connection = None
        
        # self._host='localhost'
        # self._port=3306
        # self._user="root"
        # self._passwd="Salem10292@"
        # self._database="telebot"
        # self.connection = None

    def _connect(self):
        self.connection = pymysql.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._passwd,
            database=self._database)


    def insertNewUser(self,chid , user , pas ,method,key):
            self._connect()
            self.cursor= self.connection.cursor()
            self.sql = "insert into users values (%s,%s,%s,%s,%s);"
            self.cursor.execute(self.sql,(chid,user,pas,method,key))

            self.connection.commit()
            self.connection.close()








    def importCoursesForGPA(self,chid , user , pas):
        self._connect()
        self.cursor= self.connection.cursor()

        self.cursor.execute("SELECT id,`CRSE`,Hours,`exp deg` from courses where chat_id = {} and (`exp deg` != '' and `exp deg` !=' ')".format(chid))

        self.abs = absences.gpaUser()

        self.go = self.cursor.fetchall()

        self.GPA=  self.abs.setup(self.go,user,pas)

        t = ''
        d = self.GPA.items()
        tr = '<span class="notify-badge">مرتبة الشرف %s</span>'
        trt = '   <div class="clash-card__level clash-card__level--barbarian" style="font-size: 1.3em;">%s</div>'
        # 2 , 3 , 1, 0,2
        pt = ''
        for x in d:
            if float(x[1][2]) >= 4.5:
                pt = tr %'الأولى'

            if  float(x[1][2]) >= 4.2 and  float(x[1][2]) < 4.5:
                pt =tr% 'الثانية'

            if x[0] == 'gpaKnow' :
                        t+= htm.gpa%(trt%'المعدل التراكمي الحالي',(pt),x[1][2], x[1][3] , x[1][1] , x[1][0],x[1][2])

            elif x[0] == 'gpanew'  :
                        t+= htm.gpa%(trt%'المعدل التراكمي الجديد',(pt),x[1][2], x[1][3] , x[1][1] , x[1][0],x[1][2])

        gpaTnt = htm.gpaimg%(htm.st,t)

        tt1 = ''
        trt = '   <div class="clash-card__level clash-card__level--barbarian" style="font-size: 1.3em;">%s</div>'

        tt1 = htm.gpa%(trt%'المعدل الفصلي',' ',x[1][2], x[1][3] , x[1][1] , x[1][0],x[1][2])

        tt2 = htm.gpaimg%(htm.st,tt1)

        x1 = '%s.png'%chid


        with open('%s.html'%chid,'w',encoding='utf-8') as f :
            f.write(gpaTnt)


        x = pathlib.Path('%s.html'%chid).absolute()
        y = 'file://'+str(x)
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=options)

        self.driver.get(y)

        self.driver.set_window_size(1824, 1200)
        self.driver.maximize_window()
        self.driver.get_screenshot_as_file(x1)



      #__________________________________________________________________________

        with open('%sp.html'%chid,'w',encoding='utf-8') as f :
            f.write(tt2)

        x = pathlib.Path('%sp.html'%chid).absolute()
        y = 'file://'+str(x)
        self.driver.get(y)

        x = self.driver.find_element_by_id('as12').screenshot_as_png
        image = Image.open(io.BytesIO(x))

        x2 = '%sp.png'%chid
        image.load()
        image.save(x2)

        self.driver.quit()

        os.remove("%s.html"%chid)
        os.remove("%sp.html"%chid)
        self.connection.close()





    def coursesTable(self):
        self._connect()
        self.cursor= self.connection.cursor()
        self.sql= " create table IF NOT EXISTS Courses ( id int NOT NULL AUTO_INCREMENT primary key,courseCode varchar(10),courseName varchar(50),Hours int, courseRate int,Instructor varchar(200));"


        self.cursor.execute(self.sql)
        self.connection.close()


    def getsCourse(self):
        self._connect()
        self.cursor= self.connection.cursor()
        course = CourseInfo.setup()
        self.insertCoursesIntoTable(course)
        self.connection.close()

    def getinfo(self,chid):
        self._connect()
        self.cursor= self.connection.cursor()
        self.cursor.execute("select method from users where chat_id={};".format(chid))
        self.info = self.cursor.fetchone()[0]
        self.connection.close()
        return self.info

    def getUserinfo(self,chid,key="",pas=""):
         self._connect()
         self.cursor= self.connection.cursor()

         self.cursor.execute("select * from users where chat_id={};".format(chid))

         self.info = self.cursor.fetchall()

         if self.info[0][2]=='1':
               self.pas = encode.decode1(self.info[0][3])
               self.connection.close()
               return(self.info[0][1],self.pas)

         if self.info[0][2]=='2':
             self.pas = encode.decode1(self.info[0][3],key)
             self.connection.close()
             return (self.info[0][1],self.pas)
         if self.info[0][2]=='3':
             self.connection.close()
             return self.info[0][1]

    def getKey(self,chid):
        self._connect()
        self.cursor= self.connection.cursor()
        self.cursor.execute("select `key` from users where chat_id={};".format(chid))
        self.info = self.cursor.fetchone()[0]
        self.connection.close()
        return self.info




    def importforMsg(self):
        self._connect()
        self.cursor= self.connection.cursor()

        self.cursor.execute("SELECT chat_id from users")

        x = self.cursor.fetchall()
        self.connection.close()
        return x


    def insertCoursesIntoTable(self,course,chid,user):

                self._connect()
                self.cursor= self.connection.cursor()


                sql = "INSERT INTO courses (chat_id,CRSE,`CRSE NAME`,Actvity,Hours,`final exam`,`Exp deg`,Instructor ) VALUES (%s,'%s','%s','%s','%s','%s','%s','%s')"


                c = list(map(lambda x : sql%(chid,x[0],x[1],x[2],x[3],x[4],x[5],x[6]), course ) )

                for x in c :
                       self.cursor.execute(x)
                       self.connection.commit()


                self.connection.close()
                self.uploadcalendar(chid,user)


    def cleardeg(self,id):
        self._connect()
        self.cursor= self.connection.cursor()
        self.cursor.execute("update courses set `Exp deg` =' ' where chat_id = {} ".format(id))
        self.connection.commit()
        self.connection.close()
        
    def importCourse(self,chid):

        self._connect()
        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT id,`CRSE`,Hours,`exp deg` ,`crse name`from courses where chat_id = {} and (Hours != '' and Hours !=' ' ) ".format(chid))
        self.tem = self.cursor.fetchall()
        self.connection.close()
        return self.tem





    def retrunids(self,chid):

        self.r = self.importCourse(chid)

        return list(map(lambda x : x[0],self.r   ))
  
    def importCourseEvl(self,chid):
        self._connect()
        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT id,`CRSE`,`Actvity` from courses where chat_id = {}".format(chid))   
        self.cus = self.cursor
        
        return self.cus
        
    def retrunids_evl(self,chid):
        self._connect()
        self.cursor= self.connection.cursor()
     
        self.r = self.importCourseEvl(chid).fetchall()  
     
        return list(map(lambda x : x[1],self.r       ))
    




    def insertRate(self,rate):
        self._connect()
        self.cursor= self.connection.cursor()
        self.x = len(rate)
        for i in range(self.x):
            self.sql = " UPDATE courses SET `exp deg` = '{}'  WHERE id = {};".format(rate[i][1],rate[i][0])

            self.cursor.execute(self.sql)
            self.connection.commit()

        self.connection.close()







    def ifUserExists(self,chid):
        self._connect()
        self.cursor= self.connection.cursor()
        self.sql = "SELECT EXISTS(SELECT chat_id FROM users WHERE chat_id = {}) as truth;".format(chid)
        self.cursor.execute(self.sql)
        self.tem = self.cursor.fetchall()[0][0]
        self.connection.close()
        return self.tem



    def uploadcalendar(self,chid,user):

        self._connect()
        self.cursor= self.connection.cursor()
        with open('{}.png'.format(user), 'rb') as self.f:
            self.img = self.f.read()
        self.cursor.execute("insert into calendar (chat_id ,calendar )values(%s,%s)",(chid,self.img))
        self.connection.commit()
        os.remove('%s.png'%user)
        self.connection.close()



    def retrunCalemdar(self,chid):
            self._connect()
            self.cursor= self.connection.cursor()
            self.cursor.execute('select calendar from calendar where chat_id = {}'.format(chid))
            self.cal = self.cursor.fetchall()

            # The returned data will be a list of list
            self.image = self.cal[0][0]
            # binary_data = base64.b64decode(image)

            # Convert the bytes into a PIL image
            self.image = Image.open(io.BytesIO(self.image))
            self.connection.close()

            return self.image


    def x (self,p):


        textS = '''
                    <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>

                </tr>
                    '''
                   
        dateformqu = p[2].split('[')
        date = re.split('-',dateformqu[0])
        moresplit = dateformqu[1].replace(']','')
        finalformat = re.split("-",str(moresplit))
        finalformat = re.split(" ",str(finalformat[0]))
        finalformat =re.split(":",str(finalformat[1]))



        convertedDate = convert.Hijri(int(date[2]),int(date[1]),int(date[0])).to_gregorian()# convert from hijri to Gregorian

        #greDateAftersplit = str(convertedDate).split('-')# split Gregorian gets from hijri converter for use it in datetime
        greDateAftersplit = re.split("-",str(convertedDate))

        finalExamDate = datetime.datetime(int(greDateAftersplit[0]),int(greDateAftersplit[1]),int(greDateAftersplit[2]),int(finalformat[0]),int(finalformat[1]))
        # The finalExamDate above is the exam date after all data has been processed

        todayDate= datetime.datetime.today().replace(second=0, microsecond=0) # today date for calculate difference between dates

        leftDate = finalExamDate - todayDate # how many left time before exam
        leftDate = str(leftDate)
        c =  int(leftDate[:2])
        if c < 0 :
            return ' '
        
        y = p[2].split('[')

        ttr = y[1].split('-')



        finalDatemsg_2 = textS %(str(leftDate).replace(',',' and'),str(ttr[1]).replace(']',''),
                             str(ttr[0]).replace('[',''),str(convertedDate), str(p[1]), str(p[0])

                             )
        return finalDatemsg_2


    def finalDate(self,chid):


        self._connect()
        self.cursor= self.connection.cursor()
        self.cursor.execute("SELECT `CRSE`,`CRSE NAME`,`final exam` from courses where chat_id = %s and (`final exam` != '' and `final exam` !=' ')"%(chid))


        self.x = list(    map(self.x, self.cursor.fetchall())           )

        t = ''
        for i in  self.x  :
           t += i

        self.thm = htm.htm%(t)


        x1 = '%sc.png'%chid


        open('%sc.html'%chid,'w',encoding='utf-8').write(self.thm)


        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=options)


        x = pathlib.Path('%sc.html'%chid).absolute()
        y = 'file://'+str(x)

        self.driver.get(str(y))

        self.driver.set_window_size(3500, 2300)
        self.driver.maximize_window()
        x = self.driver.find_element_by_id('as12').screenshot_as_png
        image = Image.open(io.BytesIO(x))

        image.load()
        image.save(x1)
        self.driver.quit()


        self.connection.close()






    def takenote(self,chid,note):
        self._connect()
        self.cursor= self.connection.cursor()
        self.sql = "insert into  notes values (%s , %s)"
        self.val = (chid,note)
        self.cursor.execute(self.sql , self.val)

        self.connection.commit()
        self.connection.close()



    def importNote(self,chid):
            self._connect()
            self.cursor= self.connection.cursor()

            self.cursor.execute('select note from notes where chat_id = {};'.format(chid))
            self.notes = self.cursor.fetchall()

            self.msg = str()
            for self.p in self.notes:
                    self.msg += str('\n'+self.p[0])
            self.connection.close()

            return self.msg


    

 



    def check_if_deg_empty(self,chid):
        #   self._connect()
        #   self.cursor= self.connection.cursor()
        #   self.cursor.execute('SELECT EXISTS(SELECT `exp deg` FROM courses WHERE `exp deg` = " " and chat_id = {})  as truth ;'.format(chid))

       self.t  = self.importCourse(chid)

       for x in self.t:
           if x[3]==' ' or x[3]=='':
               return 1

   

    def close(self):
        self.connection.close()




# x = ' 8-05-1443 [ 10:30 ص-12:30 م]'

# y = x.split('[')

# print(y[1].replace(']',''))