import os
import shutil
import urllib.request
import sys
import subprocess
import zipfile
try:
    from colorama import Fore
except ImportError:
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
    if os.path.isfile(fileName):
        return
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
                print("%10d  [%3.2f%%]" % (dlCount, dlCount * 100. / contentLen), end="\r")

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

def extract(zipFile, destPath):
    log(INFO, "Decompressing file '{0}'".format(zipFile))
    os.makedirs(destPath, exist_ok=True)
    currCwd = os.getcwd()
    os.chdir(destPath)
    subprocess.call([bsdtar, "-v", "-x", "-f", os.path.abspath(currCwd + "/" + zipFile)])
    os.chdir(currCwd)


def changeDir(path):
    log(INFO, "Changing working directory: '{0}'".format(path))
    os.chdir(path)


# configuration variables

toolchain_url = "https://developer.arm.com/-/media/Files/downloads/gnu-rm/8-2019q3/RC1.1/gcc-arm-none-eabi-8-2019-q3-update-win32.zip?revision=2f0fd855-d015-423c-9c76-c953ae7e730b?product=GNU%20Arm%20Embedded%20Toolchain,ZIP,,Windows,8-2019-q3-update"
cmake_url = "https://github.com/Kitware/CMake/releases/download/v3.15.0/cmake-3.15.0-win64-x64.zip"
openocd_url = "http://sysprogs.com/getfile/552/openocd-20190715.7z"
libarchive_url = "https://liquidtelecom.dl.sourceforge.net/project/ezwinports/libarchive-3.3.1-w32-bin.zip"

toolchain_path = "toolchain"
cache_dir = "cache"

# go to root directory
changeDir(os.path.dirname(os.path.abspath(__file__)) + "/../")

# delete toolchain folder if it exists
# if os.path.isdir(toolchain_path):
#     shutil.rmtree(toolchain_path, ignore_errors=True)

# create toolchain directory
if not os.path.isdir(toolchain_path):
    os.mkdir(toolchain_path)
changeDir(toolchain_path)

# delete all folders except cache
for f in os.listdir("."):
    if f != cache_dir:
        shutil.rmtree(f, ignore_errors=True)

# create cache directory
if not os.path.isdir(cache_dir):
    os.mkdir(cache_dir)
changeDir(cache_dir)

# download toolchain, cmake and openocd
downloadFile(libarchive_url, "libarchive.zip")
downloadFile(toolchain_url, "toolchain.zip")
downloadFile(cmake_url, "cmake.zip")
downloadFile(openocd_url, "openocd.7z")

# extract libarchive, and set bsdtar path
unzip("libarchive.zip", "../libarchive")
bsdtar = os.path.abspath("../libarchive/bin/bsdtar.exe")

# extract toolchain, cmake and openocd
unzip("toolchain.zip", "../")
unzip("cmake.zip", "../cmake")
extract("openocd.7z", "../openocd")

# delete cache dir
# changeDir("..")
# shutil.rmtree(cache_dir)
