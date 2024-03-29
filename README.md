# alert2qywx

## 描述：
alertmanager告警信息发送到企业微信群，先发送到alert2qywx程序，再由alert2qywx对信息格式解析后再发送到企业微信群中。
并可以对指定对应标签system的告警进行周期沉默，避免正常业务系统更新等操作导致出现告警

## 使用:
alertmanager配置webhook处配置url为'http://[ip]:[port]/alertmanager2qywx?key=[企业微信机器人的key]'即可

## 创建 systemd 文件(centos)
[root@zabbix system]# cat /usr/lib/systemd/system/alert2qywx.service  
[Unit]  
Description=This is prometheus node exporter  
After=docker.service  
[Service]  
Type=simple  
ExecStart=/usr/bin/python3 /opt/alert2qywx/app/main.py -p 5000 -k XXXX {替换为机器人key}  
ExecReload=/bin/kill -HUP $MAINPID  
KillMode=process  
Restart=on-failure  
[Install]  
WantedBy=multi-user.target

## 启动：
systemctl start alert2qywx.service



创建docker镜像：      
1、创建app目录，将代码文件拷贝到app下。     
2、在app目录下指定依赖包，放在rquirements.txt中。             
3、requirements.txt与dockerfile同目录。               
4、docker build . -t /lizhejie/alert2qywx
docker run -d -p 5000:8000 --name alert2qywx  lizhejie/alert2qywx


## 注意事项：
程序解析以下标签:

    instance = labels.get('instance') # 实例
    name = labels.get('alertname') # 告警名称
    severity = labels.get('severity') # 自定义severity
    system = labels.get('system')  # 自定义system,设置改标签可以进行对应的告警沉默设置
    annotations = alertinfo.get('annotations')
    summary = annotations.get('summary') # 自定义注解中的summary

prometheus的rule示例:

    groups:
    - name: Mysql数据库3306端口探测失败!
      rules:    # 规则设置
      - alert: Mysql数据库3306端口探测失败!
        expr: probe_success{instance=~".*:3306"} != 1
        for: 1m    # 告警持续时间
        labels:
          severity: 1
          team: p0
        annotations:
          summary: "{{ $labels.system }}系统-Mysql数据库{{ $labels.instance }}端口探测失败"

