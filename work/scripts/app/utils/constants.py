"""
    Constants
"""
import platform


SIZE_X = 10
SIZE_Y = 10

STATE_DEFAULT = 0
STATE_CLICKED = 1
STATE_FLAGGED = 2

BTN_CLICK = '<Button-1>'
BTN_FLAG = '<Button-2>' if platform.system() == 'Darwin' else '<Button-3>'
