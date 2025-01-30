import requests

def analyze_mac(mac_address):
    # MAC adresinden üretici bilgisini almak için API
    url = f"https://macvendors.co/api/{mac_address}"
    headers = {
        'Authorization': 'Bearer <eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImp0aSI6IjM0NDU0ODQ0LWU3MzAtNDdmMy1iNmMwLTZhODllN2FmOWJlMyJ9.eyJpc3MiOiJtYWN2ZW5kb3JzIiwiYXVkIjoibWFjdmVuZG9ycyIsImp0aSI6IjM0NDU0ODQ0LWU3MzAtNDdmMy1iNmMwLTZhODllN2FmOWJlMyIsImlhdCI6MTczODI0ODg2NCwiZXhwIjoyMDUyNzQ0ODY0LCJzdWIiOiIxNTUwMSIsInR5cCI6ImFjY2VzcyJ9.ppz3D1xAuhp4Jeoi7CkwxfRWS2b_LoavVa5eBWKK0oYgRrhPgplqt97Q8ZcTOVo7BWyLMlMS09jJVeTjQyDHFg>'  # API anahtarınızı burada girin
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if 'error' in data:
        return {"status": "fail", "message": "MAC address not found"}

    vendor_info = {
        "mac": mac_address,
        "vendor": data.get('company', 'N/A'),
        "device_category": "N/A"  # Burada daha fazla kategori ekleyebilirsiniz
    }

    return {"status": "success", "data": vendor_info}

