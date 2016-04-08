__author__ = 'stevenchun'
import speech_recognition as sr
from wolfram_class import *
import pyvona
import pyglet
#import pygame

#again you'll need an APPID from wolfram alpha here.
appid = "############"

#r = sr.Recognizer()
#m = sr.Microphone()
#m.SAMPLE_RATE = 48000

# this is a ugly little function I had to write to use pyglet properly. On my raspberry PI I use pygame
# and it's much better. This kept giving me an error about how many arguments "exiter" was taking until I just gave
# it a random argument to take. But at least it works.
class Winston:

    def __init__(self, woken = False):
        self.woken = woken


    def exiter(self, dt):
        pyglet.app.exit()

    def activate(self):
        r = sr.Recognizer()
        m = sr.Microphone()
        m.SAMPLE_RATE = 48000
        try:
            print("A moment of silence, please...")
            with m as source:r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
            # create the IVONA voice
            #winston = pyvona.create_voice("GDNAJRUJP55AJ25DGUPA", "MXlt+SAWMs6ZUE4rRmq2e8LbhWIISuBpuJmi5sWV")
            #winston.codec = "mp3"
            print winston_voice.codec
            while True:
                print("Say something!")
                #fixed
                with m as source: audio = r.listen(source, 10)
                print("Got it! Now to recognize it...")
                try:
                    # recognize speech using Google Speech Recognition
                    value = r.recognize_google(audio)

                    #we need some special handling here to correctly print unicode characters to standard output
                    #I have python 2 so this is the one I'm probably using

                    if str is bytes: # this version of Python uses bytes for strings (Python 2)
                        # instead of printing value, store it, and send it over to wolfram alpha
                        value = value.encode("utf-8")
                        print value

                        #get the answer from Wolfram's returned XML document. The implementation of this is
                        #hideous. I don't even know what an XML is. I just kept on iterating mannn.
                        answer = ask_wolfram(value, appid)

                        #creates an audio.mp3 file storing the audio of IVONA saying the answer
                        winston_voice.fetch_voice(answer, "audio.mp3")


                        #plays the audio. Uuuuuugly.
                        speech = pyglet.media.load("audio.mp3", streaming = False)
                        speech.play()

                        pyglet.clock.schedule_once(self.exiter, speech.duration)
                        pyglet.app.run()


                        # Put Winston back to sleep
                        self.woken = False


                    else: # this version of Python uses unicode for strings (Python 3+)
                        print("You said {}".format(value))

                except sr.UnknownValueError:
                    print("Oops! Didn't catch that")
                except sr.RequestError as e:
                    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
                #except IOError:
                    #pass
                except sr.WaitTimeoutError:
                    pass

        except KeyboardInterrupt:
            pass
        #except IOError:
            #pass

    def wake(self):
        r = sr.Recognizer()
        m = sr.Microphone()
        m.SAMPLE_RATE = 48000
        try:
            print("A moment of silence, please...")
            with m as source: r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
            # create the IVONA voice
            #winston = pyvona.create_voice("GDNAJRUJP55AJ25DGUPA", "MXlt+SAWMs6ZUE4rRmq2e8LbhWIISuBpuJmi5sWV")
            #winston.codec = "mp3"
            print winston_voice.codec
            while True:
                print("Say something!")
                with m as source: audio = r.listen(source, 3)
                print("Got it! Now to recognize it...")
                try:
                    # recognize speech using Google Speech Recognition
                    wake = r.recognize_google(audio)

                    #we need some special handling here to correctly print unicode characters to standard output
                    #I have python 2 so this is the one I'm probably using

                    if str is bytes: # this version of Python uses bytes for strings (Python 2)
                        # instead of printing value, store it, and send it over to wolfram alpha
                        wake = wake.encode("utf-8")
                        print wake

                        if wake.lower() == "winston":
                            winston_voice.fetch_voice("Yes, sir?", "confirm.mp3")
                            speech = pyglet.media.load("confirm.mp3", streaming = False)
                            speech.play()

                            pyglet.clock.schedule_once(self.exiter, speech.duration)
                            pyglet.app.run()

                            #Wake Winston up so that he will try to answer whatever is next said

                            self.woken = True


                    else: # this version of Python uses unicode for strings (Python 3+)
                        print("You said {}".format(wake))

                except sr.UnknownValueError:
                    print("Oops! Didn't catch that")
                except sr.RequestError as e:
                    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
                #except IOError:
                    #pass
                except sr.WaitTimeoutError:
                    pass

        except KeyboardInterrupt:
            pass
        #except IOError:
            #pass
        except sr.WaitTimeoutError:
            pass

w = Winston()

winston_voice = pyvona.create_voice("GDNAJRUJP55AJ25DGUPA", "MXlt+SAWMs6ZUE4rRmq2e8LbhWIISuBpuJmi5sWV")
winston_voice.codec = "mp3"
winston_voice.voice_name = 'Brian'


while True:
    w.wake()
    if w.woken == True:
        w.activate()

