#!/usr/bin/env python
# -*- coding: utf-8 -*- 

PKG = 'smart_home_core'
NAME = 'command_server_test'

import unittest
import sys
import rospy, rostest
from smart_home_core.srv import *

class TestCommandServer(unittest.TestCase):

    def test_empty_call(self):
        rospy.wait_for_service('command')
        command = rospy.ServiceProxy('command', Command)
        resp = command('').response.decode('utf-8')
        self.assertTrue(resp.startswith(u'неизвестная команда'))

    def test_wrong_call(self):
        rospy.wait_for_service('command')
        command = rospy.ServiceProxy('command', Command)
        resp = command('unknown').response.decode('utf-8')
        self.assertTrue(resp.startswith(u'неизвестная команда'))

    def test_ok_call(self):
        rospy.wait_for_service('command')
        command = rospy.ServiceProxy('command', Command)
        resp = command('test param').response.decode('utf-8')
        self.assertTrue(resp.startswith('test ok, param:param'))

    def test_time_call(self):
        result = u'Текущее время'
        rospy.wait_for_service('command')
        command = rospy.ServiceProxy('command', Command)

        self.assertTrue(command(u'скажи сколько время').response.decode('utf-8').startswith(result))
        self.assertTrue(command(u'сколько время').response.decode('utf-8').startswith(result))
        self.assertTrue(command(u'который час').response.decode('utf-8').startswith(result))

if __name__ == '__main__':
    rostest.rosrun(PKG, NAME, TestCommandServer, sys.argv)
