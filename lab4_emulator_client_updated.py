# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np


#TODO 1: modify the following parameters
#Starting and end index, modify this
device_st = 1
device_end = 5

#Path to the dataset, modify this
data_path = "data2/vehicle{}.csv"

#Path to your certificates, modify this
certificate_formatter = "Green_Grass_Config/device_{}/device_{}_certificate.pem.crt"
key_formatter = "Green_Grass_Config/device_{}/device_{}_private.pem.key"

#certificate_formatter = "Green_Grass_Config/certificate.pem.crt"
#key_formatter = "Green_Grass_Config/private.pem.crt"


class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address
        self.client.configureEndpoint("aiz3ikhw59kmt-ats.iot.us-west-2.amazonaws.com", 8883)
        self.client.configureCredentials("Green_Grass_Config/device_0/AmazonRootCA1 (1).pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        #TODO3: fill in the function to show your received message
        print("client {} received payload {} from topic {}".format(self.device_id, message.payload, message.topic))


    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass


    def publish(self, Payload="payload"):
        #TODO4: fill in this function for your publish
        #self.client.subscribeAsync("TestTopic1", 0, ackCallback=self.customSubackCallback)
        
        #self.client.publishAsync("TestTopic2", Payload, 0, ackCallback=self.customPubackCallback)
        self.client.publishAsync("vehicle/CO2", Payload, 0, ackCallback=self.customPubackCallback)




print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))
    data.append(a)

print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end):
    client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))
    #print(client)
    client.client.connect()
    #print(tst)
    clients.append(client)
    #print(clients)
print(clients)

# def format_line (datid,co2,noise,):
    # json_form = "{\n"
    # json_form = json_form + " ID: '" +data
    
# k =0
# while True:
min_row = min([x.shape[0] for x in data])
max_row = max([x.shape[0] for x in data])
print(min_row,max_row)
print("adding rows")
for k in range(0,max_row):
    # print("send now?")
    # x = input()
    # if x == "s":
        
        # for i,c in enumerate(clients):
        
            # if k > data[i].shape[0]:
                # continue
                
            # cd = data[i].iloc[k,].to_json()
            # #print(cd)
            # tst = c.publish(Payload=cd)
            # #print(tst)
        
    for i,c in enumerate(clients):
    
        if k >= data[i].shape[0]:
            continue
        else:
            cd = data[i].iloc[k,].to_json()

            tst = c.publish(Payload=cd)


    # elif x == "d":
        # for c in clients:
            # c.client.disconnect()
        # print("All devices disconnected")
        # exit()
    # else:
        # print("wrong key pressed")

    #time.sleep(3)
print("all_done")
for c in clients:
    c.client.disconnect()
print("All devices disconnected")
exit()

# test message:
# {
  # "ID": "1",
  # "CO2": 2624.72,
  # "fuel": 1.13,
  # "noise": 55.94
# }