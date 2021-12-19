from datetime import datetime
import pathlib
from re import T, escape
from time import sleep
from typing import List
import telebot
import os
from telebot import *
from prettytable import PrettyTable
from prettytable import from_db_cursor
from prettytable.prettytable import ALL
from prettytable import *
import message
from PIL import Image
import CourseInfo
import db
import encode
TOKEN = os.environ.get('API_KEY')
bot = telebot.TeleBot(TOKEN)



def active(target):
    
    f = open('active.txt','r').read()
    f = re.split(',',f)
    return bool( list(( filter(   lambda item : item == str(target)    ,f)    )))
     

 
@bot.message_handler(commands=['start'])
def start(msg):
        d = db.data()  # create object from database class
        q =  d.uesrActive(msg.chat.id)
        if active(msg.chat.id) == True and  q ==0:
           b = BotHandler()
           b.ShowMethods(msg)
           

 
@bot.message_handler(commands=['active'])
def act(msg):          
           if msg.chat.id==340095920:
                   bot.reply_to(msg,'ارسل')
                   bot.register_next_step_handler(msg,ActivateID)
                   
def ActivateID(msg):   
        f = open('active.txt','a')
        f.write(',%s'%msg.text)
        bot.reply_to(msg,'تم التفعيل')


@bot.message_handler(commands=['myid'])
def myid(msg):  
         bot.reply_to(msg,msg.chat.id)
 


@bot.message_handler(commands=['schedule'])
def Schedule(msg):
    d = db.data()  # create object from database class
    if d.uesrActive(msg.chat.id)==0:
         bot.reply_to(msg,'ليس لديك صلاحيات')
         return
    chid = msg.chat.id
    d = db.data()
    calender = d.retrunCalemdar(chid)
    bot.send_photo(chid, calender)
    del d
 

@bot.message_handler(commands=['absence']) # done
def abs(msg):
   
    d = db.data()  # create object from database class
    if d.uesrActive(msg.chat.id)==0:
         bot.reply_to(msg,'ليس لديك صلاحيات')
         return
    bo = BotHandler()
    bo.NecessaryInformation(msg,'absence')
    del bo
 

@bot.message_handler(commands=['grades']) # done
def greads(msg):
    d = db.data()  # create object from database class
    if d.uesrActive(msg.chat.id)==0:
         bot.reply_to(msg,'ليس لديك صلاحيات')
         return

    bo = BotHandler()
    bo.NecessaryInformation(msg,'grades')
    del bo




@bot.message_handler(commands=['final'])
def final(msg):
    d = db.data()  # create object from database class
    if d.uesrActive(msg.chat.id)==0:
         bot.reply_to(msg,'ليس لديك صلاحيات')
         return
    chid = msg.chat.id  # chat id
    d = db.data()  # object from database class
    
    bot.send_message(msg.chat.id,"قيد التنفيذ")
    d.finalDate(chid)  # gets final dates exam data from data base class
    image = Image.open('%sc.png'%chid)
    image.load()
    bot.send_photo(chid,image)
    os.remove('%sc.png'%chid)
    os.remove('%sc.html'%chid)
    del d



@bot.message_handler(commands=['gpa'])
def gpa(msg):
    d = db.data()  # create object from database class
    if d.uesrActive(msg.chat.id)==0:
         bot.reply_to(msg,'ليس لديك صلاحيات')
         return
     
    chid = msg.chat.id
   
    botHand = BotHandler()  # create object from Bot Handler
   
  
    if d.check_if_deg_empty(chid) == 1:  # check if any course rate empty
        botHand.printTable(chid)
        botHand.newRate(msg, chid)
    else:

        botHand.editrate(msg, chid)



@bot.message_handler(commands=['evaluation'])
def docum(msg):
    d = db.data()  # create object from database class
    bo = BotHandler()
    if d.uesrActive(msg.chat.id)==0:
         bot.reply_to(msg,'ليس لديك صلاحيات')
         return
   
   
    bo.printtableforEvl(msg.chat.id)
    
    bo.newEvl(msg,msg.chat.id)
    

 


@bot.message_handler(commands=['reset'])
def reset(msg):
    d = db.data()  # create object from database class
    if d.uesrActive(msg.chat.id)==0:
         bot.reply_to(msg,'ليس لديك صلاحيات')
         return
    botHand = BotHandler()  # create object from Bot Handler
    botHand.NecessaryInformation(msg,'reset')
    


class BotHandler():
    def __init__(self):
        self.info = list()
    
    def handler(self,msg,user,pas,Type):
          
            
            bot.reply_to(msg,'قيد التنفيذ')
            self.Qu = CourseInfo.qu()
            self.d = db.data()
            if Type =='absence':
                self.img = self.Qu.absences(user,pas)
                bot.send_photo(msg.chat.id, self.img)  # send absences img
            if Type =='grades':
                self.img = self.Qu.Greads(user,pas)
                bot.send_photo(msg.chat.id, self.img)  # send absences img
            if Type=='gpa':
                        self.info = self.d.getUserinfo(msg.chat.id)
                        self.d.importCoursesForGPA(msg.chat.id,user, pas)   
                        image = Image.open('%s.png'%msg.chat.id)
                        bot.send_photo(msg.chat.id,image)
                        os.remove('%s.png'%msg.chat.id)
                        
                        image = Image.open('%sp.png'%msg.chat.id)
                        bot.send_photo(msg.chat.id,image)
                        os.remove('%sp.png'%msg.chat.id)
            
            if Type == 'reset':
                bot.reply_to(msg,'يتم إعادة التعيين الرجاء الأنتظار')
                self.d.deleteCourses(msg.chat.id)
                self.course = self.Qu.getsCourses(user,pas)
                self.d.insertCoursesIntoTable(self.course,msg.chat.id,user)
                bot.send_message(msg.chat.id,'تمت إعادة التعيين ')
            if Type == 'Evl':
                
                 img = self.Qu.Eval(user,pas,self.x_Evl)
                 bot.send_photo(msg.chat.id, img)  # send absences img
           
            
            
    def NecessaryInformation(self,msg,Type):
            
             
              
               
            self.d= db.data()  # object of data base class
            self.method = self.d.getinfo(msg.chat.id)  # gets info form sing in
            if self.method == '1':
               self.info=  self.d.getUserinfo(msg.chat.id)
               self.handler(msg,self.info[0],self.info[1],Type)
            else: 
                    bot.send_message(msg.chat.id,'أدخل رمز الدخول')
                    bot.register_next_step_handler(msg,self.secondM,Type)
                    
    def secondM(self,msg,Type):
                key = msg.text
               
                hash = encode.hash1(key)
                self.d= db.data()
               
                if hash != self.d.getKey(msg.chat.id):
                    
                        bot.send_message(msg.chat.id,'أعد ادخال الرمز')
                        bot.register_next_step_handler(msg,self.NecessaryInformation,Type)
                        return
                        
             
                self.info= self.d.getUserinfo(msg.chat.id,key)
                self.handler(msg,self.info[0],self.info[1],Type)


                                 
    def ShowMethods(self,msg):
         
                self.markup = types.ReplyKeyboardMarkup()
                self.methodOne = types.KeyboardButton('1')
                self.methodTwo = types.KeyboardButton('2')
                self.markup.row(self.methodOne, self.methodTwo)
                bot.send_message(msg.chat.id, message.loginMsg, reply_markup=self.markup)
                bot.register_next_step_handler(msg,self.methods,self.markup)


    i_evl= 1
    
    row_evl=0
    
    
    
    def newEvl(self, message, chid):
        if self.i_evl<= self.row_evl:
            global markup

            markup = types.ReplyKeyboardMarkup()
            itembtnap = types.KeyboardButton('موافق بشدة')
            itembtna = types.KeyboardButton('موافق')
            itembtnbp = types.KeyboardButton('غير متأكد')
            itembtnb = types.KeyboardButton('غير موافق')
            itembtncp = types.KeyboardButton('غير موافق بشدة')
            markup.row(itembtnap, itembtna)
            markup.row(itembtnbp, itembtnb, itembtncp)
            
            bot.send_message(chid, "rate course {}".format(self.ids_evl[self.i_evl-1]), reply_markup=markup)

            bot.register_next_step_handler(message, self.dealwithCourseTaple_Evl)
        if self.i_evl> self.row_evl:
            
            evltonum  = {
                            'موافق بشدة':2,
                            'موافق':3,
                            'غير متأكد':4,
                            'غير موافق':5,
                            'غير موافق بشدة':6
                            
                        }
            markup = types.ReplyKeyboardRemove()
          
            bot.send_message(chid, "انتهيت من التعيين", reply_markup=markup)
          
            self.x_Evl = list(map(lambda q: (q[0] ,evltonum[q[1]]) , self.x_Evl ))
          
           
            self.NecessaryInformation(message,'Evl')

    
    x_Evl = list()

    # this function deal with rate of course when ends
    def dealwithCourseTaple_Evl(self, message):

        if self.i_evl <= self.row_evl:

            self.x_Evl.append([self.ids_evl2[self.i_evl-1 ], message.text])
            
            self.i_evl += 1
            self.newEvl(message, message.chat.id)

        elif message.text == "سلام":
            bot.reply_to(message, "done")

    
    
    
    
    
    
    
    def printtableforEvl(self,chid):
        self.v = db.data()
        self.ids_evl,self.ids_evl2 = self.v.retrunids_evl(chid)
        self.row_evl= len(self.ids_evl2)
        
       
    
            

    def methods(self, msg, markup):
            self.method = msg.text  # method
          
            if self.method not in ['1','2','3']:
                    bot.reply_to(msg,'أعد ادخال الرقم')
                    bot.register_next_step_handler(msg,self.methods,markup)
                    return
            
            markup = types.ReplyKeyboardRemove()
            bot.send_message(msg.chat.id, "ادخل الرقم الجامعي", reply_markup=markup)
            bot.register_next_step_handler(msg, self.user, self.method)
        

    def user(self, msg, method):
            
            bot.send_message(msg.chat.id, 'ارسل الرقم السري')
            bot.register_next_step_handler(msg, self.password, msg.text, method)
   
    def password(self, msg, user, method):
   
        purePassword = msg.text
        self.chid = msg.chat.id
        self.uoload = db.data()
        self.p = CourseInfo.qu()
       
        try :  
            bot.send_message(self.chid, 'يتم التحقق من صحة البيانات')
            self.course = self.p.getsCourses(user,purePassword)
            
        except Exception:
                        bot.send_message(self.chid, 'الرقم الجامعي او كلمة السر تم أدخال أحدهما بشكل خاطئ تأكد من البيانات المرسلة.')
                        bot.send_message(self.chid, 'أدخل الرقم الجامعي')
                        bot.register_next_step_handler(msg, self.user,method)
                        return

        bot.send_message(self.chid, 'تم التحقق من صحة البيانات')    
        if method == '1':
                   
                bot.send_message(self.chid, 'يتم اعداد البوت انتظر')
        
                self.info =(user,msg.text)
        
                self.pas = encode.encode1(self.info[1])
                self.uoload.insertNewUser(self.chid, self.info[0], '1', self.pas, 'none')
                self.uoload.insertCoursesIntoTable(self.course,self.chid,self.info[0]) 
                bot.send_message(self.chid, "تم الأنتهاء من أعداد البوت تستطيع استخدامه ")
                
             
                          
                   
                 
                    
        if method == '2':
            
            bot.send_message(self.chid,"ارسل رمز لفك التشفير سيتم طلبه بدلاََ من كلمة السر")
            bot.register_next_step_handler(msg,self.secondMethod,user,purePassword, self.course)
        if method == '3':
                    bot.send_message(self.chid, 'يتم اعداد البوت انتظر')
                   
                    self.uoload.insertNewUser(self.chid, user, '3', 'none', 'none')
                    self.uoload.insertCoursesIntoTable(self.course,self.chid,user)
                    bot.send_message(self.chid, "تم الأنتهاء من أعداد البوت أستخدامة ")
            
   
    def secondMethod(self,msg,user,pas,courses):
       self.uoload = db.data()
       self.hash = encode.hash1(msg.text)
       
       self.pas1 = encode.encode1(pas,msg.text) 
       
       bot.send_message(self.chid, 'يتم اعداد البوت انتظر')
                
       self.uoload.insertNewUser(self.chid, user, '2', self.pas1, self.hash)
       
      
       self.uoload.insertCoursesIntoTable(courses,self.chid,user)
       bot.send_message(self.chid, "تم الأنتهاء من أعداد البوت تستطيع استخدامه ")
   
    i = 1
    rows = 0
    def printTable(self, chid):

        self.v = db.data()
        table = PrettyTable()
        self.c = self.v.importCourse(chid)
       
        table.title = 'Courses'
       
        table.field_names = ['crse','H','deg']
        self.co = list()
       
        for x in self.c :
            table.add_row([ x[1],x[2],x[3]  ])
            self.co.append(x[4])
        
        # table = from_db_cursor(self.c)
      
        table.hrules = ALL
        
        self.ids = self.v.retrunids(chid)
        self.rows = len(self.ids)
        bot.send_message(chid, '\>\n``` {} ```\n\>'.format(table), parse_mode='MarkdownV2')

   
    def newRate(self, message, chid):
        if self.i <= self.rows:
            global markup

            markup = types.ReplyKeyboardMarkup()
            itembtnap = types.KeyboardButton('A+')
            itembtna = types.KeyboardButton('A')
            itembtnbp = types.KeyboardButton('B+')
            itembtnb = types.KeyboardButton('B')
            itembtncp = types.KeyboardButton('C+')
            itembtnc = types.KeyboardButton('C')
            itembtndp = types.KeyboardButton('D+')
            itembtnd = types.KeyboardButton('D')
            itembtnf = types.KeyboardButton('F')
            markup.row(itembtnap, itembtna)
            markup.row(itembtnbp, itembtnb, itembtncp)
            markup.row(itembtnc, itembtndp, itembtnd)
            markup.row(itembtnf)
            bot.send_message(chid, "توقعاتك لمادة : {} ".format(self.co[self.i - 1]), reply_markup=markup)

            bot.register_next_step_handler(message, self.dealwithCourseTaple)
        if self.i > self.rows:
            markup = types.ReplyKeyboardRemove()
            bot.send_message(chid, "انتهيت من تعيين الدرجات", reply_markup=markup)
            self.uploadrate(message, chid)

    x = list()

    # this function deal with rate of course when ends
    def dealwithCourseTaple(self, message):

        if self.i <= self.rows:

            self.x.append([self.ids[self.i - 1], message.text])
            self.i += 1
            self.newRate(message, message.chat.id)


    # upload rate into data base
    def uploadrate(self, message, chid):
 
        self.y = db.data()
        self.y.insertRate(self.x)
        self.printTable(chid)
        
        self.markup = types.ReplyKeyboardMarkup()
        self.methodOne = types.KeyboardButton('احسب معدلي')
        self.methodTwo = types.KeyboardButton('إعادة تعين الدرجات')
        self.markup.row(self.methodOne, self.methodTwo)
        bot.send_message(chid,'أختر ماذا تريد', reply_markup=self.markup)
        self.x.clear()
        bot.register_next_step_handler(message, self.resetRate)
      
        del self.y

    # calc gpa and make change on rate of courses
    def resetRate(self, msg):
        markup = types.ReplyKeyboardRemove()
     
        if msg.text == 'احسب معدلي':
            bot.send_message(msg.chat.id, "حساب المعدل", reply_markup=markup)
            self.NecessaryInformation(msg,'gpa')
            
           
            # bot.register_next_step_handler(msg , )
        elif msg.text == 'إعادة تعين الدرجات':
            self.d = db.data()
            self.d.cleardeg(msg.chat.id)
            bot.send_message(msg.chat.id, "تمت اعادة التعيين",reply_markup=markup)
        

    
    # If the courses have already been evaluated the now cgange start from here
    def editrate(self, message, chid):

        self.printTable(chid)
        self.i = self.rows + 1
        self.markup = types.ReplyKeyboardMarkup()
        self.methodOne = types.KeyboardButton('احسب معدلي')
        self.methodTwo = types.KeyboardButton('إعادة تعين الدرجات')
        self.markup.row(self.methodOne, self.methodTwo)
        bot.send_message(chid,'أختر ماذا تريد', reply_markup=self.markup)
        bot.register_next_step_handler(message, self.resetRate)
        
    

if __name__ == "__main__":    
   
   
    # while True:
    #     try:
            bot.polling(none_stop=True)
            #ConnectionError and ReadTimeout because of possible timout of the requests library
            #maybe there are others, therefore Exception
        # except Exception:
        #     time.sleep(7)
        #     print("there is erorr")
