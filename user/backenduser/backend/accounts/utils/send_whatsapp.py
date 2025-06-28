import requests

def format_phone(phone):
    if phone.startswith('0'):
        return '+234' + phone[1:]
    return phone


def send_whatsapp(phone: str, message: str):
    url = "https://api.ultramsg.com/instance128582/messages/chat"

    payload = {
        "token": "bd4yyce40e1253q8",
        "to": format_phone(phone),
        "body": message,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.json()
