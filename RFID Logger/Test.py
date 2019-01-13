##Test
#!/usr/bin/python3.4
import RPi.GPIO as GPIO
import SimpleMFRC522
import xlwt
from time import *
import time
import datetime
import sys
import pdb
import os.path  ##library used to check whether a file already exists or not
import I2C_LCD_driver   ##Import the library for the LCD screen
import xlrd
import shutil ##Imports the library to copy and rename files
import xlutils  #needed to load xl -duncan
from xlutils.copy import copy #used to copy read-only workbook into a writeable
import Write
import Read

mylcd = I2C_LCD_driver.lcd() ##Creates a variable to change and access the LCD screen

##Setup the GPIO 21 & 20 for the button interface
Button = 21
Buzzer = 20
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Buzzer,GPIO.OUT)
GPIO.remove_event_detect(Button)
#############################################################################
##
##This Function will take a string input and display it on the LCD screen.
##
#############################################################################
def DisplayLCD(text, is_cleared = True):
    try:
        mylcd.lcd_clear()
        if len(text) > 32:
            count = int(len(text)/32)    ##Determines the number of sections for the display
            #print count
            for n in range(0,count+4):  ## count equals to 4 is big enough
                mylcd.lcd_display_string(text[15*n:15*(n+1)], 1)## first one is content, second one is row number
                mylcd.lcd_display_string(text[15*(n+1):15*(n+2)],2)
                time.sleep(1)
                if is_cleared == True:
                    mylcd.lcd_clear()
                
        elif len(text) <= 32 and len(text) > 16:
            mylcd.lcd_display_string(text[:16], 1)
            mylcd.lcd_display_string(text[16:], 2)
            time.sleep(1)
            if is_cleared == True:
                mylcd.lcd_clear()
                
        elif len(text) <= 16:
            mylcd.lcd_display_string(text, 1)
            time.sleep(1)
            if is_cleared == True:
                mylcd.lcd_clear()
    except:
        print ("Issue Occured with lcdDisplay(...)")
        lcd_time_reset("LCD ERROR")
    finally:
        return

def ReadCard():
    EmployeeName = Read.read()
    return EmployeeName

def WriteCard(AdminSelect):
    Write.write(AdminSelect)
    return

def MainProgram():
    print("Hello")
    DisplayLCD("Hello",False)
    Press1 = GPIO.wait_for_edge(21, GPIO.RISING, bouncetime = 100)
    print(Press1)
    Press2 = GPIO.wait_for_edge(Button, GPIO.RISING, bouncetime = 100, timeout = 500)
    print(Press2)
    if (Press2 == 21):
        print("Going into write Function....")
        DisplayLCD("Going Into Write Function...")
        DisplayLCD("Please Go To Admin Computer...",False)
        time.sleep(2)
        
        decision = input("Is this an admin?")
    
        if decision == 'N' or decision == 'n':
            WriteCard(False)
            return
        elif decision == 'Y' or decision == 'y':
            WriteCard(True)
            return
    elif (Press2 == None):
        EmployeeName = ReadCard()
    return

while (True):
    MainProgram()
