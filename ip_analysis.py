import requests

def analyze_ip(ip_address):
    # IP adresi ile ilgili lokasyon bilgisini al
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'fail':
        return {"status": "fail", "message": "IP address not found"}

    location = {
        "ip": ip_address,
        "city": data.get('city', 'N/A'),
        "region": data.get('regionName', 'N/A'),
        "country": data.get('country', 'N/A'),
        "isp": data.get('isp', 'N/A'),
        "threat_level": "Low"  # Burada daha ayrıntılı bir analiz ekleyebilirsiniz
    }

    return {"status": "success", "data": location}

