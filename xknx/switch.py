import time
from xknx.knx import Address
from .binaryinput import BinaryInput
from .action import Action
from .switchtime import SwitchTime

class Switch(BinaryInput):

    def __init__(self,
                 xknx,
                 name,
                 group_address=None,
                 actions=None,
                 device_updated_cb=None):
        # pylint: disable=too-many-arguments
        if isinstance(group_address, (str, int)):
            group_address = Address(group_address)
        if actions is None:
            actions = []

        BinaryInput.__init__(self, xknx, name, group_address, device_updated_cb)
        self.last_set = None
        self.actions = actions


    @classmethod
    def from_config(cls, xknx, name, config):
        group_address = \
            config.get('group_address')

        actions = []
        if "actions" in config:
            for action in config["actions"]:
                action = Action.from_config(xknx, action)
                actions.append(action)

        return cls(xknx,
                   name,
                   group_address=group_address,
                   actions=actions)


    def get_switch_time(self):
        if self.last_set is None:
            self.last_set = time.time()
            return SwitchTime.LONG

        new_set_time = time.time()
        time_diff = new_set_time - self.last_set
        self.last_set = new_set_time
        if time_diff < 0.2:
            return SwitchTime.SHORT
        return SwitchTime.LONG


    def process(self, telegram):
        BinaryInput.process(self, telegram)
        switch_time = self.get_switch_time()

        for action in self.actions:
            if action.test(self.state, switch_time):
                action.execute()


    def __str__(self):
        return '<Switch group_address="{0}" name="{1}" />' \
            .format(self.group_address, self.name)


    def __eq__(self, other):
        return self.__dict__ == other.__dict__
