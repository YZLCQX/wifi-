import pywifi  #破解wifi
import time

#扫描AP 判断wifi是否存在
def scann(wifi,ssid):
    wifi.scan()
    time.sleep(3)
    re = wifi.scan_results()
    r = []
    for i in range(len(re)):
        r.append(re[i].ssid)
    if ssid in r:
        return 0
    return -1

if __name__ == '__main__': 
    wifi_e = pywifi.PyWiFi()
    
    wifi = wifi_e.interfaces()[0]

    if scann(wifi,'XT'):
        print('no')
    else:
        print("yes")