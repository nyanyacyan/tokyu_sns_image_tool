# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# import
import os
from enum import Enum

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# **********************************************************************************
# ログイン要素

class Login_elements(Enum):
    TOKYU = {
        "ID": "",
        "PASS": "",
        "LOGIN_BTN": "",
    }

# **********************************************************************************

class ClickElements(Enum):
    TOKYU = {
        "": "",
        "": "",
        "": "",
    }

# **********************************************************************************

class RoomInfo(Enum):
    DEFAULT_ROOM_DATA = {
        "title": "",
        "line": "",
        "station": "",
        "walk": "",

        "price": 0,
        "management_price": 0,

        "deposit": 0.0,
        "key_money": 0.0,

        "layout": "",
        "area": "",

        "features": [],
        "preferences": [],

        "exterior_image": "",
        "layout_image_path": "",

        "interior_1": "",
        "interior_2": "",
        "interior_3": "",
        "interior_4": "",
        "interior_5": "",

        "comment_b": "",
        "comment_c": "",
        "comment_d": ""
    }

# **********************************************************************************
