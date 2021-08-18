import time
import telebot 
import os
from cryptography.fernet import Fernet
import rncryptor
import cryptocode
from hashlib import sha256

# cipher_suite = Fernet(key)
# #encoded_text = cipher_suite.encrypt(b"Hello stackoverflow!")
# decoded_text = cipher_suite.decrypt(b'gAAAAABg0tFMMP6mVqfGt9t6ZBEjBu1ntiwegsl6gDRsEnKKRq7q-eEXHVXmTKLDh7PK2r9QKDOX7FCLHbIiL-QlWDaUBsckgWZskus5Kdapglwt6qkJzvg=')

# print(decoded_text)


def  encode1 (pas,key=''):
    Gkey = 'xBaneXUu5YAh4yXDwO2Y0PjcvEjuyXLoRLwF4_yb5pg=%s'%key
    

    encoded = cryptocode.encrypt(pas,Gkey)
  
    return(encoded)
    

def decode1(pas,key=''):
    try :
        Gkey = 'xBaneXUu5YAh4yXDwO2Y0PjcvEjuyXLoRLwF4_yb5pg=%s'%key
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
