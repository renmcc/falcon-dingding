#!/usr/bin/env python
#coding:utf-8
#__author__ = "ren_mcc"

import os
from flask import Flask,request,jsonify,render_template,abort
import commands
import json
import urllib2

app = Flask(__name__)

url = "https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxx"
header = {
    "Content-Type": "application/json",
    "charset": "utf-8"
}

@app.route('/API/runner',methods=['POST'])
def Runner():
    if not request.json or not 'content' in request.json or not 'tos' in request.json:
        abort(400)
    recive_data = request.form.get('content')
    recive_data = recive_data.replace('[]', '').replace('[','').replace(']',',').rstrip(',').split(',')
    print recive_data[4]
    stat = u'### %s\n' % recive_data[1]
    host = u'- 监控主机: %s\n' % recive_data[2]
    item = u'- 监控指标: %s\n' % recive_data[3]
    count = u'- 报警次数: %s\n' % recive_data[4].split()[0]
    time = u'- 报警时间: %s\n' % ' '.join(recive_data[4].split()[1:])
    recive_data = stat + host + item + count + time
    data = {
        "msgtype": "markdown",
        "markdown": {
        "title":stat.strip('#'),
        "text":recive_data
        },
        "at":{
        "atMobiles":[
        ],
        "isAtAll":True
        }
    }
    sendData = json.dumps(data)
    result = urllib2.Request(url,data = sendData,headers = header)
    urlopen = urllib2.urlopen(result)

    return json.dumps('ok',indent=4)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
