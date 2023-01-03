


from telnetlib import Telnet


class measurements:
    def __init__(self, id, createdAt,  MEASUREMENT_START_TIME,  MEASUREMENT_START_UNIXTIME, CHUNK_COUNT, CALIBRATED_SAMPLINGRATE , device, gateway, TELEMETRY):
        self.id = id
        self.createdAt = createdAt
        self.MEASUREMENT_START_TIME = MEASUREMENT_START_TIME
        self.MEASUREMENT_START_UNIXTIME = MEASUREMENT_START_UNIXTIME
        self.CHUNK_COUNT = CHUNK_COUNT
        self.CALIBRATED_SAMPLINGRATE = CALIBRATED_SAMPLINGRATE
        self.device = device
        self.gateway = gateway
        self.TELEMETRY = TELEMETRY
        self.num_var = {}
        #self.telemetry = []
        self.datas = []
        
        
        for i in range(len(TELEMETRY)):
            
            if (TELEMETRY[i]["NAME"] == "TEMPERATURE"): 

                name = TELEMETRY[i]["NAME"]
                self.num_var[name] = TELEMETRY[i]["VALUE"]
            else:
                
                for j in range(len(TELEMETRY[i]["VALUE"])):
                    name = TELEMETRY[i]["NAME"] + "_" + str(j+1)
                    self.num_var[name] = TELEMETRY[i]["VALUE"][j]

        
    def data(self):
        
        self.datas.append([self.id, self.createdAt, self.MEASUREMENT_START_TIME,  self.MEASUREMENT_START_UNIXTIME, self.CHUNK_COUNT, self.CALIBRATED_SAMPLINGRATE , self.device, self.gateway])
        for i,j in self.num_var.items():
            self.datas.append([i, j])
        return self.datas
