"""
This file is for initializing the OOB-Gesture-Publisher with parameters which
were loaded by the config-class on 

This is a quick and dirty solution, bound to be changed at some point.

author: Jason Cabezuela - https://github.com/JCab09/
"""
def init():
    global g_rostopic_gestures
    global g_firstInit
    global g_queueSize
    g_firstInit = True
    g_queueSize = None
    g_rostopic_gestures = None
