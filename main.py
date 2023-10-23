

import os
import yaml
import platform
import importlib
import tools.GlobalTool as Tool
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from tools.LogTool import CustomLogger


class ExploitConsole:

    def __init__(self, prompt="ExploitConsole > "):
        self.prompt = prompt
        self.proxy = None
        self.value = None

        # 日志对象
        self.Logger = CustomLogger()

        # 配置文件数据
        self.data = self.__get_config()

        self.modules = {}
        # 命令列表
        self.commands = ['search', 'help', 'use', 'clear', 'exit', 'list']
        self.command_completer = WordCompleter(self.commands, ignore_case=True)

        # 创建 KeyBindings 对象
        self.kb = KeyBindings()

    def __get_config(self):
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
            exit(-1)
        except Exception:
            self.Logger.error(f'配置文件 config.yaml 解析出错，原因不明\n')

    def __search(self, keyword) -> list:
        res = []
        pocs = Tool.list_directory_contents("poc")
        for poc in pocs:
            if keyword in poc:
                if ".pyc" in poc:
                    continue
                tmp = poc.replace("\\", '/')
                res.append(tmp)

        if len(res) > 0:
            print("\n" + "="*40)
            for poc in res:
                print(poc)
            print("="*40 + "\n")
        else:
            print("nothing")

        return res

    def __list(self) -> list:
        pocs = Tool.list_directory_contents("poc")

        if len(pocs) > 0:
            print("\n" + "="*40)
            for poc in pocs:
                if ".pyc" in poc:
                    continue
                tmp = poc.replace("\\", '/')
                print(tmp)
            print("="*40 + "\n")
        else:
            print("nothing")

        return pocs

    def __help(self):
        print("""
    name              | Command description                                               
    --------------------------------------------------------------------------------------------------------------------
    list              | 显示所有POC
    search            | search [keyword] 搜索指定poc                                       
    use               | use [poc] 执行指定poc                                            
    clear             | 清屏                                                          
    exit              | Go back                                                   
    --------------------------------------------------------------------------------------------------------------------
        """)

    def __run(self, poc, flag=1):
        try:
            if flag == 1:
                poc = poc.split('.')[0]
                poc = poc.replace('/', '.')
                module = importlib.import_module(poc)
                result = module.run()
            else:
                with open(poc, "r", encoding='utf-8', errors='ignore') as file:
                    script_code = file.read()

                exec(script_code)
        except Exception as e:
            print(e)

    def __clear(self):
        """Clear the screen"""
        os_name = platform.system()
        if os_name == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    def Console(self):
        while True:
            user_input = prompt(self.prompt, completer=self.command_completer,
                                history=FileHistory('tools/data/log/history.txt'))
            try:
                value = ""
                user_input = user_input.split()
                if len(user_input) < 1:
                    continue
                elif len(user_input) >= 2:
                    for i in range(1, len(user_input)):
                        value += user_input[i] + ' '

                if user_input[0] == 'exit':
                    break
                elif user_input[0] == 'search':
                    self.__search(value[:-1])
                elif user_input[0] == 'list':
                    self.__list()
                elif user_input[0] == 'help':
                    self.__help()
                elif user_input[0] == 'use':
                    self.__run(value)
                elif user_input[0] == 'clear':
                    self.__clear()
                else:
                    print(f"Unknown command: {user_input}")
            except Exception as E:
                self.Logger.error(E)

if __name__ == '__main__':
    E = ExploitConsole()
    E.Console()
