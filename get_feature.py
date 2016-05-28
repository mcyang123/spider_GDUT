# -*- coding: utf-8 -*-
"""
Created on Sun May 22 17:20:30 2016
提取字符特征，保存到txt中
@author: mike
"""

import pylab
import PIL.Image as Image
import os

def f_catch(IM,size_g):
    IMA = array(IM)
    width,high = IMA.shape
    gL = []
    for r in range(int(width/size_g)):
        for c in range(int(high/size_g)):
            gL.append(len(list(find(IMA[r*size_g:(r+1)*size_g,c*size_g:(c+1)*size_g] < 10))))
    return gL
    
path = r'C:\Users\mike\Desktop\spider_GDUT\pic2'
f = open(path+'\\gea.txt','a')
f_l = os.listdir(path)
for fn in f_l:
    if fn[-3:] =='jpg':
        im = Image.open(path+'\\'+fn)
        gea = f_catch(im,10)
        f.write(fn+':'+str(gea)+'\n')
f.close()  
print 'end'

f = open(path+'\\gea.txt','r')
f2 = open(path+'\\gea2.txt','a')
temp = ''
for s in f:
    L = s.split(':')
    exec('x ='+L[1] )
    print L[0][0],temp
    if L[0][0]!= temp:
        z = array(x)
        temp = L[0][0]
    else:
        y = array(x)
        y = (y+z)/2
        f2.write(L[0][0]+':'+str(list(y))+'\n')
print 'end2'
f.close()
f2.close()