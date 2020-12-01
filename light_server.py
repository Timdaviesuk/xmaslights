#import RPi.GPIO as GPIO
import time
import csv
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__)

################
# GPIO Methods #
################

channel_1 = 11
channel_2 = 13
channel_3 = 15
channel_4 = 16
channel_5 = 18
channel_6 = 22
channel_7 = 29
channel_8 = 31

channels = [channel_1, channel_2, channel_3, channel_4, channel_5, channel_6, channel_7, channel_8]
channel_states = [0, 0, 0, 0, 0, 0, 0, 0]

sequences = ["test.csv", "chasing.csv"]

sequence_running = False

def gpio_setup():
    # use PHYSICAL GPIO Numbering
    GPIO.setmode(GPIO.BOARD)

    # By default, set all to be output and on
    for channel in channels:
        GPIO.setup(channel, GPIO.OUT)
        set_gpio(channel, "1")

def run_sequence(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            print(row)
            wait = float(row.pop())

            for channel, signal in enumerate(row):
                set_gpio(channel, signal)
                print("in_sequence")

            time.sleep(wait)

def set_gpio(channel, signal):
    channel_s = channels[channel]
    sig = bool(float(signal))
    if sig == True:
        print("Turn on  " + str(channel))
        #GPIO.output(channel_s, GPIO.LOW)
    else:
        print("Turn off " + str(channel))
        #GPIO.output(channel_s, GPIO.HIGH)

def destroy():
    GPIO.cleanup()                     # Release all GPIO

#####################
# Web API Endpoints #
#####################

# Set an individual light
@app.route('/api/light/<id>')
def set_light(id):
    channel = int(id)
    signal = request.args.get('signal')
    set_gpio(channel, signal)
    return jsonify({"result":True})

# Start running a sequence. This is WIP, need to implement running a sequence in a seperate process
# that I can kill when any other action comes in.
@app.route('/api/sequence/<id>')
def set_sequence(id):
    sequence = sequences[int(id)]
    # print("Run sequence:" + str(sequence))
    run_sequence(sequence)
    return jsonify({"result":True})

# Loads the index.html. All other pages are served from the default static folder.
@app.route('/')
def main_page():
    return render_template("index.html")

###################
# App starts here #
###################
if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    # Set up the GPIO
    print('Set up the GPIO')
    #gpio_setup()
    
    print('Start the web server')
    app.run(host='0.0.0.0',port=2801)