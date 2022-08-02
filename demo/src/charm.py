#! /usr/bin/python3

from ops.main import main
from ops_openstack.core import OSBaseCharm
from ops_utils import inherit_actions

# This will import every action, and together with the
# call to 'inherit_actions' below will allow the charm class
# to utilize every action as a method.
import actions   # noqa: F401


class DemoCharm(OSBaseCharm):

    def __init__(self, *args):
        super().__init__(*args)
        # This pulls every action into the charm class. If the need
        # arises to use the method directly, it can be retrieved as
        # '_action_name', the name being what's used in the 'ops_action'
        # decorator.
        inherit_actions(self)


if __name__ == '__main__':
    main(DemoCharm)
