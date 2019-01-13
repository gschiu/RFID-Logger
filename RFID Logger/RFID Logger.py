#!/usr/bin/python3
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
from xlrd import open_workbook
import shutil ##Imports the library to copy and rename files
import xlutils  #needed to load xl
from xlutils.copy import copy #used to copy read-only workbook into a writeable
import Write
import Read
import calendar

mylcd = I2C_LCD_driver.lcd() ##Creates a variable to change and access the LCD screen

##Setup the GPIO 21 & 20 for the button interface
Button = 21
Buzzer = 20
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Buzzer,GPIO.OUT)

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

def OpenWorkbook(EmployeeData):
    WorkbookName = EmployeeData+str(datetime.date.today().year)+".xls"
    if os.path.exists(WorkbookName):
        rb = xlrd.open_workbook(WorkbookName)
        File = copy(rb)
        return File,rb,WorkbookName
    else:
        print ("File does not exist!")
        DisplayLCD("File does not exist!")
        print ("Creating New Workbook...")
        CreateWorkbook(EmployeeData)
        DisplayLCD("Creating New Workbook...")
        print ("Workbook Created!")
        rb = xlrd.open_workbook(WorkbookName)
        File = copy(rb)
        DisplayLCD("Workbook Created!")
        return File,rb,WorkbookName
    
def CreateWorkbook(EmployeeData):
    wb = xlwt.Workbook()
    for i in range(0,12):
        Month = wb.add_sheet(calendar.month_name[i+1])
        MonthDays = calendar.monthrange(int(datetime.date.today().year),i+1)
        for k in range(1,MonthDays[1]+1):
            if i < 9 and k < 10:
                Month.write(k,0,str(datetime.date.today().year)+"-0"+str(i+1)+"-0"+str(k))
            elif i < 9 and k >= 10:
                Month.write(k,0,str(datetime.date.today().year)+"-0"+str(i+1)+"-"+str(k))
            elif i >= 9 and k < 10:
                Month.write(k,0,str(datetime.date.today().year)+"-"+str(i+1)+"-0"+str(k))
            elif i >= 9 and k >= 10:
                Month.write(k,0,str(datetime.date.today().year)+"-"+str(i+1)+"-"+str(k))
        Month.write(0,0,"Date")
        Month.write(0,1,"Log 1")
        Month.write(0,2,"Log 2")
        Month.write(0,3,"Log 3")
        Month.write(0,4,"Log 4")
        Month.write(0,5,"Hours")
        Month.write(k+1,4,"Total")
        Month.write(0,6,"Overtime")
        Month.write(0,7,EmployeeData)

    wb.save(EmployeeData+str(datetime.date.today().year)+".xls")
    return

def LogHours(EmployeeWorkbook,ReadOnlyCopy,WorkbookName):
    month,day,hour,minute = GetTime()
    WriteSheet = EmployeeWorkbook.get_sheet(int(month)-1)       ##Sheet used for writing new information
    ReadSheet = ReadOnlyCopy.sheet_by_index(int(month)-1)       ##Sheet used for reading previous information

    if (int(minute)<10):
        minute = "0"+minute

    if (ReadSheet.cell(int(day),1).value == ""):
        WriteSheet.write(int(day),1,hour+":"+minute)
    elif (ReadSheet.cell(int(day),2).value == ""):
        WriteSheet.write(int(day),2,hour+":"+minute)
    elif(ReadSheet.cell(int(day),3).value == ""):
        WriteSheet.write(int(day),3,hour+":"+minute)
    elif(ReadSheet.cell(int(day),4).value == ""):
        WriteSheet.write(int(day),4,hour+":"+minute)
    else:
        print("Warning Exceeding log amount! Contact Admin to fix!")
        DisplayLCD("Warning Exceeding log amount! Contact Admin to fix!")

    EmployeeWorkbook.save(WorkbookName)
    return
def CalculateTotal(EmployeeWorkbook,ReadOnlyCopy,WorkbookName):
    month,day,hour,minute = GetTime()
    WriteSheet = EmployeeWorkbook.get_sheet(int(month)-1)       ##Sheet used for writing new information
    ReadSheet = ReadOnlyCopy.sheet_by_index(int(month)-1)       ##Sheet used for reading previous information
    Total = 0
    Overtime = 0

    if (ReadSheet.cell(int(day),1).value != ""):
        Hour1,Minute1 = ReadSheet.cell(int(day),1).value.split(":")
    
    if (ReadSheet.cell(int(day),2).value != ""):
        Hour2,Minute2 = ReadSheet.cell(int(day),2).value.split(":")
        Time1 =float(Hour1)+(float(Minute1)/float(60))
        Time2 =float(Hour2)+(float(Minute2)/float(60))
        Total = round(Time2-Time1,2)
    else:
        return

    if (ReadSheet.cell(int(day),3).value != ""):
        Hour3,Minute3 = ReadSheet.cell(int(day),3).value.split(":")
        Time1 =float(Hour1)+(float(Minute1)/float(60))
        Time2 =float(Hour3)+(float(Minute3)/float(60))
        Total = round(Time2-Time1,2)

    if (ReadSheet.cell(int(day),4).value != ""):
        Hour4,Minute4 = ReadSheet.cell(int(day),4).value.split(":")
        Time1 =float(Hour1)+(float(Minute1)/float(60))
        Time2 =float(Hour4)+(float(Minute4)/float(60))
        Total = round(Time2-Time1,2)
    
    WriteSheet.write(int(day),5,str(Total))

    Overtime = round(Total - 8,2)
    WriteSheet.write(int(day),6,str(Overtime))
    EmployeeWorkbook.save(WorkbookName)

def CalculateGrandTotal(EmployeeWorkbook,ReadOnlyCopy,WorkbookName):
    month,day,hour,minute = GetTime()
    WriteSheet = EmployeeWorkbook.get_sheet(int(month)-1)       ##Sheet used for writing new information
    ReadSheet = ReadOnlyCopy.sheet_by_index(int(month)-1)       ##Sheet used for reading previous information
    MonthDays = calendar.monthrange(int(datetime.date.today().year),int(month))
    GrandTotal = 0
    OvertimeTotal = 0

    
    for k in range(1,MonthDays[1]+1):
        DayTime = ReadSheet.cell(k,5).value
        OverTime = ReadSheet.cell(k,6).value
        if DayTime == '' or DayTime == ' ':
            DayTime = float(0);
        if OverTime == '' or OverTime == ' ':
            OverTime = float(0);
            
        GrandTotal = GrandTotal + float(DayTime)
        OvertimeTotal = OvertimeTotal + float(OverTime)

    WriteSheet.write(k+1,5,str(GrandTotal))
    WriteSheet.write(k+1,6,str(OvertimeTotal))
    EmployeeWorkbook.save(WorkbookName)

    return
def ReadCard():
    EmployeeName = Read.read()
    return EmployeeName

def WriteCard(AdminSelect):
    Write.write(AdminSelect)
    return

def GetTime():
    month = str(datetime.datetime.today().month)
    day = str(datetime.date.today().day)
    hour = str(datetime.datetime.today().hour)
    minute = str(datetime.datetime.today().minute)
    return month,day,hour,minute

def Program():
    GPIO.output(Buzzer,GPIO.HIGH)
    time.sleep(0.05)
    GPIO.output(Buzzer,GPIO.LOW)
    Press2 = GPIO.wait_for_edge(Button, GPIO.RISING, bouncetime = 200, timeout = 500)
    print(Press2)
    if (Press2 == 21):
        GPIO.output(Buzzer,GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(Buzzer,GPIO.LOW)
        print("Going into write Function....")
        DisplayLCD("Going Into Write Function...",False)
        WriteCard(False)
            
    elif (Press2 == None):
        DisplayLCD("Ready to Scan...",False)
        EmployeeName = ReadCard().replace(" ","")
        GPIO.output(Buzzer,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(Buzzer,GPIO.LOW)
        return EmployeeName

def MainProgram():
    GPIO.add_event_detect(21, GPIO.RISING , bouncetime = 200)
    while (True):
        if GPIO.event_detected(21):
            GPIO.remove_event_detect(21)
            EmployeeName = Program()
            return EmployeeName
        month,day,hour,minute = GetTime()
        monthName = calendar.month_name[int(month)]
        DisplayLCD(monthName +" " + day +","+ hour + ":" + minute + " Press to Scan")
while (True):
    EmployeeName = MainProgram()        ##Function returns none if used to write a new card
    if (EmployeeName == None):
        continue
    else:
        EmployeeWorkbook,ReadOnlyCopy,WorkbookName = OpenWorkbook(EmployeeName)      ##OpensWorkbook
        LogHours(EmployeeWorkbook,ReadOnlyCopy,WorkbookName)
        time.sleep(0.5)
        EmployeeWorkbook,ReadOnlyCopy,WorkbookName = OpenWorkbook(EmployeeName)      ##OpensWorkbook
        CalculateTotal(EmployeeWorkbook,ReadOnlyCopy,WorkbookName)
        time.sleep(0.5)
        EmployeeWorkbook,ReadOnlyCopy,WorkbookName = OpenWorkbook(EmployeeName)      ##OpensWorkbook
        CalculateGrandTotal(EmployeeWorkbook,ReadOnlyCopy,WorkbookName)
