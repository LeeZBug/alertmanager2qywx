"""
@Author: lizhejie
@Desc: 
@Usage: python3 utils.py
Let zeal join!
Copyright (c) 2023 by lizhejie, All Rights Reserved.
"""
from datetime import datetime
import re
import requests
import json
from setting import *


# 判断告警名称
def is_ignorealertname(alertname):
    if alertname in IGNORE_ALERT_NAME:
        return True
    else:
        return False


# iso时间转换，用于转换从alertmanager获取的时间
def isotime2localtime(isotimestr: str):
    # 判断最后一位时间是不是2位，2位就补0
    dot_index = isotimestr.rindex('.')
    z_index = isotimestr.index('Z')
    sub_string = isotimestr[dot_index + 1:z_index]
    numbers = re.findall(r'\d', sub_string)
    numbers_count = len(numbers)
    if numbers_count == 2:
        isotimestr = isotimestr.replace(sub_string, sub_string + "0")
    else:
        pass
    if "Z" in isotimestr:
        dt = datetime.fromisoformat(isotimestr.replace("Z", "+00:00"))
    else:
        dt = datetime.fromisoformat(isotimestr)
    local_dt = dt.astimezone()
    formatted_time = local_dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


# 判断年月日时分秒的时间是否为特定周几几点
def is_specialtime(formatted_time: str, special_time_list: list):
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


# 格式化告警信息
def format_alert(alert):
    labels = "\n".join([f'<font color="comment">{key}:</font>{value}' for key, value in alert['labels'].items()])
    annotations = "\n".join(
        [f'<font color="comment">{key}:</font>{value}' for key, value in alert['annotations'].items()])

    return f"**告警名称: **{alert['labels']['alertname']}\n**告警标签: **\n{labels}\n**告警注解: **\n{annotations}"


# 发送企业微信机器人信息
def webhook_url(params, url_key):
    headers = {"Content-type": "application/json"}
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={0}".format(url_key)
    r = requests.post(url, params, headers)


# 构建发送请求体
def alert2(content):
    params = json.dumps({
        "msgtype": "markdown",
        "markdown":
            {
                "content": content
            }
    })

    return params


if __name__ == '__main__':
    print(is_ignorealertname("TargetDown"))
