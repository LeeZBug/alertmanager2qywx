from flask import Flask, request
from gevent import pywsgi
import sys
import alertinfo
import argparse
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "Prometheus告警企业微信通知服务"


@app.route('/alertmanager2qywx', methods=['POST'])
def alert_data():
    qywxbot_key = request.args.get('key', args.key)
    data = request.get_data()
    # print(data.decode(encoding='utf8'))
    json_re = json.loads(data)
    # print(json_re['alerts'])
    # print(qywxbot_key)
    alertinfo.send_alert(json_re, qywxbot_key)
    return {"msg": "通知发送成功"}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="The service port")
    parser.add_argument("-k", "--key", type=str, help="The webhook url key")
    args = parser.parse_args()

    # if not args.port or not args.key:
    #     parser.print_help()
    #     sys.exit(0)
    if not args.port:
        args.port = 8000
    if not args.key:
        print("没有输入默认的企业微信机器人key，可以在配置webhook的url时使用key参数配置")
    # app.run(host="0.0.0.0", port=args.port)

    server = pywsgi.WSGIServer(('0.0.0.0', args.port), app)
    server.serve_forever()
