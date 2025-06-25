import requests

def send_whatsapp(phone, message):
    url = "https://api.ultramsg.com/instanceXXXX/messages/chat"
    payload = {
        "to": f"{phone}",
        "body": message,
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "token": "your_ultramsg_token"
    }
    return requests.post(url, data=payload, headers=headers)
