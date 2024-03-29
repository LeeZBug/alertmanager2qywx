"""
@Author: lizhejie
@Desc: 
@Usage: python3 utils.py
Let zeal join!
Copyright (c) 2023 by lizhejie, All Rights Reserved.
"""
from datetime import datetime


# iso时间转换
def isotime2localtime(isotimestr: str):
    dt = datetime.fromisoformat(isotimestr.replace("Z", "+00:00"))
    local_dt = dt.astimezone()
    formatted_time = local_dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


# 判断年月日时分秒的时间是否为特定周几几点
def isspecialtime(formatted_time: str, special_time_list: list):
    # 获去告警时间的星期几和小时
    date_format = '%Y-%m-%d %H:%M:%S'
    date = datetime.strptime(formatted_time, date_format)
    weekday = date.weekday()
    # 星期一为0，星期日为7
    weekday_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hour_name = date.hour

    for special_time in special_time_list:
        # 获取指定时间的星期几和小时
        st_weekday = special_time.split(":")[0]
        # print(st_weekday, special_time)
        st_time_start = int(special_time.split(":")[1].split("-")[0])
        st_time_end = int(special_time.split(":")[1].split("-")[1])
        if weekday_name[weekday] == st_weekday and is_between(hour_name, st_time_start, st_time_end):
            print("该时间段告警沉默，不进行告警")
            return True
    return False


# 判断某个数是不是在两数之间
def is_between(number: int, lower_limit: int, upper_limit: int):
    return lower_limit <= number <= upper_limit
