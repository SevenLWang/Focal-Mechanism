import sys
import os
from os.path import join
from glob import glob
import shutil
import subprocess
from tqdm import tqdm

datadir = '/work/wang_li/Project/Tibet/Test/'
os.environ['SAC_DISPLAY_COPYRIGHT']='0' #配置环境变量
number = 0
#os.system("cp %s/SAC/*.BHZ.M.SAC out_dire/") %  input_dire 
for dirs in (glob(datadir+'20*')):
    input_dire = "%s" % dirs
    print(input_dire)
    SAC = subprocess.Popen(['sac'],stdin=subprocess.PIPE) #建立子程序
    s=""
    for filename in os.listdir(input_dire):
        # os.path.splitext()是一个元组,类似于('188739', '.jpg')，索引1可以获得文件的扩展名
        if os.path.splitext(filename)[1]=='.SAC':
            number += 1
    time = number//3
    print(time)
    output_dire = os.system("mkdir %s/rot_dire/" % (input_dire))
    input_dire1=glob(input_dire+"/*.BH?.*.SAC")
    input_dire1.sort()
#   print(input_dire1)
    for freq in tqdm(range(time)):
        file_1 = input_dire1[freq*3]
        file_2 = input_dire1[freq*3+1]
        file_3 = input_dire1[freq*3+2]
        filename = os.path.basename(file_1)
        net = filename.split(".")[0]
        sta = filename.split(".")[1]
        cha = filename.split(".")[2]
        
        cmd = "saclst b e f %s" % (file_1)
        junk, b1, e1 = os.popen(cmd).read().split()
        b1 = float(b1)
        e1 = float(e1)

        cmd = "saclst b e f %s" % (file_2)
        junk, b2, e2 = os.popen(cmd).read().split()
        b2 = float(b2)
        e2 = float(e2)

        cmd = "saclst b e f %s" % (file_3)
        junk, b3, e3 = os.popen(cmd).read().split()
        b3 = float(b3)
        e3 = float(e3)
                    
        path1 = file_1.split('/')[-1]
        path2 = file_2.split('/')[-1]
        path3 = file_3.split('/')[-1]

### Cmpaz Correction
        s += "r %s\nch cmpaz %8.2f\nwh\n" % (file_1, 90)
        s += "r %s\nch cmpaz %8.2f\nwh\n" % (file_2, 0)
        s += "r %s\nch cmpaz %8.2f\nwh\n" % (file_3, 0)

### Cmpinc Correction
        s += "r %s %s\n ch cmpinc 90\n wh\n" % (file_1,file_2)
        s += "r %s\n ch cmpinc 0\n wh\n" % (file_3)

### Cut Off
        if b1 > b2 and b1 > b3: b=b1;
        elif b2 > b1 and b2 > b3: b=b2;
        else: b = b3

        if e1 < e2 and e1 < e3: e=e1;
        elif e2 < e1 and e2 < e3: e=e2;
        else: e=e3

        b += 0.1
        e -= 0.1

### Head Write    
        s += "cut off\ncut %f %f\n" % (b, e)
        s += "r %s %s\n" % (file_1,file_2)
        s += "rot to gcp\n"
        s += "w %s %s\n" % (join(net+'.'+sta+'.'+cha+'.r'), join(net+'.'+sta+'.'+cha+'.t'))
        s+= "cut off\n"
        shutil.copy(file_3, join(net+'.'+sta+'.'+cha+'.z'))
    s += "q\n"
    SAC.communicate(s.encode())
    os.system("mv *.[rtz] %s/rot_dire/" % (input_dire))

