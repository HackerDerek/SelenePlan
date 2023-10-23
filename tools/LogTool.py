
import datetime
import platform
from colorama import init, Fore, Style

# 适用于Linux操作系统的语法高亮，定义ANSI转义码
class ANSI:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"

class CustomLogger:
    def __init__(self):
        init()
        self.system_type = platform.system()

    def info(self, tip=""):
        #self._print_log("[*]", tip)
        if self.system_type == "Windows":
            self._print_log("[*]", tip, True)
        else:
            self._print_log("[*]", tip, True)

    def error(self, tip=""):
        self._print_log("[-]", tip, False)

    def warn(self, tip=""):
        self._print_log("[!]", tip, False)

    def pass_msg(self, tip=""):
        self._print_log("[+]", tip, False)

    def get_msg(self, tip=""):
        if self.system_type == "Windows":
            self._print_log("   [->]", tip, False)
        else:
            self._print_log("   [->]", tip, False)

    def _print_log(self, prefix, tip, time: bool):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if time:
            print(f"[{timestamp}] {prefix} {tip}")
        else:
            print(f"{prefix} {tip}")

