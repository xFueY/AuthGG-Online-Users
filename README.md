# AuthGG Online Users Counter
Python Flask application for counting users, currently using your application.

If you wanna use this, make sure to edit the variables to your requirements in the `FlaskApp.py` file.
<br>
Options are listed below.

# Options

| Option | Type | Description |
| --- | --- | --- |
| Timeout | Integer | Amount of seconds to go let the user go without sending a request, before the user will be counted as offline. |
| AdminAPIKey | String | Not Auth.GG admin api key, just whatever you wanna use for the admin endpoint here. |
| ReturnOnlineToPublic | Boolean | Whether or not to include the online user count in the response for the users to see. |
| AllowManualDelete | Boolean | Whether or not to allow counting users as offline by sending a "DELETE" request. |
| UseAuthGGAdmin | Boolean | Whether or not to use the Auth.GG feature implemented, that returns the online users details in the admin endpoint. |
| AuthGGAdminAPIKey | String | Auth.GG Admin/Authorization key if UseAuthGGAdmin is set to True, not needed otherwise. |

# Endpoints

| Method  | Endpoint |
| ------------- | -- |
| GET  | /online/    |
| POST  | /online/   |
| DELETE  | /online/ |
| GET | /admin/      |

**Note:** If `ReturnOnlineToPublic` is set to `False`, the `/online/` endpoint will return an empty json dictionary (`{}`)

## GET /online/
This endpoint will return the current online counter, if `ReturnOnlineToPublic` is set to `True`

Returns:
```json
{
  "online": 1
}
```

## POST /online/
This endpoint will register a user as online.
<br>
Requires `hwid` key in body, containing the users username in lowercase and hwid (hwid as is) like this: `username:hwid`.
<br>
(Like this: `xfuey:XXXXXXXX-XXX-XXXX-XXXX-XXXXXXXXXXXXXX`)

Returns:
```json
{
  "online": 1
}
```

## DELETE /online/
This endpoint will remove the user from the online users, if `AllowManualDelete` is set to `True`.
<br>
Requires `hwid` key in body, containing the users username in lowercase and hwid (hwid as is) like this: `username:hwid`.
<br>
(Like this: `xfuey:XXXXXXXX-XXX-XXXX-XXXX-XXXXXXXXXXXXXX`)

Returns:
```json
{
  "online": 0
}
```

## GET /admin/
This endpoint will return a list of users currently online.
<br>
If `UseAuthGGAdmin` is set to `True`, it will return a list of the Auth.GG users currently online.

`UseAuthGGAdmin = True` returns:
```json
{
  "online": 1, 
  "users": [
    {
      "username": "xFueY", 
      "email": "xFueY", 
      "hwid": "XXXXXXXX-XXX-XXXX-XXXX-XXXXXXXXXXXXXX", 
      "rank": "0", 
      "variable": "", 
      "lastlogin": "", 
      "lastip": "", 
      "expiry_date": "2295-03-07 07:29:20"
    }
  ]
}
```

`UseAuthGGAdmin = False` returns:
```json
{
  "online": 1, 
  "users": [
    "xfuey:XXXXXXXX-XXX-XXXX-XXXX-XXXXXXXXXXXXXX"
  ]
}
```


# Python Application Example
```python
import time
import threading
import requests

def PingOnline(Username : str, HWID : str):
    while True:
        print("Sending Request")
        r = requests.post("http://localhost/online/", data={"hwid" : Username.lower() + ":" + HWID.lower()})
        print("Request Sent")
        time.sleep(30)


# Run this once user has logged in.
t = threading.Thread(target=PingOnline, args=(Username, HWID, ))
t.start()
```


If you have any questions, feel free to contact me on Discord: `xFueY#7575`
