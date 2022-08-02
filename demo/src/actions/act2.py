from ops_wander.actions import (
    ops_action, action_get, action_fail, action_set, log)


@ops_action('act2')
def main():
    value2 = action_get('key2')
    value3 = action_get('key3')
    if value2 and value3:
        action_set({'message': '{} {}'.format(value2, value3)})
        return
    elif value2:
        action_set({'message': value2.lower()})
        return
    elif value3:
        action_set({'message': value3.upper()})
        return

    log('action 2 failed')
    action_fail('keys not present')
