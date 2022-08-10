# Copyright 2022 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import errno
import glob
from logging import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
import os
import threading

_thread_local = threading.local()
_ops_actions = {}

_MAX_ARGS = 131071


def action_get(*args, **kwargs):
    """Get the value associated with a key."""
    return _thread_local.event.params.get(*args, **kwargs)


def action_set(*args, **kwargs):
    """Set the results of an action."""
    return _thread_local.event.set_results(*args, **kwargs)


def action_fail(*args, **kwargs):
    """Set the failure reason for an action."""
    return _thread_local.event.fail(*args, **kwargs)


def clear_event():
    """Mark the current event as invalid."""
    _thread_local.event = None


def set_event(event):
    """Set the current event."""
    _thread_local.event = event


def ops_action(name):
    """Decorate a function so that it's registered as an action
       with a particular name."""
    def wrapper(fn):
        _ops_actions[name] = fn
        return fn
    return wrapper


def action_modules(path):
    """Return a list of action modules. This is a helper utility
       so that charms may define an __init__.py file for actions
       and place the result of this call as __all__, and make the
       charm inherit all the actions' implementations."""
    files = glob.glob(os.path.join(os.path.dirname(path), "*.py"))
    return [os.path.basename(f)[:-3] for f in files
            if os.path.isfile(f) and not f.endswith('__init__.py')]


def inherit_actions(inst):
    """Make a charm class 'inherit' all the registered actions as methods."""
    def _make_method(fn):
        def _inner(self, event):
            try:
                set_event(event)
                return fn()
            finally:
                clear_event()
        return _inner

    cls = type(inst)
    fw = inst.framework
    for name, fn in _ops_actions.items():
        method_name = '_' + name
        method = _make_method(fn)
        # In addition to being a method, the action callbacks _must_ have
        # the same '__name__' as their attribute name (this is how lookups
        # work in the operator framework world).
        method.__name__ = method_name
        setattr(cls, method_name, method)
        fw.observe(getattr(inst.on, name + '_action'),
                   getattr(inst, method_name))
