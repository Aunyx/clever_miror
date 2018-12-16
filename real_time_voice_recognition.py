#!/usr/bin/env python
"""
This node does on device voice recognition using PyAudio to capture
the sound data and pocket sphinx to transcript it into text
"""
import os
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import pyaudio

#sphinx_files_path
sphinx_files_path= os.path.join('sphinx_files')

class VoiceCmd:
    def __init__(self):
        #initialize PyAudio to stream data from the mic to the pocketsphinx decoder
        p = pyaudio.PyAudio()
        #The decoder works with an input rate of 16000HZ, mono, 16bits, little endian
        #The buffer has to be long enough to contain an answer ("yes please" or "no thank you")
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=16000)
        #Check that there are audio devices that can be used to record sound
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print "Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name')

        #start picking mic data
        stream.start_stream()

        # initialize pocketsphinx
        global sphinx_files_path
        config = Decoder.default_config()
        #provide a model of the language you want to use
        config.set_string('-hmm',str(os.path.join(sphinx_files_path, 'en-us')))
        #A dictionnary that contains the relation between the sound that are recognized and the text to write
        config.set_string('-dict', str(os.path.join(sphinx_files_path, 'yes_please_no_thank_you.dic')))
        #A compilation of the possible sentences
        config.set_string('-lm', str(os.path.join(sphinx_files_path, 'yes_please_no_thank_you.lm')))
        #Suppress some of the output of pocketsphinx
        config.set_boolean('-verbose', False)
        self.decoder = Decoder(config)
        self.decoder.start_utt()

        #the decoder is running, we just have to feed him with data
        while not rospy.is_shutdown():
            buf = stream.read(16000)#1 seconds buffer
            if buf: #if there is something to decode
                #process it using the above configuration
                self.decoder.process_raw(buf,
                                        False,
                                        False)
            else:
                break
            self.parse_result() # Check what the decoder picked up

    #parse the result from the decoder
    def parse_result(self):
        if self.decoder.hyp() != None: #if the decoder recognized something
            words = []
            #visualize the result of the decoder
            print("###############################################")
            for seg in self.decoder.seg():
                print (seg.word, seg.prob, seg.start_frame, seg.end_frame)
                words.append(seg.word)
            print("###############################################")

            #publish on the topic if somethin useful as been picked
            if 'YES' in words and 'PLEASE' in words:
                print("recognized YES PLEASE")

            elif ('NO' in words or 'YOU' in words) and 'THANK' in words :"
                print("recognized NO THANK YOU")

            # the data has been already processed, and the decoder had some hypothesis,
            # erase the previous hypothesis
            # and start the recognition using the next set of data
            self.decoder.end_utt()
            self.decoder.start_utt()
        #if the decoder didn't recognized anything in the previous set of data,
        # feed it with more data from the next buffer content until
        #it recognizes something

    def shutdown(self):
        rospy.sleep(1)

if __name__ == '__main__':
    VoiceCmd()
