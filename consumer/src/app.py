import os
import pika
import sys
from time import sleep

DEBUG = int(os.environ.get('DEBUG', 0))
QUEUE = os.environ.get('QUEUE', 'default')

if DEBUG == 1:
  print("env:", DEBUG, QUEUE)

# MESSAGE BROKER
BROKER_HOST = os.environ.get('BROKER', 'non-existent-broker')
BROKER_USER = os.environ.get('BROKER_USER', 'guest')
BROKER_PASSWORD = os.environ.get('BROKER_PASSWORD', 'guest')

def callback(ch, method, properties, body):
  if DEBUG == 1:
    print(" [x] Received %r from %s" % (body, QUEUE))

def consume(connection):
  channel = connection.channel()

  channel.queue_declare(queue=QUEUE)
  channel.basic_consume(callback,
                        queue=QUEUE,
                        no_ack=True)
  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()

  connection.close()

  print("End of my job here. Closing connection to", BROKER_HOST)


# Fallback logic - we can't predict when Rabbit is online 
fallback_counter = 0
notConnected = True

while notConnected and fallback_counter < 10 :
  try:
    print("Connecting to", BROKER_HOST, BROKER_USER, BROKER_PASSWORD, QUEUE)
    connection = pika.BlockingConnection(pika.ConnectionParameters(BROKER_HOST))
    notConnected = False
    consume(connection)

  except:
    notConnected = True
    print("Can't connect to {0}".format(BROKER_HOST))
    fallback_counter += 1

    if fallback_counter == 10:
      print("Exiting...")
      sys.exit(1)

    secondsToWait = fallback_counter * 10
    print("Waiting {0} seconds for broker comming online...".format(secondsToWait))
    sleep(secondsToWait)

