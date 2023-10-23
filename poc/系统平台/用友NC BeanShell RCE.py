

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork


ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
def help():
    print('''
    fofa: title=="YONYOU NC"
        1. 用友NC BeanShell RCE servlet利用, /servlet/~ic/bsh.servlet.BshServlet页面可RCE
    x. 退出
    ''')

def vul_servlet(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
    }
    body = ""
    method = "GET"
    path = "/servlet/~ic/bsh.servlet.BshServlet"
    notes = ""
    return (url, method, headers, body, path, notes)

def run():
    OUTDIR = "result/用友"
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
            item = vul_servlet(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            try:
                if v[1] != 200:
                    url = v[0] + '/servlet/~ic/bsh.servlet.BshServlet'
                    print(f'[+] {url} -> getRCE')
            except Exception as E:
                pass
            res.append(v[:-2])
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}用友NC BeanShell RCE.xlsx")

    else:
        print('bye....')
