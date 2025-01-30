from ip_analysis import analyze_ip
from mac_analysis import analyze_mac

# Test IP ve MAC adresi
ip = "8.8.8.8"  # Google DNS IP adresi
mac = "44:38:39:ff:ef:57"  # Örnek MAC adresi

# IP Analizini test et
ip_result = analyze_ip(ip)
print(ip_result)

# MAC Analizini test et
mac_result = analyze_mac(mac)
print(mac_result)

