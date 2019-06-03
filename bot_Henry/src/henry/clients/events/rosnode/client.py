#!/usr/bin/env python3
"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This file was created/modified by: Jason Cabezuela
"""
from programy.utils.logging.ylogger import YLogger

from programy.clients.events.client import EventBotClient
from henry.clients.events.rosnode.config import ROSnodeConfiguration

import rospy
from std_msgs.msg import String

class ROSnodeClient(EventBotClient):
    
    def __init__(self, argument_parser=None):
        self.running = False
        EventBotClient.__init__(self, "rosnode", argument_parser)
    
    def get_client_configuration(self):
        return ROSnodeConfiguration()
    
    def add_client_arguments(self, parser=None):
        return
    
    def parse_args(self, arguments, parsed_args):
        return
    
    # Write subscriber-code
    def get_question(self, client_context):
        return rospy.wait_for_message(self._subscription, String)

    def display_startup_messages(self, client_context):
        self.process_response(client_context, client_context.bot.get_version_string(client_context))
        initial_question = client_context.bot.get_initial_question(client_context)
        self._renderer.render(client_context, initial_question)

    def process_question(self, client_context, question):
        self._questions += 1
        return client_context.bot.ask_question(client_context , question, responselogger=self)

    def render_response(self, client_context, response):
       # Calls the renderer which handles RCS context, and then calls back to the client to show response
        self._renderer.render(client_context, response)

    def process_response(self, client_context, response):
        self._publisher.publish(response)
        print(response)
        
    def process_question_answer(self, client_context):
        question = self.get_question(client_context)
        print("QUESTION: %s" %question.data)
        response = self.process_question(client_context, question.data)
        self.render_response(client_context, response)

    # This is the Main Loop!
    def wait_and_answer(self):
        try:
            while not rospy.is_shutdown():
                client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
                self.process_question_answer(client_context)
        
        except rospy.ROSInterruptException:
            client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
            self._renderer.render(client_context, client_context.bot.get_exit_response(client_context))
            pass
        
        return False

    def prior_to_run_loop(self):
        self._topic = self._configuration.client_configuration.rostopic
        self._subscription = self._configuration.client_configuration.subscription
        self._publisher = rospy.Publisher(self._topic, String, queue_size=self._configuration.client_configuration.queueSize)
        rospy.init_node(self._configuration.client_configuration.nodename,anonymous=True)
        self._rate = rospy.Rate(self._configuration.client_configuration.rosrate)
        
        client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
        self.display_startup_messages(client_context)


if __name__ == '__main__':

    print("Initiating ROS-Node Client...")

    def run():
        rosnode_app = ROSnodeClient()
        rosnode_app.run()

    run()