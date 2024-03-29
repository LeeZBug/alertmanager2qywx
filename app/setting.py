"""
@Author: lizhejie
@Desc: 
@Usage: python3 setting.py
Let zeal join!
Copyright (c) 2023 by lizhejie, All Rights Reserved.
"""
# TODO 这种方式的告警沉默无法进行实时编辑
# 沉默告警时间设置.可以使用多个
OA_SILENCE_TIME = ["Tue:22-23", "Thu:22-23"]

# 系统沉默字典,key对应告警的system标签.程序会自动找到对应的system键值进行判断是否需要沉默告警
SILENCE_DICT = {
    "oa": OA_SILENCE_TIME,
}
