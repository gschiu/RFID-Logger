#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import datetime

def write(admin = False):
        global text
        reader = SimpleMFRC522.SimpleMFRC522()
        try:
                if admin == False:
                        text = input('Please input employee name Eg. John S:')
                        
                        print("Now place your tag to write")
                        reader.write(text)
                        
                        clock = datetime.datetime.today()
                        print ("Current date and time of writing")
                        print (clock.strftime("%Y-%m-%d %H:%M"))
                elif admin == True:
                        text = input('Please input employee name Eg. John S:')
                        card = text + " *Admin*"
                        print("Now place your tag to write")
                        reader.write(card)
                        
                        clock = datetime.datetime.today()
                        print ("Current date and time of writing")
                        print (clock.strftime("%Y-%m-%d %H:%M"))
        finally:
                return
