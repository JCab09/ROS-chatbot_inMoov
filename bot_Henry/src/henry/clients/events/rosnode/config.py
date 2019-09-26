"""
This file holds the ROSnodeConfiguration class
It is responsible for extracting the configuration values for the client from the config file.

The design of this file is heavily influenced by Keith Sterling's Program-Y console client.
For further information on the chatbot engine check out: https://github.com/keiffster/program-y

Author: Jason Cabezuela - https://github.com/JCab09/
"""

from programy.clients.config import ClientConfigurationData
from programy.utils.substitutions.substitues import Substitutions
import henry.oob.settings.gestures as gestSettings

class ROSnodeConfiguration(ClientConfigurationData):
    def __init__(self):
        ClientConfigurationData.__init__(self, "rosnode")

        # Initializing config-variables used by the client
        if gestSettings.g_firstInit == True:
            gestSettings.g_rostopic_gestures = "gestureOut"
            gestSettings.g_queueSize = 10
        self._default_userid = "rosClient"
        self._nodename = "chatbot"
        self._rostopic_chat = "chatbotOUT"
        self._subscription = "chatbotIN"
        self._rosrate = 10

    @property
    def default_userid(self):
        return self._default_userid

    @property
    def nodename(self):
        return self._nodename

    @property
    def rostopic_chat(self):
        return self._rostopic_chat

    @property
    def subscription(self):
        return self._subscription

    @property
    def rosrate(self):
        return self._rosrate


    def check_for_license_keys(self, license_keys):
        ClientConfigurationData.check_for_license_keys(self, license_keys)

    def load_configuration_section(self, configuration_file, rosnode, bot_root, subs: Substitutions = None):
        """This method writes the client-config from a file to variables"""
        if rosnode is not None:

            # Global config-variables used by the OOB-Gesture module to set up ROS
            gestSettings.g_firstInit = False
            gestSettings.g_rostopic_gestures = configuration_file.get_option(rosnode, "rostopic_gestures", missing_value="gestureOut", subs=subs)
            gestSettings.g_queueSize = configuration_file.get_option(rosnode, "queue_size", missing_value=10, subs=subs)

            # Config-variables used by the client to set up ROS
            self._queueSize = configuration_file.get_option(rosnode, "queue_size", missing_value=10, subs=subs)
            self._default_userid = configuration_file.get_option(rosnode, "default_userid", missing_value="rosClient", subs=subs)
            self._nodename = configuration_file.get_option(rosnode, "nodename", missing_value="chatbot", subs=subs)
            self._rostopic_chat = configuration_file.get_option(rosnode, "rostopic_chat", missing_value="chatBotOut", subs=subs)
            self._subscription = configuration_file.get_option(rosnode, "subscription", missing_value="chatBotIn", subs=subs)
            self._rosrate = configuration_file.get_option(rosnode, "rosrate", missing_value=10, subs=subs)

            super(ROSnodeConfiguration, self).load_configuration_section(configuration_file, rosnode, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['default_userid'] = "rosClient"
            data['nodename'] = "chatbot"
            data['rostopic_chat'] = "chatbotOUT"
            data['rostopic_gestures'] = "gestureOUT"
            data['subscription'] = "chatbotIN"
            data['rosrate'] = 10
            data['queue_size'] = 10
            print("to_yaml(default) exec")
        else:
            data['default_userid'] = self._default_userid
            data['nodename'] = self._nodename
            data['rostopic_chat'] = self._rostopic_chat
            data['rostopic_gestures'] = gestSettings.g_rostopic_gestures
            data['subscription'] = self._subscription
            data['rosrate'] = self._rosrate
            data['queue_size'] = gestSettings.g_queueSize
            print("to_yaml(custom) exec")
        super(ROSnodeConfiguration, self).to_yaml(data, defaults)
