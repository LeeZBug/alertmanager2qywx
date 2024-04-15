"""
@Author: lizhejie
@Desc: 
@Usage: python3 alertinfo.py
Let zeal join!
Copyright (c) 2023 by lizhejie, All Rights Reserved.
"""
import time

import requests
import json
from utils import *
from setting import *


def send_alert(json_re, qywxbot_key):
    for alertinfo in json_re['alerts']:
        status = alertinfo.get('status')
        # labels = alertinfo.get('labels')
        # instance = labels.get('instance')
        system = alertinfo.get('labels').get('system', 'saas')
        # namespace = labels.get('namespace')
        # pod = labels.get('pod') or labels.get('service')
        alertname = alertinfo.get('labels').get('alertname')
        # severity = labels.get('severity')
        # system = labels.get('system')
        # annotations = alertinfo.get('annotations')
        # message = annotations.get('message') or annotations.get('description') or annotations.get('summary')
        startat = isotime2localtime(alertinfo.get('startsAt'))

        alertinfo_list = [alertinfo]
        formatted_alerts = map(format_alert, alertinfo_list)
        result_string = "\n".join(list(formatted_alerts))
        # print(result_string)

        if status == 'firing' and (not is_specialtime(startat, SILENCE_DICT.get(system, ALL_SILENCE_TIME))) and (
                not is_ignorealertname(alertname)):
            addition_title = "# <font color=\"red\">告警通知:</font>\n**告警时间:** {0}\n".format(startat)
            alert_msg = alert2(addition_title + result_string)
            webhook_url(alert_msg, qywxbot_key)
            time.sleep(2)
        elif status == 'resolved' and (not is_specialtime(startat, SILENCE_DICT.get(system, ALL_SILENCE_TIME))) and (
                not is_ignorealertname(alertname)):
            endsat = isotime2localtime(alertinfo.get('endsAt'))
            addition_title = "# <font color=\"green\">恢复通知:</font>\n**告警时间:** {0}\n**恢复时间:** {1}\n".format(
                startat, endsat)
            recover_msg = alert2(addition_title + result_string)
            webhook_url(recover_msg, qywxbot_key)
            time.sleep(2)
        else:
            print("告警命符合规则或告警时间为沉默时间，告警被沉默")
