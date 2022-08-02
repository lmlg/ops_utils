"""This file, and the file 'act2.py' showcases 2 simple examples
of how actions can be easily refactored to work with an operator
framework charm."""

from ops_wander.actions import (
    ops_action, action_get, action_set, action_fail, log)


@ops_action('act1')
def main():
    value = action_get('key1')
    if value:
        action_set({'message': value + '!'})
        return
    log('action 1 failed')
    action_fail('key1 not present')
