import whois
from mac_vendor_lookup import MacLookup
import json
from datetime import datetime
import logging
from typing import Dict, Optional, Union

class NetworkAnalyzer:
    def __init__(self):
        self.mac_lookup = MacLookup()
        self.mac_lookup.load_vendors()
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='network_analyzer.log'
        )
    
    def get_mac_vendor(self, mac_address: str) -> Dict[str, str]:
        """
        MAC adresinden üretici bilgisini alır.
        
        Args:
            mac_address: MAC adresi (örn: "00:00:00:00:00:00")
            
        Returns:
            Dict containing vendor information
        """
        try:
            vendor = self.mac_lookup.lookup(mac_address)
            result = {
                "mac_address": mac_address,
                "vendor": vendor,
                "timestamp": datetime.now().isoformat()
            }
            logging.info(f"MAC vendor found: {result}")
            return result
        except Exception as e:
            logging.error(f"MAC lookup error for {mac_address}: {str(e)}")
            return {
                "mac_address": mac_address,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def get_whois_info(self, domain: str) -> Dict[str, Union[str, dict]]:
        """
        Domain veya IP adresi için WHOIS bilgilerini alır.
        
        Args:
            domain: Domain adı veya IP adresi
            
        Returns:
            Dict containing WHOIS information
        """
        try:
            w = whois.whois(domain)
            result = {
                "domain": domain,
                "registrar": w.registrar,
                "creation_date": self._format_date(w.creation_date),
                "expiration_date": self._format_date(w.expiration_date),
                "name_servers": w.name_servers if isinstance(w.name_servers, list) else [w.name_servers],
                "status": w.status if isinstance(w.status, list) else [w.status],
                "emails": w.emails if isinstance(w.emails, list) else [w.emails],
                "raw": w.text,
                "timestamp": datetime.now().isoformat()
            }
            logging.info(f"WHOIS info retrieved for {domain}")
            return result
        except Exception as e:
            logging.error(f"WHOIS lookup error for {domain}: {str(e)}")
            return {
                "domain": domain,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _format_date(self, date) -> Optional[str]:
        """Tarihleri ISO format'a çevirir."""
        if isinstance(date, list):
            date = date[0]
        return date.isoformat() if date else None
    
    def save_to_json(self, data: dict, filename: str):
        """Sonuçları JSON dosyasına kaydeder."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logging.info(f"Data saved to {filename}")
        except Exception as e:
            logging.error(f"Error saving to {filename}: {str(e)}")

# Ana program
if __name__ == "__main__":
    analyzer = NetworkAnalyzer()
    
    # MAC adresi testi
    mac_result = analyzer.get_mac_vendor("00:1A:11:22:33:44")
    print("MAC Sonucu:", mac_result)
    
    # WHOIS testi
    whois_result = analyzer.get_whois_info("google.com")
    print("WHOIS Sonucu:", whois_result)
    
    # Sonuçları JSON dosyasına kaydet
    analyzer.save_to_json(whois_result, "whois_results.json")
