# -*- coding: utf-8 -*-
"""
打开图片，模式转换，去噪
"""
import PIL.Image as Image
from pylab import *
import string
import numpy as np

#去噪
def Filter_1(i):
    if i>35:
        i = 255
    else:
        i=0
    return i
#图像强化
def strong(IM,power):
    IM_C = IM.copy()
    IM_CA = array(IM_C)
    IMA = array(IM)
    width,high = IMA.shape
    for r in range(width)[power:width-power]:
        for c in range(high)[power:high-power]:   
            if IMA[r,c]<5:
                IM_CA[r-power:r+power,c-power:c+power] = 0
    return Image.fromarray(IM_CA)
                
#特征提取                
def f_catch(IM,size_g):
    IMA = array(IM)
    width,high = IMA.shape
    gL = []
    for r in range(int(width/size_g)):
        for c in range(int(high/size_g)):
            gL.append(len(list(find(IMA[r*size_g:(r+1)*size_g,c*size_g:(c+1)*size_g] < 10))))
    return gL

#分割图片
def split_pic(im):
    ima = array(im)
    row,col = ima.shape
    t = -1
    imL = []
    for c in range(col):
        if len(find(ima[:,c]>250)) == row:
            if c-t>33:
                im_t = im.crop((t+1,0,c,row))
                im_ta = array(im_t)
                row2,col2 = im_ta.shape
                r21 = 0
                while len(find(list(im_ta[r21,:])>250)) == col2 :
                    r21 = r21+1
                r22 = 1
                while len(find(list(im_ta[row2-r22,:])>250)) == col2:
                    r22 = r22+1
                r22 =row2-r22
                im_d = im_t.crop((0,r21,col2,r22))
                im3 = Image.new('L',(100,100),(255))
                im_d = im_d.resize((100,100))
                im_d = strong(im_d,1)
                im_d = im_d.resize((100,100))
                imL.append(im_d)
                t  = c
            else:
                t = c
    #print len(imL)
    return imL

def str2text(im):
    text = ''
    w,h = im.size
    im = im.resize((w*10,h*10))
    im = im.convert('L').point(Filter_1)   #图片预处理
    im = strong(im,1)
    IML = split_pic(im)                                      #分割
    f = open(r'gea2.txt','r')
    GLD = {}
    for g in f:
        LL = g.split(':')
        exec("GLD['"+str(LL[0])+"']="+LL[1])
    f.close()
    for IM in IML:
        GL = f_catch(IM,10)                                   #特征数组
        count_L =[]
        key = GLD.keys()
        for g in range(len(GLD)):
            count_L.append(sum((array(GLD[key[g]])-array(GL))**2))
        count_L = array(count_L)
        count_index = list(find(count_L == min(count_L)))
        if len(count_index)>0:
            text = text+key[count_index[0]]
    f.close()
    return text
            
        
if __name__ =='__main__':
    filename = r'C:\Users\mike\Desktop\spider_GDUT\3.jpg'
    im = Image.open(filename)
    t = str2text(im)
    print t
    


