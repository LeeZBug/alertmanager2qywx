"""
@Author: lizhejie
@Desc: 
@Usage: python3 alertinfo.py
Let zeal join!
Copyright (c) 2023 by lizhejie, All Rights Reserved.
"""
import requests
import json
from utils import *
from setting import *


def alert(status, instance, name, severity, system, startat, summary):
    params = json.dumps({
        "msgtype": "markdown",
        "markdown":
            {
                "content": "## <font color=\"red\">告警通知: {0}</font>\n**告警实例:** <font color=\"red\">{1}</font>\n**告警名称:** {2}\n**告警级别:** {3}\n**相关系统:** {4}\n**告警时间:** {5}\n**告警详情:** {6}".format(
                    status, instance, name, severity, system, startat, summary)
            }
    })

    return params


def recover(status, instance, name, severity, system, startat, endsat, summary):
    params = json.dumps({
        "msgtype": "markdown",
        "markdown":
            {
                "content": "## <font color=\"green\">恢复通知: {0}</font>\n**恢复实例:**<font color=\"green\"> {1}</font>\n**告警名称:** {2}\n**告警级别:** {3}\n**相关系统:** {4}\n**告警时间:** {5}\n**恢复时间:** {6}\n**告警详情:** {7}".format(
                    status, instance, name, severity, system, startat, endsat, summary)
            }
    })

    return params


def webhook_url(params, url_key):
    headers = {"Content-type": "application/json"}
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={0}".format(url_key)
    r = requests.post(url, params, headers)


def send_alert(json_re, qywxbot_key):
    for alertinfo in json_re['alerts']:
        status = alertinfo.get('status')
        labels = alertinfo.get('labels')
        instance = labels.get('instance')
        # job = labels.get('job')
        name = labels.get('alertname')
        severity = labels.get('severity')
        system = labels.get('system')
        # team = labels.get('team')
        annotations = alertinfo.get('annotations')
        summary = annotations.get('summary')
        startat = isotime2localtime(alertinfo.get('startsAt'))

        if status == 'firing' and (not isspecialtime(startat, SILENCE_DICT.get(system, ["Mon:0-1"]))):
            # endsat = alertinfo.get('endsAt')
            alert_msg = alert(status, instance, name, severity, system, startat, summary)
            webhook_url(alert_msg, qywxbot_key)
        elif status == 'resolved' and (not isspecialtime(startat, SILENCE_DICT.get(system, ["Mon:0-1"]))):
            endsat = isotime2localtime(alertinfo.get('endsAt'))
            recover_msg = recover(status, instance, name, severity, system, startat, endsat, summary)
            webhook_url(recover_msg, qywxbot_key)
        else:
            pass
