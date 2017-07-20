import os
import pika
import sys
from time import sleep


DEBUG = int(os.environ.get('DEBUG', 0))


# MESSAGE BROKER
BROKER_HOST = os.environ.get('BROKER', 'non-existent-broker')
BROKER_USER = os.environ.get('BROKER_USER', 'guest')
BROKER_PASSWORD = os.environ.get('BROKER_PASSWORD', 'guest')


MSG_2_SEND = os.environ.get('MSG_2_SEND', '1337')
MSG_2_SEND = int(MSG_2_SEND)
MSG = os.environ.get('MSG', 'Default message')
QUEUE = os.environ.get('QUEUE', 'default')

if DEBUG == 1:
  print("env:", DEBUG, MSG_2_SEND, MSG, QUEUE)
  


# Fallback logic - we can't predict when Rabbit is online 
fallback_counter = 0
notConnected = True

while notConnected and fallback_counter < 10 :
  try:
    print("Connecting to", BROKER_HOST, BROKER_USER, BROKER_PASSWORD, QUEUE)
    connection = pika.BlockingConnection(pika.ConnectionParameters(BROKER_HOST))
    notConnected = False
  except:
    print("Can't connect to {0}".format(BROKER_HOST))
    fallback_counter += 1

    if fallback_counter == 10:
      print("Exiting...")
      sys.exit(1)

    secondsToWait = fallback_counter * 10
    print("Waiting {0} seconds for broker coming online...".format(secondsToWait))
    sleep(secondsToWait)



    
channel = connection.channel()
print("Connected to", BROKER_HOST)
sleep(3)

channel.queue_declare(queue=QUEUE)
print("Sending {0} messages".format(MSG_2_SEND))

for i in range(0,MSG_2_SEND):
  channel.basic_publish(exchange='', routing_key=QUEUE, body='{0} {1}'.format(i, MSG))
                      
if DEBUG == 1:
  print(" [{0}] Sent {1}".format(i, MSG))

connection.close()

print("Closing connection to", BROKER_HOST)
print("End of my job here, exiting.")