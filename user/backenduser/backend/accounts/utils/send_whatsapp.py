import requests

def send_whatsapp(phone: str, message: str):
    url = "https://api.ultramsg.com/instance128107/messages/chat"

    payload = {
        "token": "bd4yyce40e1253q8",
        "to": phone,
        "body": message,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.json()
