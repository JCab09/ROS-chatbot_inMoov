#!/usr/bin/env python3
"""
This file holds the ROSnode-Client
It contains the __main__() method and is responsible for handling the input-ouput process of the chatbot.

The design of this file is heavily influenced by Keith Sterling's Program-Y console client.
For further information on the chatbot engine check out: https://github.com/keiffster/program-y

Author: Jason Cabezuela - https://github.com/JCab09/
"""
from programy.utils.logging.ylogger import YLogger

from programy.clients.events.client import EventBotClient
from henry.clients.events.rosnode.config import ROSnodeConfiguration
import henry.oob.settings.gestures as gestSettings

import rospy
from std_msgs.msg import String

class ROSnodeClient(EventBotClient):

    def __init__(self, argument_parser=None):
        print("Initiating ROS-Node Client...")
        self.running = False
        EventBotClient.__init__(self, "rosnode", argument_parser)

    def get_client_configuration(self):
        return ROSnodeConfiguration()

    def add_client_arguments(self, parser=None):
        return

    def parse_args(self, arguments, parsed_args):
        return

    def get_question(self, client_context):
        """Wait for new message"""
        return rospy.wait_for_message(self._subscription, String)

    def display_startup_messages(self, client_context):
        """Method for displaying startup context"""
        self.process_response(client_context, client_context.bot.get_version_string(client_context))
        initial_question = client_context.bot.get_initial_question(client_context)
        self._renderer.render(client_context, initial_question)

    def process_question(self, client_context, question):
        """Method for processing the question in order to get a response"""
        self._questions += 1
        return client_context.bot.ask_question(client_context , question, responselogger=self)

    def render_response(self, client_context, response):
        """ Calls the renderer which handles RCS context, and then calls back to the client to show response"""
        self._renderer.render(client_context, response)

    def process_response(self, client_context, response):
        """This method publishes the response and prints it to the console"""
        self._publisher.publish(response)
        print("Bot-Henry: %s" %response)

    def process_question_answer(self, client_context):
        """Method for retrieving a question and a response"""
        question = self.get_question(client_context)
        print("Human: %s" %question.data)
        response = self.process_question(client_context, question.data)
        self.render_response(client_context, response)

    def wait_and_answer(self):
        """This is the main-loop of the bot"""
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
        """This method gets called before the run-method which is inherited by the EventBotClient-class
        This method sets up everything that is ROS-related, e.g. publisher and subscriber"""        
        self._topic_chat = self._configuration.client_configuration._rostopic_chat
        self._subscription = self._configuration.client_configuration._subscription
        self._publisher = rospy.Publisher(self._topic_chat, String, queue_size=self._configuration.client_configuration._queueSize)
        rospy.init_node(self._configuration.client_configuration.nodename, anonymous=True)
        self._rate = rospy.Rate(self._configuration.client_configuration._rosrate)

        client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
        self.display_startup_messages(client_context)


if __name__ == '__main__':
    def run():
        gestSettings.init()
        rosnode_app = ROSnodeClient()
        rosnode_app.run()

    run()
