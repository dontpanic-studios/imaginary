import subprocess, asyncio
from qemu.qmp import QMPClient

async def syncStatus(name):
    qmp = QMPClient(name)
    print('Trying to connect to qmp.sock')
    await qmp.connect('qmp.sock')

    res = await qmp.execute('query-status')
    print(f'vmStatus: {res['staus']}')

    await qmp.disconnect()

def runSyncStatus(name):
    asyncio.run(syncStatus(name))   

def runQemu(iso_loc, disk_loc, mem_size: int, sys_core: int):
    try:
        subprocess.run(f'./src/qemu/qemu.exe -enable-kvm -m {mem_size} -smp {sys_core} -cdrom {iso_loc} -hda {disk_loc} -vga qxl -device AC97 -netdev user,id=net0,net=192.168.0.0,dhcpstart=192.168.0.9')
    except:
        print("qemu run failed.")