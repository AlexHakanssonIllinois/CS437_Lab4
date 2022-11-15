import json
import logging
import sys
import pandas

import greengrasssdk

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# SDK Client
client = greengrasssdk.client("iot-data")

# Counter
my_counter = 0
def lambda_handler(event, context):
    global my_counter
    #TODO1: Get your data
    dat = pd.read.csv("data_store.csv")


    #TODO2: Calculate max CO2 emission
    co2 = dat.vehicle_co2.max()

    #TODO3: Return the result
    client.publish(
        topic="hello/world/counter",
        payload=json.dumps(
            {"message": "CO2 max is "+str(co2)}
        ),
    )
    my_counter += 1

    return