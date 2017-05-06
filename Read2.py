import time
import RPi.GPIO as GPIO
import MFRC522
import signal

GPIO.setmode(GPIO.BOARD)

LED0    = 7   
LED1    = 11
counter = 0

GPIO.setup(LED0,GPIO.OUT)
GPIO.setup(LED1,GPIO.OUT)


continue_reading = True

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."
while continue_reading:
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    for num in range(0,16):
	#time.sleep(1)
	print num
	# If we have the UID, continue
	if status == MIFAREReader.MI_OK:
	    #print num
	    # Print UID
	    print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
            # This is the default key for authentication
	    key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
	    # Select the scanned tag
	    MIFAREReader.MFRC522_SelectTag(uid)

	    # Authenticate
	    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, num, key, uid)
	    if status == MIFAREReader.MI_OK:
		MIFAREReader.MFRC522_Read(num)
		#MIFAREReader.MFRC522_StopCrypto1()
	        #GPIO.output(LED0,GPIO.HIGH)
	        #time.sleep(0.5)
	        #GPIO.output(LED0,GPIO.LOW)
	    else:
	        print "Authentication error"
	        #GPIO.output(LED1,GPIO.HIGH)
	        #time.sleep(0.5)
	        #GPIO.output(LED1,GPIO.LOW)
	else:
	    print "UID failed"
	time.sleep(0.01)
    #MIFAREReader.MFRC522_StopCryptol()
