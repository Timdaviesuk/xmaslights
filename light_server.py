#import RPi.GPIO as GPIO
import time
import csv
import json
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__)

# Class representing a light
class Light:    
    def __init__(self, id, name, channel):
        self.id = id
        self.name = name
        self.channel = channel
        self.state = False

################
# GPIO Methods #
################

lights = [Light(0, "Train", 11),
    Light(1, "Snowman", 13),
    Light(2, "Motorbike santa",15),
    Light(3, "Christmas trees", 16),
    Light(4, "Silouthette santa", 18),
    Light(5, "Sleigh", 22),
    Light(6, "Candy canes", 29),
    Light(7, "Icicles", 31)
]

sequences = ["test.csv", "chasing.csv"]

sequence_running = False

def gpio_setup():
    # use PHYSICAL GPIO Numbering
    GPIO.setmode(GPIO.BOARD)

    # By default, set all to be output and on
    for light in lights:
        GPIO.setup(light.channel, GPIO.OUT)
        set_gpio(light.channel, "1")

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

def set_gpio(light, signal):
    if signal == True:
        print("Turn on  " + str(light.channel))
        #GPIO.output(light.channel, GPIO.LOW)
    else:
        print("Turn off " + str(light.channel))
        #GPIO.output(light.channel, GPIO.HIGH)

    light.state = signal

def destroy():
    GPIO.cleanup()                     # Release all GPIO

#####################
# Web API Endpoints #
#####################

def obj_dict(obj):
    return obj.__dict__

# Get the list of lights
@app.route('/api/lights')
def get_lights():
    return json.dumps(lights, default=obj_dict)

# Set an individual light
@app.route('/api/lights/<id>')
def set_light(id):
    light = next((l for l in lights if l.id == int(id)), None)
    signal = request.args.get('signal')
    signal1 = bool(float(signal))
    set_gpio(light, signal1)
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