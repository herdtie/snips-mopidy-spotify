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

        # Tell mopidy to start playing "Die Moldau" by Smetana
        #self.mopidy.play_single_track('spotify:track:6y51eybZuc4Jv8bXbL3d9K')
        # Vivaldi, first
        #self.mopidy.play_single_track('spotify:track:4js8kCJgiQJ0suhau4ZbTh')
        # zauberlehrling: spotify:track:26Ko7pSCJ1lV5NOtIhsocy
        # Vivaldi, 4 seasons album (not the fast one)
        self.mopidy.play_single_track('spotify:album:1unTNtXCpPRaKH4u24nrcl')

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "Ok", "")
    # --> Sub callback function, one per intent


    def play_zauberlehrling(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        self.mopidy.play_single_track('spotify:track:26Ko7pSCJ1lV5NOtIhsocy')

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "Ok", "")


    def stop_music_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        # Tell mopidy to stop_music_callback
        self.mopidy.stop()


    def volume_up_callback(self, hermes, intent_message):
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        # Get volume
        volume = self.mopidy.get_volume()

        new_vol = min(100, volume+20)
        self.mopidy.set_volume(new_vol)
        hermes.publish_start_session_notification(intent_message.site_id, u"Lautsẗarke jetzt bei {} Prozent".format(new_vol), "")


    def volume_down_callback(self, hermes, intent_message):
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        # Get volume
        volume = self.mopidy.get_volume()

        new_vol = max(0, volume-20)
        self.mopidy.set_volume(new_vol)
        hermes.publish_start_session_notification(intent_message.site_id, u"Lautsẗarke jetzt bei {} Prozent".format(new_vol), "")


    def intent_warum_callback(self, hermes, intent_message):
        ## terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        ## action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        ## if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "warum ist die Banane krumm? weil keiner in den Urwald zog und sie wieder grade bog", "")


    def intent_milan_callback(self, hermes, intent_message):
        ## terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        ## action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        ## if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id,
                "Hallo Milan, wir freuen uns dass du da bist. Herzlich Willkommen!", "")

    # More callback function goes here...

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name

        if coming_intent == 'herdtie:Musik' :
            self.play_music_callback(hermes, intent_message)
        if coming_intent == 'herdtie:zauberlehrling' :
            self.play_zauberlehrling(hermes, intent_message)
        elif coming_intent == 'herdtie:MusikStop':
            self.stop_music_callback(hermes, intent_message)
        elif coming_intent == 'herdtie:MusikVolumeUp':
            self.volume_up_callback(hermes, intent_message)
        elif coming_intent == 'herdtie:MusikVolumeDown':
            self.volume_down_callback(hermes, intent_message)
        elif coming_intent == 'herdtie:Warum':
            self.intent_warum_callback(hermes, intent_message)
        elif coming_intent == 'herdtie:HalloMilan':
            self.intent_milan_callback(hermes, intent_message)

        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    MusicApp()
