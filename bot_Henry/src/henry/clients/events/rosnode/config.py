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

from programy.clients.config import ClientConfigurationData
from programy.utils.substitutions.substitues import Substitutions

class ROSnodeConfiguration(ClientConfigurationData):
    def __init__(self): 
        ClientConfigurationData.__init__(self, "rosnode")
        print("***clientconfigurationData DONE***")
        self._default_userid = "rosClient"
        self._nodename = "chatbot"
        self._rostopic = "chatOUT"
        self._subscription = "chatIN"
        self._rosrate = 10
        self._queueSize = 10

    @property
    def default_userid(self):
        return self._default_userid
    
    @property
    def nodename(self):
        return self._nodename

    @property
    def rostopic(self):
        return self._rostopic
    
    @property
    def subscription(self):
        return self._subscription
    
    @property
    def rosrate(self):
        return self._rosrate
    
    @property
    def queueSize(self):
        return self._queueSize

    def check_for_license_keys(self, license_keys):
        ClientConfigurationData.check_for_license_keys(self, license_keys)

    def load_configuration_section(self, configuration_file, rosnode, bot_root, subs: Substitutions = None):
        if rosnode is not None:
            self._default_userid = configuration_file.get_option(rosnode, "default_userid", missing_value="rosClient", subs=subs)
            self._nodename = configuration_file.get_option(rosnode, "nodename", missing_value="chatbot", subs=subs)
            self._rostopic = configuration_file.get_option(rosnode, "rostopic", missing_value="chatOUT", subs=subs)
            self._subscriber = configuration_file.get_option(rosnode, "subscription", missing_value="chatIN", subs=subs)
            self._rosrate = configuration_file.get_option(rosnode, "rosrate", missing_value=10, subs=subs)
            self._queueSize = configuration_file.get_option(rosnode, "queue_size", missing_value=10, subs=subs)
            super(ROSnodeConfiguration, self).load_configuration_section(configuration_file, rosnode, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['default_userid'] = "rosClient"
            data['nodename'] = "chatbot"
            data['rostopic'] = "chatOUT"
            data['subscription'] = "chatIN"
            data['rosrate'] = 10
            data['queue_size'] = 10
            print("to_yaml(default) exec")
        else:
            data['default_userid'] = self._default_userid
            data['nodename'] = self._nodename
            data['rostopic'] = self._rostopic
            data['subscription'] = self._subscription
            data['rosrate'] = self._rosrate
            data['queue_size'] = self._queueSize
            print("to_yaml(specific) exec")
        super(ROSnodeConfiguration, self).to_yaml(data, defaults)
