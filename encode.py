import time
import telebot 
import os
from cryptography.fernet import Fernet
import rncryptor
import cryptocode
from hashlib import sha256


def  encode1 (pas,m1=''):
    key = os.environ.get("ewsd4")

    Gkey = key+m1
    

    encoded = cryptocode.encrypt(pas,Gkey)
  
    return(encoded)
    

def decode1(pas,m1=''):
    try :
        Gkey = key+m1
        
        decoded = cryptocode.decrypt(pas, Gkey)
        return(decoded)
        
    except Exception:
        return "erorr" 
    
    
 
def hash1(p):
       h = sha256()
       str_as_bytes = str.encode(p)
       h.update(str_as_bytes)
       hash = h.hexdigest()
       return hash
