# -*- coding: utf-8 -*-
"""
Created on Sun May 22 15:13:15 2016
获取验证码图片，
手动输入验证码内容，
将验证码分割
每个片用其字符命名并保存到pic2中
@author: mike
"""
import urllib2
import urllib
import re
import PIL.Image as Image

def f_en(i):
    if i>20:
        i = 255
    else:
        i=0
    return i

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
    
def split_pic(im):
    ima = array(im)
    row,col = ima.shape
    t = -1
    imL = []
    for c in range(col):
        if len(find(ima[:,c]>240)) == row:
            if c-t>2:
                im_t = im.crop((t+1,0,c,row))
                im_ta = array(im_t)
                row2,col2 = im_ta.shape
                print row2
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
    return imL
    
path = r'C:\Users\mike\Desktop\spider_GDUT\pic2'
host = 'http://222.200.98.3'
url = host+'/selfservice/login.jsf'
f = open(path+'\\log.txt','r')
exec('wordL='+f.read())
code = ''
f.close()
f = open(path+'\\log.txt','w')
while code!='@':
    html = urllib2.urlopen(url).read()
    p_url_t = re.findall('<img src=(.+)jpg',html)
    if len(p_url_t)>0:
        p_url = host+p_url_t[0][1:]+'jpg'
        print p_url
        urllib.urlretrieve(p_url,'temp.jpg')
        im = Image.open('temp.jpg').convert('L').point(f_en)
        IML = split_pic(im)
        print len(IML)
        if len(IML)==4:
            im.show()
            code = raw_input('code:')
            if len(code) == 4:
                for i in range(len(code)):
                    print code[i]
                    if code[i] not in wordL.keys():
                        wordL[code[i]] = 1
                        if code[i].isupper():
                            IML[i].save(path + '\\'+code[i]+'_'+str(1)+'.jpg')
                        else:
                            IML[i].save(path + '\\'+code[i]+str(1)+'.jpg')
                    elif wordL[code[i]] < 2:
                        wordL[code[i]] = wordL[code[i]]+1
                        if code[i].isupper():
                            IML[i].save(path + '\\'+code[i]+'_'+str(wordL[code[i]])+'.jpg')
                        else:
                            IML[i].save(path + '\\'+code[i]+str(wordL[code[i]])+'.jpg')
                    else:
                        pass
                f.write(str(wordL))
f.close()
