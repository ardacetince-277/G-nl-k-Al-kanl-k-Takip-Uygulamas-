"""
DataManager Service Class
Veri kaydetme, yükleme ve yedekleme işlemlerini yöneten sınıf
"""

import json
import os
import datetime
from typing import Dict, List, Any


class DataManager:
    """
    Veri yönetimi sınıfı
    JSON formatında veri kaydetme, yükleme ve yedekleme işlemlerini yönetir
    """
    
    def __init__(self, base_directory="data"):
        """
        DataManager sınıfı constructor
        """
        self.base_directory = base_directory
        self.file_path = os.path.join(base_directory, "habits_data.json")
        self.backup_path = os.path.join(base_directory, "backup")
        
        # Klasörleri oluştur
        self._ensure_directories()
    
    def _ensure_directories(self):
        """
        Gerekli klasörleri oluşturur
        """
        try:
            if not os.path.exists(self.base_directory):
                os.makedirs(self.base_directory)
            
            if not os.path.exists(self.backup_path):
                os.makedirs(self.backup_path)
                
        except Exception as e:
            print(f"Klasör oluşturma hatası: {e}")
    
    def save_data(self, users, habits, records):
        """
        Tüm verileri dosyaya kaydeder
        Args: users - kullanıcı listesi, habits - alışkanlık listesi, records - kayıt listesi
        Returns: bool - işlem başarılı ise True
        """
        try:
            # Verileri JSON formatına dönüştür
            data = {
                'users': [user.get_user_info() if hasattr(user, 'get_user_info') else user for user in users],
                'habits': [habit.get_habit_details() if hasattr(habit, 'get_habit_details') else habit for habit in habits],
                'records': [record.get_record_details() if hasattr(record, 'get_record_details') else record for record in records],
                'last_updated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Dosyaya yaz
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            
            print(f"Veriler başarıyla kaydedildi: {self.file_path}")
            return True
            
        except Exception as e:
            print(f"Veri kaydetme hatası: {e}")
            return False
    
    def load_data(self):
        """
        Dosyadan verileri yükler
        Returns: dict - yüklenen veriler veya boş dict
        """
        try:
            if not os.path.exists(self.file_path):
                print("Veri dosyası bulunamadı, yeni veri seti oluşturuluyor...")
                return self._get_empty_data()
            
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            print(f"Veriler başarıyla yüklendi: {self.file_path}")
            return data
            
        except json.JSONDecodeError as e:
            print(f"JSON okuma hatası: {e}")
            return self._get_empty_data()
        except Exception as e:
            print(f"Veri yükleme hatası: {e}")
            return self._get_empty_data()
    
    def _get_empty_data(self):
        """
        Boş veri yapısı döndürür
        Returns: dict - boş veri yapısı
        """
        return {
            'users': [],
            'habits': [],
            'records': [],
            'last_updated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def create_backup(self, users, habits, records):
        """
        Veri yedeği oluşturur
        Args: users - kullanıcı listesi, habits - alışkanlık listesi, records - kayıt listesi
        Returns: bool - işlem başarılı ise True
        """
        try:
            # Yedek dosyası adı oluştur
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(self.backup_path, f"backup_{timestamp}.json")
            
            # Verileri JSON formatına dönüştür
            data = {
                'users': [user.get_user_info() if hasattr(user, 'get_user_info') else user for user in users],
                'habits': [habit.get_habit_details() if hasattr(habit, 'get_habit_details') else habit for habit in habits],
                'records': [record.get_record_details() if hasattr(record, 'get_record_details') else record for record in records],
                'backup_created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Yedek dosyasına yaz
            with open(backup_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            
            print(f"Yedek başarıyla oluşturuldu: {backup_file}")
            return True
            
        except Exception as e:
            print(f"Yedekleme hatası: {e}")
            return False
    
    def restore_backup(self, backup_filename):
        """
        Belirtilen yedek dosyasından verileri geri yükler
        Args: backup_filename - yedek dosyası adı
        Returns: dict - geri yüklenen veriler veya None
        """
        try:
            backup_file = os.path.join(self.backup_path, backup_filename)
            
            if not os.path.exists(backup_file):
                print(f"Yedek dosyası bulunamadı: {backup_file}")
                return None
            
            with open(backup_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            print(f"Yedek başarıyla geri yüklendi: {backup_file}")
            return data
            
        except Exception as e:
            print(f"Yedek geri yükleme hatası: {e}")
            return None
    
    def list_backups(self):
        """
        Mevcut yedek dosyalarını listeler
        Returns: list - yedek dosyası listesi
        """
        try:
            if not os.path.exists(self.backup_path):
                return []
            
            backup_files = []
            for filename in os.listdir(self.backup_path):
                if filename.startswith('backup_') and filename.endswith('.json'):
                    file_path = os.path.join(self.backup_path, filename)
                    file_stat = os.stat(file_path)
                    
                    backup_files.append({
                        'filename': filename,
                        'size': file_stat.st_size,
                        'created': datetime.datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                    })
            
            # Oluşturulma tarihine göre sırala
            backup_files.sort(key=lambda x: x['created'], reverse=True)
            
            return backup_files
            
        except Exception as e:
            print(f"Yedek listeleme hatası: {e}")
            return []
    
    def delete_backup(self, backup_filename):
        """
        Belirtilen yedek dosyasını siler
        Args: backup_filename - yedek dosyası adı
        Returns: bool - silme başarılı ise True
        """
        try:
            backup_file = os.path.join(self.backup_path, backup_filename)
            
            if not os.path.exists(backup_file):
                print(f"Yedek dosyası bulunamadı: {backup_file}")
                return False
            
            os.remove(backup_file)
            print(f"Yedek dosyası silindi: {backup_file}")
            return True
            
        except Exception as e:
            print(f"Yedek silme hatası: {e}")
            return False
    
    def validate_data(self, data):
        """
        Veri yapısını doğrular
        Args: data - doğrulanacak veri
        Returns: bool - veri geçerli ise True
        """
        try:
            if not isinstance(data, dict):
                return False
            
            required_keys = ['users', 'habits', 'records']
            for key in required_keys:
                if key not in data:
                    return False
                if not isinstance(data[key], list):
                    return False
            
            return True
            
        except Exception as e:
            print(f"Veri doğrulama hatası: {e}")
            return False
    
    def get_file_info(self):
        """
        Ana veri dosyası bilgilerini döndürür
        Returns: dict - dosya bilgileri
        """
        try:
            if not os.path.exists(self.file_path):
                return {'exists': False}
            
            file_stat = os.stat(self.file_path)
            
            return {
                'exists': True,
                'size': file_stat.st_size,
                'modified': datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'path': self.file_path
            }
            
        except Exception as e:
            print(f"Dosya bilgisi alma hatası: {e}")
            return {'exists': False}
    
    def export_data(self, users, habits, records, export_filename):
        """
        Verileri belirtilen dosyaya dışa aktarır
        Args: users, habits, records - veri listeleri, export_filename - dışa aktarılacak dosya adı
        Returns: bool - işlem başarılı ise True
        """
        try:
            export_path = os.path.join(self.base_directory, export_filename)
            
            # Verileri JSON formatına dönüştür
            data = {
                'users': [user.get_user_info() if hasattr(user, 'get_user_info') else user for user in users],
                'habits': [habit.get_habit_details() if hasattr(habit, 'get_habit_details') else habit for habit in habits],
                'records': [record.get_record_details() if hasattr(record, 'get_record_details') else record for record in records],
                'exported': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Dosyaya yaz
            with open(export_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            
            print(f"Veriler başarıyla dışa aktarıldı: {export_path}")
            return True
            
        except Exception as e:
            print(f"Dışa aktarma hatası: {e}")
            return False
    
    def __str__(self):
        """
        String representation
        """
        return f"DataManager({self.file_path})"
