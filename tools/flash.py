import os
import sys
import subprocess
import struct
try:
    from colorama import init, Fore
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore

from shutil import copyfile
import itertools

openocd = "../toolchain/openocd/OpenOCD-20190715-0.10.0/bin/openocd.exe"

firmware = "../build/hawk-osd.bin"

def flatten(l):
    result = []
    for val in l:
        if isinstance(val, list):
            result.extend(flatten(val))
        else:
            result.append(val)
    return result


def sanitizeArgs(args):
    if args is None:
        return None
    args.append(resetRun)
    args = flatten(args)
    return args


def parseFloat(s):
    try:
        return float(s)
    except:
        return None


def parseInt(s):
    try:
        return int(s)
    except:
        return None

def clear():
    os.system('cls' if os.name == "nt" else 'clear')


ERR = Fore.LIGHTRED_EX
WARN = Fore.LIGHTYELLOW_EX
OK = Fore.LIGHTGREEN_EX
INFO = Fore.LIGHTBLUE_EX
RESET = Fore.RESET

def log(s):
    print(s + RESET)

def runOpenOCD(targetFile, commands):
    args = [openocd, "-f", targetFile, "-c"]
    args.append("; ".join(sanitizeArgs(commands)))
    result = subprocess.call(args, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
    if result != 0:
        log(ERR + "Error: {0}".format(result))
        return False
    else:
        log(OK + "Success")
        return True


resetRun = [
    "shutdown"
]
erase = [
    "stm32l4x mass-erase 0"
]


def flashFirmware():
    return [
        "program %s verify reset 0x08000000" % firmware
    ]


os.chdir(os.path.dirname(os.path.realpath(__file__)))
init()

runOpenOCD("st-link.cfg", flashFirmware())