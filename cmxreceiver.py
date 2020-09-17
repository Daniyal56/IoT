#!flask/bin/python


# Libraries
from pprint import pprint
from flask import Flask
from flask import json
from flask import request
from flask import render_template
import sys
import getopt
import json
from meraki_sdk.meraki_sdk_client import MerakiSdkClient
import pandas as pd
import requests

dashboard = MerakiSdkClient(
    x_cisco_meraki_api_key='07d4b7f273f84f94f6bc4842207f2eac06276943')

apdev = dashboard.devices.get_network_devices(
    network_id='L_667095694804287796')


############## USER DEFINED SETTINGS ###############
# MERAKI SETTINGS
validator = "EnterYourValidator"
secret = "EnterYourSecret"
version = "2.1"  # This code was written to support the CMX JSON version specified
locationdata = "Location Data Holder"
####################################################
app = Flask(__name__)


# Respond to Meraki with validator


@app.route("/", methods=["GET"])
def get_validator():
    print("validator sent to: ", request.environ["REMOTE_ADDR"])
    return validator


# Accept CMX JSON POST


@app.route("/", methods=["POST"])
def get_locationJSON():
    global locationdata

    if not request.json or not "data" in request.json:
        return ("invalid data", 400)

    locationdata = request.json
    pprint(locationdata, indent=1)
    print("Received POST from ", request.environ["REMOTE_ADDR"])

    # Verify secret
    if locationdata["secret"] != secret:
        print("secret invalid:", locationdata["secret"])
        return ("invalid secret", 403)

    else:
        print("secret verified: ", locationdata["secret"])

    # Verify version
    if locationdata["version"] != version:
        print("invalid version")
        return ("invalid version", 400)

    else:
        print("version verified: ", locationdata["version"])

    # Determine device type
    if locationdata["type"] == "DevicesSeen":
        print("WiFi Devices Seen")
    elif locationdata["type"] == "BluetoothDevicesSeen":
        print("Bluetooth Devices Seen")
    else:
        print("Unknown Device 'type'")
        return ("invalid device type", 403)

    value = {'items': locationdata['data']['observations']}

    val = pd.DataFrame(value['items'])

    for i in range(len(value['items'])):
        n = dict(apfloor=locationdata['data']['apFloors'], apmac=locationdata['data']['apMac'], clmac=str(val['clientMac'][i]), lat=float(val['location'][i]['lat']), lng=float(val['location']
                                                                                                                                                                                [i]['lng']), unc=float(val['location'][i]['unc']), angx=float(val['location'][i]['x'][0]), angy=float(val['location'][i]['y'][0]), clname=str(val['name'][i]))
        x = requests.post(
            'http://151.80.237.86:1251/ords/zkt/aitrk/trk', data=n)

    # Posting to our database
      # Converting data into Json

    # Return success message
    return "Location Scanning POST Received"


@app.route("/go", methods=["GET"])
def get_go():
    return render_template("index.html", **locals())


@app.route("/clients/", methods=["GET", "POST"])
def get_clients():
    global locationdata
    with open('data.json', 'w') as f:
        json.dumps(f.write(str(locationdata)), skipkeys=True)

    if locationdata != "Location Data Holder":

        # pprint(locationdata["data"]["observations"], indent=1)
        # apMac = locationdata['apMac']
        # apFloors = locationdata['apFloors']
        # name = locationdata['name']
        # pprint('for testing'+locationdata["data"]["observations"], indent=1)

        return json.dumps(locationdata["data"]["observations"])
        # return json.dumps(apMac)
        # return json.dumps(apFloors)
        # return json.dumps(name)

    return ""
##################################################################################
#Change in Code


@app.route("/apmac/", methods=["GET", "POST"])
def get_ap():
    global locationdata
    return json.dumps(locationdata['data'])

    # pprint(locationdata["data"]["observations"], indent=1)
    # apMac = locationdata['apMac']
    # apFloors = locationdata['apFloors']
    # name = locationdata['name']
    # pprint('for testing'+locationdata["data"]["observations"], indent=1)

    return ""
####################################################################################


@app.route("/clients/<clientMac>", methods=["GET", "POST"])
def get_individualclients(clientMac):
    global locationdata
    for client in locationdata["data"]["observations"]:
        if client["clientMac"] == clientMac:
            return json.dumps(client)

    return ""


# @app.route("/db/", methods=['GET', 'POST'])
# def func():
#     global locationdata
#     value = {'items': []}
#     for client in locationdata['data']['observations']:
#         value['items'].append({'CLMAC': client['clientMac'], 'LAT': client['location']['lat'], 'LNG': client['location']['lng'],
#                                'UNC': client['location']['unc'], 'ANGX': client['location']['x'][0], 'ANGY': client['location']['y'][0], 'CLNAME': client['name']})
#         for index, val in enumerate(value['items']):
#             x = requests.post(
#                 'http://151.80.237.86:1251/ords/zkt/aitrk/trk', json=val)


# requests.post()


# Launch application with supplied arguments


def main(argv):
    global validator
    global secret

    try:
        opts, args = getopt.getopt(argv, "hv:s:", ["validator=", "secret="])
    except getopt.GetoptError:
        print("cmxreceiver.py -v <validator> -s <secret>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("locationscanningreceiver.py -v <validator> -s <secret>")
            sys.exit()
        elif opt in ("-v", "--validator"):
            validator = arg
        elif opt in ("-s", "--secret"):
            secret = arg

    print("validator: " + validator)
    print("secret: " + secret)


if __name__ == "__main__":
    main(sys.argv[1:])
    app.run(port=5000, debug=False)
