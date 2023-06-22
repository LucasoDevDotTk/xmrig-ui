import platform
import os

# Check which OS is running and install the correct packages

if platform.system() == "Linux":
    print(platform.system())
    url = "https://github.com/xmrig/xmrig/releases/download/v6.19.3/xmrig-6.19.3-linux-static-x64.tar.gz"
    os.system("curl -LJO " + url)

if platform.system() == "Windows":
    print(platform.system())
    url = "https://github.com/xmrig/xmrig/releases/download/v6.19.3/xmrig-6.19.3-gcc-win64.zip"
    os.system("curl -LJO " + url)

if platform.system() == "Darwin":
    print(platform.system())
    url = "https://github.com/xmrig/xmrig/releases/download/v6.19.3/xmrig-6.19.3-macos-arm64.tar.gz"
    os.system("curl -LJO " + url)
