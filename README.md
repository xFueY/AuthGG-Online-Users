# AuthGG Online Users Counter
Python Flask application for counting users, currently using your application.

### Endpoints

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
