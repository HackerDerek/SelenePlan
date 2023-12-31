
import ssl
import yaml
import httpx
import asyncio
from bs4 import BeautifulSoup
from tools.LogTool import CustomLogger

class HttpTool:
    def __init__(self, timeout=None, batch_size=None, proxy=None):
        # 获取配置信息
        data = self.__get_config()
        self.__results = {}
        self.__timeout = 4
        self.__proxy = None
        self.__batch_size = data.get("coroutine", 1000)  # 并发量
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            # Add more headers as needed
        }

        if timeout:
            self.__timeout = timeout
        if proxy:
            self.__proxy = self.__SetProxy(data.get("proxy", None))
        if batch_size:
            self.__batch_size = batch_size

        # 日志对象
        self.Logger = CustomLogger()

    def __http_url_check(self, url) -> str:
        if url.startswith("https://") == 0 and url.startswith("http://") == 0:
            return "http://" + url
        else:
            return url

    async def __async_fetch(self, url, method, headers, data, path, notes) -> None:
        httpx_url = url + path
        httpx_url = self.__http_url_check(httpx_url)
        proxies = self.__proxy
        timeout = self.__timeout
        ip_port = httpx_url.split('//')[1].split('/')[0]
        ip = httpx_url.split('//')[1].split('/')[0].split(':')[0]
        port = ip_port.split(':')
        if len(port) == 2:
            port = str(port[-1])
        else:
            port = 0
        try:
            async with httpx.AsyncClient(proxies=proxies, verify=False) as client:
                response = await client.request(method=method, url=httpx_url, headers=headers,
                                                data=data, timeout=timeout)
                await asyncio.sleep(self.__timeout)
                # 获取响应数据的编码方式
                #response.encoding = response.charset_encoding
                code = response.status_code
                # 使用BeautifulSoup解析响应内容，提取<title>标签内容
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string if soup.title else "No title found"
                state = "存活"
                self.__results[httpx_url] = [url, code, title, response.text, state, ip, port, ip_port, notes, response]
                print(f'[+]{httpx_url} {code} {title}')
        except (httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError) as E:
            state = "未存活或无法访问"
            self.__results[httpx_url] = [url, 0, str(E), '', state, ip, port, ip_port, "", ""]
            print(f'[-][{state}]: {httpx_url}  {E}')
        except ssl.SSLError as E:
            state = "STLv版本无法建立安全连接"
            self.__results[httpx_url] = [url, 0, str(E), '', state, ip, port, ip_port, "", ""]
            print(f"[-][{state}]: {httpx_url}  {E}")
        except Exception as E:
            state = "未知错误"
            self.__results[httpx_url] = [url, 0, str(E), '', state, ip, port, ip_port, "", ""]
            print(f"[-][{state}]: {httpx_url}  {E}")

    async def __async_main(self, urls_data) -> None:
        batch_size = self.__batch_size
        for i in range(0, len(urls_data), batch_size):
            batch = urls_data[i: i + batch_size]
            tasks = []
            for url, method, headers, data, path, notes in batch:
                if method is None:
                    method = "GET"
                if headers is None:
                    headers = self.headers
                if path is None:
                    path = ""
                if notes is None:
                    notes = ""
                tasks.append(self.__async_fetch(url, method, headers, data, path, notes))
            await asyncio.gather(*tasks)

    # 协程HTTPX异步请求启动
    def async_httpx_start(self, urls_data) -> dict:
        print(f"[*]---- 开始测试站点 ---- ")
        asyncio.run(self.__async_main(urls_data))
        print(f"[*]---- 站点测试结束 ---- \n")
        return self.__results

    def clean(self) -> None:
        self.__results.clear()

    def __get_config(self):
        """
        读取配置文件
        """
        config = "config.yaml"
        try:
            with open(config, 'r', encoding='gb18030', errors='ignore') as file:
                data = yaml.safe_load(file)
            if data is None:
                self.Logger.error(f'未能获取到 config.yaml 的数据\n')
            return data
        except FileNotFoundError:
            # 处理文件不存在的情况
            self.Logger.error(f'找不到配置文件 config.yaml\n')
        except yaml.YAMLError:
            # 处理 YAML 解析错误的情况
            self.Logger.error(f'配置文件 config.yaml 解析错误\n')
        except Exception:
            self.Logger.error(f'配置文件 config.yaml 解析出错，原因不明\n')

    def __SetProxy(self, url):
        """
        设置代理
        """
        if url is None:
            return None
        proxies = {
            "http": "http://{{baseurl}}",
            "https": "http://{{baseurl}}",
        }
        for k, v in proxies:
            v.replace("{{baseurl}}", url)

        return proxies
