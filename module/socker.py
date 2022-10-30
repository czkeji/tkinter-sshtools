import re
import datetime
import paramiko

class SshTest:
    def __init__(self, host, port, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        try:
            self.ssh.connect(self.host, self.port, self.username, self.pwd, timeout=5)
            self.sshinvalid = False
            # print(self.sshinvalid)
        except Exception as errmsg:
            self.sshinvalid = True
            self.errormsg = errmsg
            # print(self.sshinvalid)
    def check_ssh_status(self):
        if self.sshinvalid:
            send_msg = ('**告警时间：** ' + self.timenow  + ' \\\n **告警主机：** ' + str(self.host) + ' \\\n **告警内容：** ' + str(self.errormsg) + ' ')
            warn_type='主机SSH无法连接'
            sshstat = False
            # 如遇到无法ssh连接，报错详细信息
            # print(self.errormsg)
            print('ssh连接报错为: ' + str(self.errormsg))
        else:
            send_msg = ('**告警时间：** ' + self.timenow  + ' \\\n **告警主机：** ' + str(self.host) + ' \\\n **告警内容：** ')
            warn_type='主机SSH连接正常'
            sshstat = True
            print(warn_type)
        return send_msg,warn_type,sshstat
    def exec_ssh_cmd(self,cmd,report):
        if self.sshinvalid:
            i = 'SSH无法连接，请检查主机'
            # print(i)
            cmd_out = []
            cmd_out.append(i)
        else:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            # 定义一个空列表，后续用于存储命令输出
            cmd_out = []
            for i in stderr.readlines():
                print('执行命令错误为： ' + i)
                cmd_out.append(i)
            for i in stdout.readlines():
                print('命令执行成功，输出为： ' + i)
                with open(report +'report.txt', 'a+', encoding='utf8') as f:
                    f.write(i)
                cmd_out.append(i)
        # 如果有多行，则下面i返回的是最后一行数据，一定注意
        return cmd_out