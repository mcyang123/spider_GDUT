该程序用于获取GDUT账号
try_account.py为主程序，需要输入两个参数，第一个为开始的账号，第二个为结束的账号（不会尝试第二个账号）
该程序调用了image2text.py,它用于将图片转换成字符串
get_code.py，获取一定的验证码图片，并对其进行统一化处理,图片存放在pic文件夹中
get_feature.py，提取上述图片集的特征，为每个字符生成特征数据用于识别
gea2.txt：特征数据
account.txt：获取的账号