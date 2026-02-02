import time
import matplotlib.pyplot as plt
from collections import Counter
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

def find_none_devices():
    try:
        # AXL: Bilgi Toplama
        ucm = axl(username=USERNAME, password=PASSWORD, cucm=CUCM_IP, cucm_version='12.5')
        print(f"AXL: Veritabanından cihaz ve model bilgileri çekiliyor...")

        raw_phones = ucm.get_phones()
        device_info_map = {}
        for raw_p in raw_phones:
            p = helpers.serialize_object(raw_p)
            name = p.get('name')
            if name:
                device_info_map[name] = p.get('product', 'Unknown')

        device_names = list(device_info_map.keys())
        total_count = len(device_names)
        print(f"Başarılı: {total_count} cihaz sayım için hazır.\n")

        # RISPort: Canlı Durum Analizi
        ris_wsdl = f"https://{CUCM_IP}:8443/realtimeservice2/services/RISService70?wsdl"
        ris_endpoint = f"https://{CUCM_IP}:8443/realtimeservice2/services/RISService70"

        session = Session()
        session.verify = False
        session.auth = HTTPBasicAuth(USERNAME, PASSWORD)
        ris_transport = Transport(session=session, timeout=30)
        ris_client = Client(ris_wsdl, transport=ris_transport)
        ris_service = ris_client.create_service('{http://schemas.cisco.com/ast/soap}RisBinding', ris_endpoint)

        chunk_size = 100
        none_models_list = []  # Grafik için modellerin olduğu liste

        print(f"{'#':<5} | {'Cihaz Adı':<25} | {'Model':<25} | {'Durum':<10}")
        print("-" * 75)

        for i in range(0, total_count, chunk_size):
            if i > 0:
                time.sleep(4.5)

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

                for name in chunk:
                    if name.upper() not in found_in_ris:
                        model = device_info_map.get(name, "Unknown")
                        none_models_list.append(model)
                        print(f"{len(none_models_list):<5} | {name:<25} | {model:<25} | None")

            except Exception as e:
                if "rate" in str(e).lower():
                    time.sleep(15)
                else:
                    print(f"\nHata: {e}")

        # GRAFİK OLUŞTURMA
        print("-" * 75)

        if none_models_list:
            model_counts = Counter(none_models_list)

            models = list(model_counts.keys())
            counts = list(model_counts.values())

            plt.figure(figsize=(12, 7))
            bars = plt.bar(models, counts, color='skyblue', edgecolor='navy')

            plt.xlabel('Cihaz Modelleri', fontsize=12)
            plt.ylabel('None Durumundaki Cihaz Sayısı', fontsize=12)
            plt.title('CUCM "None" Durumundaki Cihazların Model Dağılımı', fontsize=14)
            plt.xticks(rotation=45, ha='right')

            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, yval, ha='center', va='bottom')

            plt.tight_layout()
            print("Grafik açılıyor...")
            plt.show()
        else:
            print("Hiç 'None' cihaz bulunamadığı için grafik üretilemedi.")

    except Exception as e:
        print(f"Genel Hata: {e}")

if __name__ == "__main__":
    find_none_devices()