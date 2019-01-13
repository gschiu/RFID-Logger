#!/usr/bin/python
import I2C_LCD_driver
from time import *
import time
mylcd = I2C_LCD_driver.lcd()
text = 'Dank memes on this thing: one does not simply make an LCD screen work properly \(^_^)/'
while True:
    if len(text) > 32:
        count = len(text)/32    ##Determines the number of sections for the display
        print count
        for n in range(0,count+4):
            mylcd.lcd_display_string(text[15*n:15*(n+1)], 1)
            mylcd.lcd_display_string(text[15*(n+1):15*(n+2)],2)
            time.sleep(3)
            mylcd.lcd_clear()
            
    elif len(text) < 32 and len(text) > 16:
        mylcd.lcd_display_string(text[:15], 1)
        mylcd.lcd_display_string(text[15:],2)
        time.sleep(3)
        mylcd.lcd_clear()
        time.sleep(3)
    elif len(text) < 16:
        mylcd.lcd_display_string(text, 1)
        time.sleep(3)
        mylcd.lcd_clear()
        time.sleep(3)
