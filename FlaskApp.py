from flask import Flask, request
import datetime
import math
import time
import threading
import requests

# Customize Variables
Timeout = 60 # Amount of seconds to go let the user go without sending a request before the user will be counted as offline.
AdminAPIKey = "" # Not Auth.GG admin api key, just whatever you wanna use for the admin endpoint here.
ReturnOnlineToPublic = True # Whether or not to include the online user count in the response for the users to see.
AllowManualDelete = True # Whether or not to allow counting users as offline by sending a "DELETE" request.
UseAuthGGAdmin = True # Whether or not to use the Auth.GG feature implemented, that returns the online users details in the admin endpoint.
AuthGGAdminAPIKey = "" # Auth.GG Admin/Authorization key if UseAuthGGAdmin is set to True, not needed otherwise.

OnlineUsers = {}

App = Flask(__name__)
App.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
App.config['JSON_SORT_KEYS'] = False


def updateOnline():
    global OnlineUsers
    while True:
        Timestamp = math.floor(datetime.datetime.utcnow().timestamp())
        OnlineUsers = {x : y for x, y in OnlineUsers.items() if y + Timeout >= Timestamp}
        time.sleep(60)


UpdateThread = threading.Thread(target=updateOnline)
UpdateThread.start()


@App.route("/admin/", methods=["GET"])
def Main_Admin():
    global OnlineUsers
    API = request.args.get("api")

    if API == AdminAPIKey:

        if UseAuthGGAdmin == True:
            AllUsers = requests.get(f"https://developers.auth.gg/USERS/?type=fetchall&authorization={AuthGGAdminAPIKey}").json()
            print(AllUsers)
            OnlineUsersInformation = []
            for x, y in AllUsers.items():
                if y['username'].lower() + ":" + y['hwid'] in OnlineUsers:
                    OnlineUsersInformation.append(y)

            return {"online" : len(OnlineUsers), "users" : OnlineUsersInformation}

        return {"online" : len(OnlineUsers), "users" : [x for x in OnlineUsers]}

    return {}


@App.route("/online/", methods=["GET", "POST", "DELETE"])
def Main_Online():
    global OnlineUsers

    if request.method == "GET":
        if ReturnOnlineToPublic == True:
            return {"online" : len(OnlineUsers)}
        else:
            return {}

    elif request.method == "POST":
        HWID = request.form.get("hwid")

        if HWID == None:
            if ReturnOnlineToPublic == True:
                return {"online" : len(OnlineUsers)}
            else:
                return {}

        OnlineUsers[HWID] = math.floor(datetime.datetime.utcnow().timestamp())

        if ReturnOnlineToPublic == True:
            return {"online" : len(OnlineUsers)}
        else:
            return {}

    elif request.method == "DELETE" and AllowManualDelete:
        HWID = request.form.get("hwid")

        if HWID == None:
            if ReturnOnlineToPublic == True:
                return {"online" : len(OnlineUsers)}
            else:
                return {}

        if HWID in OnlineUsers:
            del OnlineUsers[HWID]

        if ReturnOnlineToPublic == True:
            return {"online" : len(OnlineUsers)}
        else:
            return {}

    else:
        return {}


if __name__ == "__main__":
    App.run(port=80)
