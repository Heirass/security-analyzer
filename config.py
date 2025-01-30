import whois
from mac_vendor_lookup import MacLookup
import json
from datetime import datetime
import logging
from typing import Dict, Optional, Union
import sys
import os
from time import sleep

class NetworkAnalyzer:
    def __init__(self):
        self.mac_lookup = MacLookup()
        self.mac_lookup.load_vendors()
        self.setup_logging()
    
    # ... (önceki NetworkAnalyzer metodları aynı kalacak) ...
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_menu(self):
        self.clear_screen()
        print("=" * 50)
        print("     MAC VE WHOIS ANALİZ SİSTEMİ")
        print("=" * 50)
        print("\n1. MAC Adresi Sorgula")
        print("2. WHOIS Bilgisi Sorgula")
        print("3. Toplu MAC Adresi Sorgula")
        print("4. Toplu Domain Sorgula")
        print("5. Son Sorguları Göster")
        print("6. Sonuçları Dışa Aktar")
        print("0. Çıkış")
        print("\n" + "=" * 50)
    
    def get_user_input(self, prompt: str) -> str:
        try:
            return input(f"\n{prompt}: ").strip()
        except KeyboardInterrupt:
            print("\nİşlem iptal edildi.")
            return ""
    
    def bulk_mac_lookup(self, mac_file: str) -> list:
        results = []
        try:
            with open(mac_file, 'r') as f:
                mac_addresses = f.read().splitlines()
            
            for mac in mac_addresses:
                if mac.strip():  # Boş satırları atla
                    result = self.get_mac_vendor(mac.strip())
                    results.append(result)
                    print(f"İşleniyor: {mac} -> {result.get('vendor', 'Bulunamadı')}")
            return results
        except FileNotFoundError:
            print(f"Hata: {mac_file} dosyası bulunamadı!")
            return []
    
    def bulk_whois_lookup(self, domain_file: str) -> list:
        results = []
        try:
            with open(domain_file, 'r') as f:
                domains = f.read().splitlines()
            
            for domain in domains:
                if domain.strip():  # Boş satırları atla
                    result = self.get_whois_info(domain.strip())
                    results.append(result)
                    print(f"İşleniyor: {domain}")
            return results
        except FileNotFoundError:
            print(f"Hata: {domain_file} dosyası bulunamadı!")
            return []
    
    def run_interactive(self):
        while True:
            self.print_menu()
            choice = self.get_user_input("Seçiminiz")
            
            if choice == "0":
                print("\nProgram kapatılıyor...")
                break
            
            elif choice == "1":
                mac = self.get_user_input("MAC adresini girin (örn: 00:1A:11:22:33:44)")
                if mac:
                    result = self.get_mac_vendor(mac)
                    print("\nSonuç:")
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                    input("\nDevam etmek için Enter'a basın...")
            
            elif choice == "2":
                domain = self.get_user_input("Domain veya IP adresini girin")
                if domain:
                    result = self.get_whois_info(domain)
                    print("\nSonuç:")
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                    input("\nDevam etmek için Enter'a basın...")
            
            elif choice == "3":
                file_path = self.get_user_input("MAC adresleri içeren dosyanın yolunu girin")
                if file_path:
                    results = self.bulk_mac_lookup(file_path)
                    if results:
                        self.save_to_json(results, "bulk_mac_results.json")
                        print(f"\nSonuçlar bulk_mac_results.json dosyasına kaydedildi.")
                    input("\nDevam etmek için Enter'a basın...")
            
            elif choice == "4":
                file_path = self.get_user_input("Domain listesi içeren dosyanın yolunu girin")
                if file_path:
                    results = self.bulk_whois_lookup(file_path)
                    if results:
                        self.save_to_json(results, "bulk_whois_results.json")
                        print(f"\nSonuçlar bulk_whois_results.json dosyasına kaydedildi.")
                    input("\nDevam etmek için Enter'a basın...")
            
            elif choice == "5":
                try:
                    with open('network_analyzer.log', 'r') as f:
                        print("\nSon Sorgular:")
                        print(f.read())
                except FileNotFoundError:
                    print("\nHenüz hiç sorgu yapılmamış!")
                input("\nDevam etmek için Enter'a basın...")
            
            elif choice == "6":
                filename = self.get_user_input("Sonuçların kaydedileceği dosya adını girin (örn: results.json)")
                if filename:
                    try:
                        with open('network_analyzer.log', 'r') as f:
                            log_data = f.readlines()
                        self.save_to_json({"logs": log_data}, filename)
                        print(f"\nSonuçlar {filename} dosyasına kaydedildi.")
                    except FileNotFoundError:
                        print("\nDışa aktarılacak veri bulunamadı!")
                input("\nDevam etmek için Enter'a basın...")

if __name__ == "__main__":
    analyzer = NetworkAnalyzer()
    analyzer.run_interactive()
