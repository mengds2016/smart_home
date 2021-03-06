#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy
import json
import codecs
import uuid
import shlex,subprocess,os
from std_msgs.msg import String
from smart_home_core.srv import *
from smart_home_core.msg import Notification

class recognizer(object):

    def __init__(self):
        self.name = 'железяка'
   #    global pub
        pub = rospy.Publisher('notification', Notification)
        rospy.init_node('recognizing_node')

        dic_file_path  = rospy.get_param('~dictionary','russian.dic')
        dic_file = codecs.open(dic_file_path, 'r', 'utf-8')
        try:
            self.dictionary = json.load(dic_file)
            dic_file.close()
        except:
            err = 'Please specify a dictionary file properly'
            print err
            rospy.logerr(err)
            return
        try:
            self.name = rospy.get_param('~name')
        except:
            rospy.logerr('name not specified, using default: '+self.name)
        # subscribe to the pocketsphinx output    
        #rospy.Subscriber('/recognizer/output', String, self.on_speech)
        rospy.wait_for_service('command');
        self.command = rospy.ServiceProxy('command', Command)
        pub.publish(Notification(str(uuid.uuid1()), "Модуль распознавания речи запущен.", 0, "voice,log", "", ()))

    def translate(self, msg):
        result = msg.decode('utf-8')
        for (transl, keywords) in self.dictionary.iteritems():
            for keyword in keywords:
                result = result.replace(keyword, transl)
        return result

    def on_speech(self, msg):
        # find nickname
        start = msg.data.find(self.name);
        if start > -1:
            # string after name
            st = msg.data[start + len(self.name):]
            #translate it, using dictionary
            st = self.translate(st.strip())
            rospy.loginfo(st.encode('utf-8'))
            try:
                resp1 = self.command(st)
            except rospy.ServiceException, e:
                rospy.logerror("Service call failed: %s"%e)

    def recognizing(self):
        google_args = shlex.split('wget -q -U "Mozilla/5.0" --post-file recording.flac --header="Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v1/recognize?lang=ru-RU&client=chromium"')
        # rec sound
        try:
            os.system('sox -t alsa default recording.wav silence 1 0.1 5% 1 1.5 5% trim 0 10')
            os.system('sox recording.wav recording.flac rate 16000')
            #subprocess.call(rec_args)
        except:
            rospy.logerr('error recording sound')
        #print 'recognizing'
        output,error = subprocess.Popen(google_args,stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
        if not error and len(output)>16:
            a = eval(output)
            text = String(a['hypotheses'][0]['utterance'])
            rospy.loginfo(text)
            return text
        else:
            if error:
                rospy.logerror('error recognizing: ' + error)
            else:
                rospy.logerror('not recognized: ' + output)

if __name__=="__main__":
    r = recognizer()
    rospy.sleep(2)
    while not rospy.is_shutdown():
        text = r.recognizing()
        if text:
            r.on_speech(text)
