
import os
import urllib.parse

class WebShellLoder:
    def __init__(self, define=""):
        base = "shell/"
        self.__antSwordPHP = f"{base}antSwordPHP.php"
        self.__BehinderPHP = f"{base}BehinderPHP.php"
        self.__antSwordJava = f"{base}antSwordJava.jsp"
        self.__BehinderJava = f"{base}BehinderJava.jsp"
        self.__GodPHP = f"{base}GodPHP.php"
        self.__GodJava = f"{base}GodJava.jsp"
        self.__define = f"{base}{define}"

    def urlencode(self, data: str) -> str:
        # 使用quote函数进行URL编码
        encoded_text = urllib.parse.quote(data)

        return encoded_text

    def readfile(self, webshell: str) -> str:
        """
        读取 webshell, 并返回
        """
        try:
            with open("shell/" + webshell, 'r', encoding='gb18030', errors='ignore') as file:
                data = file.read()
                data = data.replace("\n", "").replace("\t", "")
            return data
        except Exception as e:
            print(e)
        return ""

    def webshell_list(self) -> list:
        """
        查看文件夹内所有文件
        """
        modified_files = []

        for root, dirs, files in os.walk("shell"):
            for file in files:
                file_path = os.path.join(root, file)
                file_path = file_path.split("\\")[-1]
                modified_files.append(file_path)

        if len(modified_files) > 0:
            print("可使用 [->]")
            for webshell in modified_files:
                print("      " + webshell)
        return modified_files
