#!/usr/bin/env python3
"""This file utilizes Program-Y's default OutOfBandProcessor
It implents the OutOfBand-ROSpublisher for the inMoov-Gestures which are called by the AIML-files of the bot.

Author: Jason Cabezuela - https://github.com/JCab09/
"""

import rospy
from std_msgs.msg import String
import xml.etree.ElementTree as ET
import henry.oob.settings.gestures as gestSettings
from programy.oob.defaults.oob import OutOfBandProcessor

class inMoovOutOfBandProcessor(OutOfBandProcessor):
    """
    <oob>
        <mrl>
            <service>service</service>
            <method>method</method>
            <param>parameter</param>
        </mrl>
    </oob>
    """
    def __init__(self):
        OutOfBandProcessor.__init__(self)
        self._pub = rospy.Publisher(gestSettings.g_rostopic_gestures, String, queue_size=gestSettings.g_queueSize)

        self._service = None
        self._method = None
        self._parameter = None

    def parse_oob_xml(self, oob: ET.Element):
        """This method extracts the values from the OOB-Element contained in the AIML-files"""
        if oob is not None:
            for child in oob:
                if child.tag == 'service':
                    self._service = child.text
                elif child.tag == 'method':
                    self._method = child.text
                elif child.tag == 'param':
                    self._parameter = child.text
            return True
        return False

    def execute_oob_command(self, client_context):
        """This method gets called if the previous method was successful"""
        message = String()
        message.data = self._parameter
        self._pub.publish(message)
        print("---OOB PUBLISHED Message.data \"%s\" under ROStopic \"%s\"---" %(message.data, gestSettings.g_rostopic_gestures))
        return ""
