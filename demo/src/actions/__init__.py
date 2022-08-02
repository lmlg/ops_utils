"""This file's purpose it to make it easier for charms to import every
action at once. The charm implementation (src/charm.py) should simply
'import actions' and then call 'inherit_actions' within the constructor
to incorporate them all as methods and make use of them."""

from ops_wander.actions import action_modules

__all__ = action_modules(__file__)
