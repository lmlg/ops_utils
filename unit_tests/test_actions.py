from ops_utils.actions import (ops_action, action_get, action_set,
                               action_fail, inherit_actions)
import mock
import unittest


class MockEvent:
    def __init__(self, kv):
        self.params = mock.MagicMock()
        self.params.get = mock.MagicMock()
        self.params.get.side_effect = kv.get

        self.set_results = mock.MagicMock()
        self.fail = mock.MagicMock()
        self.log = mock.MagicMock()


@ops_action('dummy')
def action():
    key = action_get('key')
    if key:
        action_set({'message': 'done'})
    else:
        action_fail('key not present')


class MockCharm:
    def __init__(self):
        self.on = mock.MagicMock()
        self.framework = mock.MagicMock()
        self.framework.observe = mock.MagicMock()
        inherit_actions(self)


class TestOpsUtils(unittest.TestCase):

    def setUp(self):
        super(TestOpsUtils, self).setUp()

    def test_charm_interface(self):
        charm = MockCharm()
        self.assertIsNotNone(getattr(charm, '_dummy'))
        charm.framework.observe.assert_called_with(
            charm.on.dummy_action, charm._dummy)
        ev = MockEvent({'key': '123'})
        charm._dummy(ev)
        ev.fail.assert_not_called()
        ev.params.get.assert_called_with('key')
        ev.set_results.assert_called()

        ev = MockEvent({})
        charm._dummy(ev)
        ev.fail.assert_called()
