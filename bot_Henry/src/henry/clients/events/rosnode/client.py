#!/usr/bin/env python
"""
COPYRIGHT PLACEHOLDER
"""
from programy.utils.logging.ylogger import YLogger

from programy.clients.events.client import EventBotClient
from henry.clients.events.rosnode.config import ConsoleConfiguration

import rospy
from std.msgs.msg import String

class ROSnodeClient(EventBotClient):
    
