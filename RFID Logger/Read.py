#!/usr/bin/env python
import RPi.GPIO as GPIO
import SimpleMFRC522

def read():
        global ReadText
        print("Ready To Scan")
        reader = SimpleMFRC522.SimpleMFRC522()

        try:
                id, ReadText = reader.read()
                print(id)
                print(ReadText)
        finally:
                return ReadText   #returns the name
