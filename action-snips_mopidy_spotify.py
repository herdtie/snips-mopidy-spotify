#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
from subprocess import Popen

from http_mopidy import HttpMopidy

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class MusicApp(object):
    """Class used to wrap action code with mqtt connection
        
        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        self.mopidy = HttpMopidy()

        # start listening to MQTT
        self.start_blocking()
        
    # --> Sub callback function, one per intent
    def play_music_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        with open('/tmp/snips-mopidy-spotify-2', 'wt') as writer:
            writer.write('test2')

        # Tell mopidy to start playing "Die Moldau" by Smetana
        #self.mopidy.play_single_track('spotify:track:6y51eybZuc4Jv8bXbL3d9K')
        # Vivaldi, first
        #self.mopidy.play_single_track('spotify:track:4js8kCJgiQJ0suhau4ZbTh')
        # Vivaldi, 4 seasons album
        self.mopidy.play_single_track('spotify:album:4h7BsBugLjCCyCY1vfAPAR')

        with open('/tmp/snips-mopidy-spotify-3', 'wt') as writer:
            writer.write('test3')

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "Ok", "")

        with open('/tmp/snips-mopidy-spotify-4', 'wt') as writer:
            writer.write('test4')


    def intent_warum_callback(self, hermes, intent_message):
        ## terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        ## action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        ## if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "warum ist die Banane krumm? weil keiner in den Urwald zog und sie wieder grade bog", "")

    # More callback function goes here...

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        with open('/tmp/snips-mopidy-spotify', 'wt') as writer:
            writer.write('test')
            writer.write(str(intent_message))
            writer.write(coming_intent)

        if coming_intent == 'herdtie:Musik' :
            self.play_music_callback(hermes, intent_message)
        if coming_intent == 'herdtie:Warum':
            self.intent_warum_callback(hermes, intent_message)

        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    MusicApp()
