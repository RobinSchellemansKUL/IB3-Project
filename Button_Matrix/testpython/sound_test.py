import os
import time

path = 'home/pi'

isExist = os.path.exists(path)

if not isExist:
    os.makedirs(path)
    print("The new directory is created.")
    os.system('chmod 777 -R /home/pi/sounds')

burp = '/home/pi/gitaarstuk2.wav'

isExist = os.path.exists(burp)

if not isExist:
    os.system('wget http://rpf.io/burp -O burp.wav')
    print("Sound has been downloaded.")

os.system('aplay ' + burp)

