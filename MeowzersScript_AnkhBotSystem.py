#---------------------------------------
#	Import Libraries
#---------------------------------------
import os
import codecs
import json
import time
import random
from collections import deque

#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "Meowzers"
Website = "http://dtkiddin.io"
Description = "Bot randomly meows to a viewer in chat and plays a cute meow sound!"
Creator = "DTkiddin"
Version = "1.1.0.0"

#---------------------------------------
#	Set Variables
#---------------------------------------
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
AudioFilesPath = os.path.join(os.path.dirname(__file__), "audio")
AudioPlaybackQueue = deque()

#---------------------------------------
# Classes
#---------------------------------------
class Settings(object):
    """ Load in saved settings file if available else set default values. """
    def __init__(self, settingsfile=None):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        except:
                self.respond_message = "/me meows at $randuser"
                self.channel_chance = 33.0
                self.announcer_timer = 5.0
                self.volume_sound = 100.0
                self.file_sound = "meow.mp3"

    def reload(self, jsondata):
        """ Reload settings from Chatbot user interface by given json data. """
        self.__dict__ = json.loads(jsondata, encoding="utf-8")
        return

    def save(self, settingsfile):
        """ Save settings contained within to .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save settings to file.")
        return

#---------------------------------------
#	Functions
#---------------------------------------
def EnqueueAudioFile(audiofile):
	""" Adds an audio file from the audio folder to the play queue. """
	fullpath = os.path.join(AudioFilesPath, audiofile)
	AudioPlaybackQueue.append(fullpath)
	return

def ParameterRandUser(parseString, randUser):
	if "$randuser" in parseString:
		return parseString.replace("$randuser", randUser)
	return parseString

def PlayTestAudio():
    EnqueueAudioFile(ScriptSettings.file_sound)
    return

#---------------------------------------
#	[Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
    """
        Init is a required function and is called the script is being loaded into memory
        and becomes	active. In here you can initialize any data your script will require,
        for example read the settings file for saved settings.
    """

    # Globals
    global ScriptSettings
    global LastRunTime

    # Load in saved settings
    ScriptSettings = Settings(SettingsFile)
    # Set LastRunTime to now
    LastRunTime = time.time()

    # End of Init
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsondata):

    """
        ReloadSettings is an optional function that gets called once the user clicks on
        the Save Settings button of the corresponding script in the scripts tab if an
        user interface has been created for said script. The entire Json object will be
        passed to the function	so you can load that back	into your settings without
        having to read the newly saved settings file.
    """

    # Globals
    global ScriptSettings

    # Reload newly saved settings
    ScriptSettings.reload(jsondata)

    # End of ReloadSettings
    return

#---------------------------------------
#	[Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    """
        Execute is a required function that gets called when there is new data to be
        processed. Like a Twitch or Discord chat messages or even raw data send from
        Twitch IRC.	This function will _not_ be called when the user disabled the script
        with the switch on the user interface.
    """
    return


#---------------------------------------
#	[Required] Tick Function
#---------------------------------------
def Tick():
    """
        Tick is a required function and will be called every time the program progresses.
        This can be used for example to create simple timer if you want to do let the
        script do something on a timed basis.This function will _not_ be called	when the
        user disabled the script	with the switch on the user interface.
    """
    # Only run check if it's been more than the announcer_timer limit since the LastRunTime
    if LastRunTime + (ScriptSettings.announcer_timer*60) <= time.time():
    #if LastRunTime + (5) <= time.time(): #For testing purposes
        # Globals
        global LastRunTime

        #Check if the bot needs to meows to the channel owner of a viewer
        if Parent.GetRandom(0,100) <= ScriptSettings.channel_chance:
            Parent.SendTwitchMessage(ParameterRandUser(ScriptSettings.respond_message, Parent.GetChannelName()))
        else:
            #Get a random viewer that has being active in the past 15 minutes and send the respond message into chat
            randUser = Parent.GetRandomActiveUser()
            #If that random user is specific that user we want to do something first, else we just meow
            if randUser == "ocb_silverback":
                #If we want to block the meow to that specific user, the channel owner gets the meow, else the viewer still gets it
                if ScriptSettings.silverback_nomeow:
                    Parent.Log(ScriptName, "Blocked the meow!")
                    Parent.SendTwitchMessage(ParameterRandUser(ScriptSettings.respond_message, Parent.GetChannelName()))
                else:
                    Parent.SendTwitchMessage(ParameterRandUser(ScriptSettings.respond_message, randUser))
            else:
                Parent.SendTwitchMessage(ParameterRandUser(ScriptSettings.respond_message, randUser))

            #Get a viewer user in chat and send the respond message into chat
            #randUser = Parent.GetViewerList()
            #Parent.SendTwitchMessage(ParameterRandUser(ScriptSettings.respond_message, random.choice(randUser)))

        #Queue sound
        PlayTestAudio()

        # Set new timestamp
        LastRunTime = time.time()

    # Audio file in the queue?
	if AudioPlaybackQueue:
		# Try to playback left most item in queue
		if Parent.PlaySound(AudioPlaybackQueue[0], (ScriptSettings.volume_sound/100.0)):
			# Pop from queue if has been played
			AudioPlaybackQueue.popleft()

    return
