import threading
import requests
import pandas as pd
from measurements import measurements
from os.path import exists
from datetime import datetime
import csv
import threading


def csv(datas, MAC, file = "data"):
    print("csv basladi")
    name = ["Id", "createdAt", "MEASUREMENT_START_TIME", "MEASUREMENT_START_UNIXTIME", "CHUNK_COUNT", "CALIBRATED_SAMPLINGRATE", "device", "gateway"]
    value = [i for i in datas[0]]
    for i in range(1, len(datas)):
        name.append(datas[i][0])
        value.append(datas[i][1])
        
    dict = {"name" : name, "value" : value}
    df = pd.DataFrame(dict["value"])
    df = df.T
    df_names = pd.DataFrame(dict["name"])
    df_names = df_names.T
    
    date_time = str(datetime.now()).replace(" ", "_")
    date_time = date_time[:13]

    MAC = MAC.replace(":","_")
    #print(datas)
    file_name = MAC + "_" # + date_time
    #path = 'C:\\Users\\doguk\\Desktop\\data\\'
    
    
    #*********************
    file_exists = exists(fr"C:/Users/doguk/Desktop/data/{file}/{file_name}.csv")
    
    if(file_exists == False):
        df_names.to_csv(fr"C:/Users/doguk/Desktop/data/{file}/{file_name}.csv", mode = "a", index = False, header = False, sep =',')
    #*********************

    df.to_csv(fr"C:/Users/doguk/Desktop/data/{file}/{file_name}.csv", mode = "a", index = False, header = False, sep =',')
    print("csv bitti")
    
    
def getJson(mac,  gelen_data):

    print(f'getjsondayim gelen mac = {mac}')
    notConnected = []
    URL = 'http://172.16.0.39:3000/device/'+ mac + '/measurement'
    print(f'getjsondayim gelen url = {URL}')
    data = requests.post(url = URL, headers = {"Content-Type": "application/json"}, json = gelen_data)
    """
    data = {
         "_id": "62529ff8e1a9bb0012714d1b",
         "createdAt": "2022-04-10T09:14:32.034Z",
         "metadata": {
             "STAT": {
                 "MEASUREMENT_START_TIME": "07:47:58:10:04:2022",
                 "MEASUREMENT_START_UNIXTIME": 1649576875,
                 "CHUNK_COUNT": 4,
                 "CALIBRATED_SAMPLINGRATE": 13360
             },
             "TELEMETRY": [
                 {
                     "NAME": "TEMPERATURE",
                     "VALUE": 24.78
                 },
                 {
                     "NAME": "CLEARANCE",
                     "VALUE": [
                         1.0423772493632315,
                         1.3342012559817278,
                         1.3802208108552754
                     ]
                 },
                 {
                     "NAME": "CREST",
                     "VALUE": [
                         115.20978001212092,
                         18.675292700514913,
                         18.597839539603406
                     ]
                 },
                 {
                     "NAME": "GRMS",
                     "VALUE": [
                         0.07638364306825231,
                         0.031276323317492784,
                         0.031466905482878685
                     ]
                 },
                 {
                     "NAME": "KURTOSIS",
                     "VALUE": [
                         3.0415954166036636,
                         3.082881834510505,
                         3.4820448763885117
                     ]
                 },
                 {
                     "NAME": "SKEWNESS",
                     "VALUE": [
                         0.03630682414950462,
                         0.010537915244593157,
                         -0.024575733670141178
                     ]
                 }
             ]
         },
         "device": "CA:B8:31:00:00:64",
         "gateway": "CA:B8:29:00:00:01",
         }
         """
    data = data.json()
    try:
        print("getjson try ")
        id = data["_id"]
        createdAt = data["createdAt"]
        MEASUREMENT_START_TIME = data["metadata"]["STAT"]["MEASUREMENT_START_TIME"]
        MEASUREMENT_START_UNIXTIME = data["metadata"]["STAT"]["MEASUREMENT_START_UNIXTIME"]
        CHUNK_COUNT = data["metadata"]["STAT"]["CHUNK_COUNT"]
        CALIBRATED_SAMPLINGRATE = data["metadata"]["STAT"]["CALIBRATED_SAMPLINGRATE"]
        device = data["device"]
        gateway = data["gateway"]
        TELEMETRY = data["metadata"]["TELEMETRY"]
    
        measurements_ = measurements(id = id, createdAt = createdAt, MEASUREMENT_START_TIME = MEASUREMENT_START_TIME,  MEASUREMENT_START_UNIXTIME = MEASUREMENT_START_UNIXTIME, CHUNK_COUNT = CHUNK_COUNT, CALIBRATED_SAMPLINGRATE = CALIBRATED_SAMPLINGRATE, device = device, gateway = gateway, TELEMETRY = TELEMETRY)
        datas = measurements_.data()
        csv(datas = datas, MAC = mac)
        print("getjson try bitiş")
    except:
        print("getjson except ")
        pass

def getJson_threading(mac):
    print("getJson2 getJson_threading")
    getJson(mac = mac, gelen_data = {'accelerometerRange':2, 'samplingRate':12800, 'sampleSize':20000})
    print("getJson2 getJson_threading bitiş")

def start_threading(macs):
    print("getJson2 start_threading")
    start(macs = macs)
    print("getJson2 start_threading bitiş")

def mac_data(url):
    list_data = []
    data = ((requests.get(url = url)).json())
    
    for i in range(0, len(data["devices"])):
        list_data.append(data['devices'][i]['macAddress'])

    return list_data
def mac_data_from_api(url):
    data = ((requests.get(url = url)).json())
    return data["mac"]

    
def check_bool(tick1 : bool = 0, tick2 : bool = 0, tick3 : bool = 0):

    print(tick1," ", tick2, " ",tick3)
    return tick1, tick2, tick3

def start(macs = "CA:B8:31:00:00:03"):
    
    macs = macs["mac"]
    print(f'gelen mac adresi = {macs}')
    tick1, tick2, tick3 = check_bool()

    ##url = 'http://172.16.0.39:3000/device/'
    #url = "http://127.0.0.1:5000/mac/0"
    ##macs = mac_data(url)
    #macs = mac_data_from_api(url)
    
    # tick2 dakika boyunca
    # tick3 zaman tetiklemeli dakika boyunca

    # kaç dakika boyunca sample alınacak
    time_sample = 2
    # kaç dakikada bir sample alınacak
    time_c_pl = 1    
    # program başlangic saati "." olmadan
    starting_time = 1629
    
    i = 0
    while(i<1):
            try:
                print("basladi")
                t = threading.Thread(target=getJson_threading(macs), args = (macs, ))
                t.start()
                print("bitti")
            except:
                print("except")     
                pass
            i+=1
            print("Bitti2")
    """
    if (tick1 == True):
        for mac in macs:
            try:
                
                t = threading.Thread(target=getJson_threading(mac), args = (mac, ))
                t.start()
            except:     
                pass
    
    
    if(tick2 == True):
        
        
        date_time = str(datetime.now()).replace(" ", "_").replace(":","")
        date_time = date_time[11:15]
        time_c = int(date_time)
        time_s = int(date_time)
        
        while(True):
            date_time = str(datetime.now()).replace(" ", "_").replace(":","")
            date_time = date_time[11:15]

            if(time_c == time_s + time_sample):
                
                break
            
            elif(int(date_time) == time_c): 
                    for mac in macs:
                        try:
                                
                            t = threading.Thread(target=getJson_threading(mac), args = (mac, ))
                            t.start()
                        except:     
                            pass
                    time_c += time_c_pl
                    print("tick2")
            

    
    if(tick3 == True):

        
        
        
        while(True):
            
            date_time = str(datetime.now()).replace(" ", "_").replace(":","")
            date_time = date_time[11:15]
            time_c = int(date_time)
            
            if(int(date_time) == starting_time):
                
                while(True):
                    date_time = str(datetime.now()).replace(" ", "_").replace(":","")
                    date_time = date_time[11:15]
                    if(time_c == time_s + time_sample):
                
                        break
            
                    elif(int(date_time) == time_c): 
                            for mac in macs:
                                try:
                                
                                    t = threading.Thread(target=getJson_threading(mac), args = (mac, ))
                                    t.start()
                                except:     
                                    pass
                            time_c += time_c_pl
                break
"""


    

"""if __name__ == "__main__":
    main(macs = {"mac":"CA:B8:31:00:00:30"})"""