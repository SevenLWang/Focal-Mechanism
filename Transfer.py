import sys
import os
from os.path import join
import glob
import shutil
import subprocess


os.environ['SAC_DISPLAY_COPYRIGHT']='0' #配置环境变量
dire = sys.argv[1]
input_dire = "%s" % dire
output_dire = "%s/rot_dire/" % dire
if not os.path.exists(output_dire):
    os.makedirs(output_dire) #创建新文件夹存储此次结果

number = 0
#os.walk()方法是一个简单易用的文件、目录遍历器
# root正在遍历的这个文件夹的本身的地址
# dirname是一个list,内容是该文件夹中所有的目录的名字(不包括子目录)
# filenames同样是list,内容是该文件夹中所有的文件名字(不包括子目录)
for root,dirname,filenames in os.walk(input_dire):  
       for filename in filenames: 
            # os.path.splitext()是一个元组,类似于('188739', '.jpg')，索引1可以获得文件的扩展名
            if os.path.splitext(filename)[1]=='.SAC':
                number += 1
time = number//3

SAC = subprocess.Popen(['sac'],stdin=subprocess.PIPE) #建立子程序
EW=0
s=""
#os.system("cp %s/SAC/*.BHZ.M.SAC out_dire/") %  input_dire 

#path = input_dire
#files = os.listdir(path)
#for item in files:
#    if not "BHZ.M.SAC" in item:
#        file_1=glob.glob(input_dire+"*.BH1.M.SAC") 
#        file_2=glob.glob(input_dire+"*.BH2.M.SAC")
#        file_n=glob.glob(input_dire+"*.BHN.M.SAC")
#        file_e=glob.glob(input_dire+"*.BHE.M.SAC")
#    else:
#        print("This file is vertical component")
#    if item in
#for file in glob.glob(input_dire+"/*BHZ.M.SAC"):
#    print(file)
#    os.system("cp input_dire/*.BHZ.M.SAC out_dire/")

input_dire1=glob.glob(input_dire+"/*.BH?.M.SAC")
for  freq in range(time):
    file_1 = input_dire1[freq*3] 
    file_2 = input_dire1[freq*3+1]
    file_3 = input_dire1[freq*3+2]
    filename = os.path.basename(file_1)
    print(filename)
    net = filename.split(".")[6]
    sta = filename.split(".")[7]
    print(join(net+"."+sta+".r"))
    if "BH1.M.SAC" in filename:
        continue
    elif "BHN.M.SAC" in filename:
        EW = 1
    
    cmd = "saclst b e cmpaz cmpinc f %s" % (file_1)
    junk, b1, e1, cmpaz1, cmpinc1 = os.popen(cmd).read().split()
    b1 = float(b1)
    e1 = float(e1)
    cmpaz1 = round(float(cmpaz1),1)
    cmpinc1 = round(float(cmpinc1),1) 

    cmd = "saclst b e cmpaz cmpinc f %s" % (file_2)
    junk, b2, e2, cmpaz2, cmpinc2 = os.popen(cmd).read().split()
    b2 = float(b2)
    e2 = float(e2)
    cmpaz2 = round(float(cmpaz2),1)
    cmpinc2 = round(float(cmpinc2),1)
    
    cmd = "saclst b e f %s" % (file_3)
    junk, b3, e3 = os.popen(cmd).read().split()
    b3 = float(b3)
    e3 = float(e3)
    
    print(cmpaz1,cmpaz2) 
    path1 = file_1.split('/')[-1]
    path2 = file_2.split('/')[-1]
### Cmpaz Correction
    corr = 0
    if EW:
        s += "r %s\nch cmpaz %8.2f\nwh\n" % (path1, 90)
        s += "r %s\nch cmpaz %8.2f\nwh\n" % (path2, 0) 
    else:
        diff_az = round(cmpaz1 - cmpaz2, 1)
        print(diff_az)
        if not (abs(diff_az) == 90 or abs(diff_az) == 270):
            print("%s and %s are not exactly orthogonal!\n Making correction......\n" %(cmpaz1,cmpaz2))
            if abs(diff_az) > 180:
                if diff_az > 0:
                    corr = diff_az - 270
                else:
                    corr = diff_az + 270
            else:
                if diff_az > 0:
                    corr = diff_az - 90
                else:
                    corr = diff_az + 90
        cmpaz1 = round(cmpaz1 - corr, 1)
        if cmpaz1 < 0:
            cmpaz1 += 360
        if cmpaz1 >= 360:
            cmpaz1 -= 360
        s += "r %s\nch cmpaz %8.2f\nwh\n" % (path1, cmpaz1)
        s += "r %s\nch cmpaz %8.2f\nwh\n" % (path2, cmpaz2) 
### Cmpinc Correction
    if (cmpinc1 != 90 or cmpinc2 !=90):
        s += "r %s %s\n ch cmpinc 90\n wh\n" % (path1,path2) 

###
    if b1 > b2 and b1 > b3: b=b1;
    elif b2 > b1 and b2 > b3: b=b2;
    else: b = b3
    
    if e1 < e2 and e1 < e3: e=e1;
    elif e2 < e1 and e2 < e3: e=e2;
    else: e=e3
    
    b += 0.1
    e -= 0.1
    
    s += "cut off\ncut %f %f\n" % (b, e)
    s += "r %s %s\n" % (path1, path2)
    s += "rot to gcp\n"
    s += "w %s %s\n" % (join(net+'.'+sta+'.r'), join(net+'.'+sta+'.t'))
    s += "cut off\n"
    shutil.copy(file_3, join(net+'.'+sta+'.z'))
s += "q\n"
SAC.communicate(s.encode())


