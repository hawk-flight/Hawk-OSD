import os
import shutil
import urllib.request
import sys
import subprocess
import zipfile
try:
    from colorama import Fore
except():
    if subprocess.call([sys.executable, "-m", "pip", "install", "colorama"
                        ]) != 0:
        sys.exit("Could not install colorama!")
    from colorama import Fore


def log(*args):
    s = "".join(args) + Fore.RESET
    print(s)


WARN = Fore.LIGHTYELLOW_EX
ERR = Fore.LIGHTRED_EX
ACT = Fore.LIGHTCYAN_EX
OK = Fore.LIGHTGREEN_EX
INFO = Fore.LIGHTBLUE_EX


def downloadFile(url, fileName):
    with urllib.request.urlopen(url) as u:
        with open(fileName, 'wb') as f:
            contentLen = u.headers['content-length']
            try:
                contentLen = int(contentLen)
            except():
                contentLen = 0
            log(INFO, "Downloading '{0}' to '{1}'".format(url.split("/")[-1], fileName), " ({0} bytes)".format(contentLen) if contentLen > 0 else "")
            dlCount = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    print()
                    break
                dlCount += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (dlCount, dlCount * 100. / contentLen)
                print(status, end="\r")

def unzip(zipFile, destPath):
    log(INFO, "Unzipping file '{0}'".format(zipFile))
    with zipfile.ZipFile(zipFile) as f:
        uncompSize = sum((file.file_size for file in f.infolist()))
        countFiles = len(f.infolist())
        count = 0
        index = 1
        for e in f.infolist():
            count += e.file_size
            f.extract(e, destPath)
            print("%i/%i [%3.2f%%]" % (index, countFiles, (count * 100. / uncompSize)), end="\r")
            index += 1


def changeDir(path):
    log(INFO, "Changing working directory: '{0}'".format(path))
    os.chdir(path)


# configuration variables

cmsis_url = "https://keilpack.azureedge.net/pack/Keil.STM32G4xx_DFP.1.1.0.pack"
toolchain_url = "https://developer.arm.com/-/media/Files/downloads/gnu-rm/8-2019q3/RC1.1/gcc-arm-none-eabi-8-2019-q3-update-win32.zip?revision=2f0fd855-d015-423c-9c76-c953ae7e730b?product=GNU%20Arm%20Embedded%20Toolchain,ZIP,,Windows,8-2019-q3-update"

toolchain_path = "toolchain"
cache_path = "cache"

cmsis_dir = "cmsis"
tools_dir = "tools"

# go to root directory
changeDir("..")

# delete toolchain folder if it exists
if os.path.isdir(toolchain_path):
    shutil.rmtree(toolchain_path, ignore_errors=True)

# create toolchain directory
if not os.path.isdir(toolchain_path):
    os.mkdir(toolchain_path)
changeDir(toolchain_path)

# create cache directory
os.mkdir(cache_path)
changeDir(cache_path)
# download cmsis and toolchain
downloadFile(cmsis_url, cmsis_dir + ".zip")
downloadFile(toolchain_url, tools_dir + ".zip")
# unzip cmsis and toolchain
unzip(cmsis_dir + ".zip", "../" + cmsis_dir)
unzip(tools_dir + ".zip", "../" + tools_dir)

# delete cache dir
changeDir("..")
shutil.rmtree(cache_path)
