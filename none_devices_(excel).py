import time
import pandas as pd
from ciscoaxl import axl
from zeep import Client, helpers
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CUCM_IP = 'ip_addr'
USERNAME = 'user.name'
PASSWORD = 'your_password'

def none_devices_to_excel():
    try:
        # 1. AXL Bağlantısı
        ucm = axl(username=USERNAME, password=PASSWORD, cucm=CUCM_IP, cucm_version='12.5')
        print("AXL: Cihaz listesi çekiliyor.")
        all_phones = ucm.get_phones()
        device_names = [p['name'] for p in all_phones]
        total_count = len(device_names)
        print(f"BAŞARILI: {total_count} cihaz bulundu.")

        # 2. RISPort Bağlantısı
        ris_wsdl = f"https://{CUCM_IP}:8443/realtimeservice2/services/RISService70?wsdl"
        ris_endpoint = f"https://{CUCM_IP}:8443/realtimeservice2/services/RISService70"
        session = Session()
        session.verify = False
        session.auth = HTTPBasicAuth(USERNAME, PASSWORD)
        ris_transport = Transport(session=session, timeout=30)
        ris_client = Client(ris_wsdl, transport=ris_transport)
        ris_service = ris_client.create_service('{http://schemas.cisco.com/ast/soap}RisBinding', ris_endpoint)

        chunk_size = 100
        none_devices_list = []  # Excel'e yazılacak liste

        print("\nTaranıyor... Lütfen bekleyin (Dakikada ~13-15 sorgu yapılır)")

        for i in range(0, total_count, chunk_size):
            if i > 0:
                time.sleep(4.5)  # Rate limit koruması

            chunk = device_names[i:i + chunk_size]

            criteria = {
                'MaxReturnedDevices': chunk_size,
                'DeviceClass': 'Any',
                'Model': 255,
                'Status': 'Any',
                'NodeName': "",
                'SelectBy': 'Name',
                'SelectItems': {'item': [{'Item': name} for name in chunk]},
                'Protocol': 'Any',
                'DownloadStatus': 'Any'
            }

            try:
                ris_response = ris_service.selectCmDevice(StateInfo="", CmSelectionCriteria=criteria)
                ris_data = helpers.serialize_object(ris_response)

                found_in_ris = set()
                nodes = ris_data['SelectCmDeviceResult']['CmNodes']['item']
                for node in nodes:
                    if node.get('CmDevices') and node['CmDevices'].get('item'):
                        for dev in node['CmDevices']['item']:
                            found_in_ris.add(dev['Name'].upper())

                # 'None' olan cihazları yakala ve listeye ekle
                for name in chunk:
                    if name.upper() not in found_in_ris:
                        none_devices_list.append({
                            "Cihaz Adı": name,
                            "Durum": "None",
                        })

                # İlerleme durumunu gösterir
                print(
                    f"İlerleme: {min(i + chunk_size, total_count)} / {total_count} tamamlandı. "
                    f"(Şu ana kadar {len(none_devices_list)} 'None' cihaz bulundu)")

            except Exception as e:
                if "rate" in str(e).lower():
                    print("\nRate Limit! 20 saniye bekleniyor...")
                    time.sleep(20)
                else:
                    print(f"\n[!] Hata: {e}")

        # 3. EXCEL'E YAZDIRMA
        if none_devices_list:
            df = pd.DataFrame(none_devices_list)
            file_name = "None_Cihazlar_Raporu.xlsx"
            df.to_excel(file_name, index=False)

            print("\n" + "=" * 50)
            print(f" İŞLEM TAMAMLANDI")
            print("=" * 50)
            print(f"Toplam Cihaz Sayısı     : {total_count}")
            print(f"None Cihaz Sayısı      : {len(none_devices_list)}")
            print(f"Dosya Oluşturuldu      : {file_name}")
            print("=" * 50)
        else:
            print("\nHiç 'None' cihaz bulunamadı, dosya oluşturulmadı.")

    except Exception as e:
        print(f"Genel Hata: {e}")

if __name__ == "__main__":
    none_devices_to_excel()