import platform
import os
import shutil
import zipfile
import tarfile

def delete_xmrig():
    if platform.system() == "Linux":
        os.system("rm -rf xmrig/xmrig-6.19.3")

    if platform.system() == "Windows":
        shutil.rmtree("xmrig/xmrig-6.19.3")

    if platform.system() == "Darwin":
        os.system("rm -rf xmrig/xmrig-6.19.3")

def install_xmrig():

    try:
        delete_xmrig()
    except:
        pass

    if platform.system() == "Linux":
        print(platform.system())
        url = "https://github.com/xmrig/xmrig/releases/download/v6.19.3/xmrig-6.19.3-linux-static-x64.tar.gz"
        os.system("curl -LJO " + url)

        tar = tarfile.open("xmrig-6.19.3-linux-static-x64.tar.gz")
        tar.extractall(path="xmrig")
        tar.close()

        os.system("rm xmrig-6.19.3-linux-static-x64.tar.gz")

    if platform.system() == "Windows":
        print(platform.system())
        url = "https://github.com/xmrig/xmrig/releases/download/v6.19.3/xmrig-6.19.3-gcc-win64.zip"
        os.system("curl -LJO " + url)

        with zipfile.ZipFile("xmrig-6.19.3-gcc-win64.zip", 'r') as zip_ref:
            zip_ref.extractall("xmrig")
        
        os.system("del xmrig-6.19.3-gcc-win64.zip")

    if platform.system() == "Darwin":
        print(platform.system())
        url = "https://github.com/xmrig/xmrig/releases/download/v6.19.3/xmrig-6.19.3-macos-arm64.tar.gz"
        os.system("curl -LJO " + url)

        tar = tarfile.open("xmrig-6.19.3-macos-arm64.tar.gz")
        tar.extractall(path="xmrig")
        tar.close()

        os.system("rm xmrig-6.19.3-macos-arm64.tar.gz")
