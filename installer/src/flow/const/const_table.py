# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
# import
import os
from enum import Enum

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# **********************************************************************************
# ログイン要素

class TableFlame(Enum):
    TEXTS_STORE_DB = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "createTime": "TEXT NOT NULL",

        "url": "TEXT NOT NULL",
        "trainName": "TEXT NOT NULL",
        "station": "TEXT NOT NULL",
        "walking": "TEXT NOT NULL",
        "stationWord": "TEXT NOT NULL",

        "area": "TEXT NOT NULL",
        "item": "TEXT NOT NULL",
        "address": "TEXT NOT NULL",
        "rent": "TEXT NOT NULL",  # 家賃
        "managementCost": "TEXT NOT NULL",  # 管理費
        "deposit": "TEXT",   # 敷金
        "keyMoney": "TEXT",  # 礼金

        "secondComment": "TEXT",
        "thirdComment": "TEXT",
        "fourthComment": "TEXT",
        "selectItems": "TEXT",
    }

# **********************************************************************************
