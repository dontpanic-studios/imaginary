import requests, sys
from os import path

class Downloader():
    def __init__():
        super().__init__()

    def whyNotQemu():
        if not path.isfile('src/qemu/qemu-system-x86_64.exe'):
            print('qemu does not exist, requesting.')

            with open("src/qemu/temp/qemu64.exe", "wb") as f:
                print("Downloading %s" % "qemu64.exe")
                response = requests.get("https://qemu.weilnetz.de/w64/2024/qemu-w64-setup-20240403.exe", stream=True)
                total_length = response.headers.get('content-length')

                if total_length is None:
                    f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(50 * dl / total_length)
                        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                        sys.stdout.flush()
                    print('\ndone, please install it from your/imaginary/project/path/src/qemu/')
        else:
            print('qemu exists')    