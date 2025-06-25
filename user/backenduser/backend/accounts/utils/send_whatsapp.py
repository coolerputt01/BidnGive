import requests

def send_whatsapp(phone: str, message: str):
    url = "https://api.ultramsg.com/instance128107/messages/chat"

    payload = {
        "token": "7zua6ekminxv7lsh",
        "to": phone,  # e.g., "+2349065978408"
        "body": message,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.json()
