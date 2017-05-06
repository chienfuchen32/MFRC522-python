#!/usr/bin/env python

# -*- coding: utf8 -*-


import RPi.GPIO as GPIO

import MFRC522

import signal

import timeit

import time

start = timeit.default_timer()

continue_reading = True



# Capture SIGINT for cleanup when the script is aborted

def end_read(signal,frame):

    global continue_reading

    print "Ctrl+C captured, ending read."

    continue_reading = False

    GPIO.cleanup()



# Hook the SIGINT

signal.signal(signal.SIGINT, end_read)



# Create an object of the class 
MFRC522
MIFAREReader = MFRC522.MFRC522()



# Welcome message

print "Welcome to the MFRC522 card key searching example"

print "Press Ctrl-C to stop."



# This loop keeps checking for chips. If one is near it will get the UID and authenticate

index_key = 0

while continue_reading:

    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)



    # If a card is found

#    if status == MIFAREReader.MI_OK:

#        print "Card detected"

    
# Get the UID of the card

    (status,uid) = MIFAREReader.MFRC522_Anticoll()


    # If we have the UID, continue

    if status == MIFAREReader.MI_OK:


        # Print UID

#        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        
        # This is the default key for authentication

        a = hex(index_key).rstrip("L").lstrip("0x") or "0"

        list_a = list(a)

        str_key = '000000000000'

        list_key = list(str_key)

        for i in range(0, len(list_key)):

            for j in range(0, len(list_a)):

                if(i == len(list_key) - 1 - j):

                    list_key[i] = list_a[j]

        str_key2 = ''

        for i in range(0, len(list_key)):

            str_key2 += list_key[i]

            if i % 2 == 1 and i != len(list_key) - 1:

                str_key2 += ' '

        key = bytearray.fromhex(str_key2)

        #key = [0x00,0x00,0x00,0x00,0x00,0x00]

        
        # Select the scanned tag

        MIFAREReader.MFRC522_SelectTag(uid)


        # Authenticate

        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)


        # Check if authenticated

        if status == MIFAREReader.MI_OK:
	    print index_key
	    print 'auth'
            MIFAREReader.MFRC522_Read(8)

            MIFAREReader.MFRC522_StopCrypto1()
	    break
#        else:

#            print "Authentication error"

	#time.sleep(0.02)
        if index_key < 281474976710655:
            index_key += 1
	    if index_key % 100000 == 0 :
		stop = timeit.default_timer()
		print stop - start, 'sec, ', 'total checked number: ', index_key
	else:
	    print 'end'
	    break

