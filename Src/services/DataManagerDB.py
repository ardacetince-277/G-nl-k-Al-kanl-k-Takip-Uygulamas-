"""
DataManager with SQLite Integration
SQLite veritabanı ile veri yönetimi sınıfı
"""

import os
import datetime
from typing import List, Dict, Any
from DatabaseManager import DatabaseManager
from models.User import User
from models.Habit import Habit
from models.HabitRecord import HabitRecord


class DataManagerDB:
    """
    SQLite tabanlı veri yönetimi sınıfı
    JSON yerine kalıcı veritabanı saklama
    """
    
    def __init__(self, db_path: str = "data/habits.db"):
        """
        DataManagerDB constructor
        Args: db_path - veritabanı dosya yolu
        """
        self.db_manager = DatabaseManager(db_path)
        self.backup_path = os.path.join(os.path.dirname(db_path), "backup")
        
        # Yedekleme klasörünü oluştur
        os.makedirs(self.backup_path, exist_ok=True)
    
    def save_user(self, user: User) -> bool:
        """
        Kullanıcıyı kaydeder/günceller
        Args: user - kullanıcı nesnesi
        Returns: Başarı durumu
        """
        try:
            # Kullanıcı zaten var mı kontrol et
            existing_user = self.db_manager.execute_query(
                "SELECT user_id FROM users WHERE user_id = ?", 
                (user.user_id,)
            )
            
            if existing_user:
                # Güncelle
                return self.db_manager.update_user(
                    user.user_id, user.username, user.email
                )
            else:
                # Yeni kayıt
                user_id = self.db_manager.create_user(
                    user.username, user.email, user.password
                )
                if user_id:
                    user.user_id = user_id
                    return True
                return False
                
        except Exception as e:
            print(f"Kullanıcı kaydetme hatası: {e}")
            return False
    
    def save_habit(self, habit: Habit) -> bool:
        """
        Alışkanlığı kaydeder/günceller
        Args: habit - alışkanlık nesnesi
        Returns: Başarı durumu
        """
        try:
            # Alışkanlık zaten var mı kontrol et
            existing_habit = self.db_manager.execute_query(
                "SELECT habit_id FROM habits WHERE habit_id = ?", 
                (habit.habit_id,)
            )
            
            if existing_habit:
                # Güncelle
                return self.db_manager.update_habit(
                    habit.habit_id, habit.name, habit.description, habit.target_frequency
                )
            else:
                # Yeni kayıt
                habit_id = self.db_manager.create_habit(
                    habit.user_id, habit.name, habit.description, habit.target_frequency
                )
                if habit_id:
                    habit.habit_id = habit_id
                    return True
                return False
                
        except Exception as e:
            print(f"Alışkanlık kaydetme hatası: {e}")
            return False
    
    def save_habit_record(self, record: HabitRecord) -> bool:
        """
        Alışkanlık kaydını kaydeder/günceller
        Args: record - kayıt nesnesi
        Returns: Başarı durumu
        """
        try:
            # Kayıt zaten var mı kontrol et
            existing_record = self.db_manager.execute_query(
                "SELECT record_id FROM habit_records WHERE record_id = ?", 
                (record.record_id,)
            )
            
            if existing_record:
                # Güncelle
                return self.db_manager.update_habit_record(
                    record.record_id, record.is_completed, record.notes
                )
            else:
                # Yeni kayıt
                record_id = self.db_manager.create_habit_record(
                    record.habit_id, 
                    record.completion_date.strftime('%Y-%m-%d %H:%M:%S'),
                    record.is_completed, 
                    record.notes
                )
                if record_id:
                    record.record_id = record_id
                    return True
                return False
                
        except Exception as e:
            print(f"Kayıt kaydetme hatası: {e}")
            return False
    
    def load_users(self) -> List[User]:
        """
        Tüm kullanıcıları yükler
        Returns: Kullanıcı listesi
        """
        try:
            users_data = self.db_manager.get_all_users()
            users = []
            
            for user_data in users_data:
                user = User()
                user.user_id = user_data['user_id']
                user.username = user_data['username']
                user.email = user_data['email']
                user.password = user_data['password']
                user.created_date = datetime.datetime.strptime(
                    user_data['created_date'], '%Y-%m-%d %H:%M:%S'
                )
                users.append(user)
            
            return users
            
        except Exception as e:
            print(f"Kullanıcı yükleme hatası: {e}")
            return []
    
    def load_habits(self) -> List[Habit]:
        """
        Tüm alışkanlıkları yükler
        Returns: Alışkanlık listesi
        """
        try:
            habits_data = self.db_manager.execute_query(
                "SELECT * FROM habits ORDER BY created_date"
            )
            habits = []
            
            for habit_data in habits_data:
                habit = Habit()
                habit.habit_id = habit_data['habit_id']
                habit.user_id = habit_data['user_id']
                habit.name = habit_data['name']
                habit.description = habit_data['description']
                habit.target_frequency = habit_data['target_frequency']
                habit.created_date = datetime.datetime.strptime(
                    habit_data['created_date'], '%Y-%m-%d %H:%M:%S'
                )
                habit.is_active = bool(habit_data['is_active'])
                habits.append(habit)
            
            return habits
            
        except Exception as e:
            print(f"Alışkanlık yükleme hatası: {e}")
            return []
    
    def load_habit_records(self) -> List[HabitRecord]:
        """
        Tüm alışkanlık kayıtlarını yükler
        Returns: Kayıt listesi
        """
        try:
            records_data = self.db_manager.execute_query(
                "SELECT * FROM habit_records ORDER BY completion_date DESC"
            )
            records = []
            
            for record_data in records_data:
                record = HabitRecord()
                record.record_id = record_data['record_id']
                record.habit_id = record_data['habit_id']
                record.completion_date = datetime.datetime.strptime(
                    record_data['completion_date'], '%Y-%m-%d %H:%M:%S'
                )
                record.is_completed = bool(record_data['is_completed'])
                record.notes = record_data['notes'] or ""
                records.append(record)
            
            return records
            
        except Exception as e:
            print(f"Kayıt yükleme hatası: {e}")
            return []
    
    def get_user_by_credentials(self, username: str, password: str) -> User:
        """
        Kullanıcı adı ve şifre ile kullanıcı bulur
        Args: username, password
        Returns: Kullanıcı nesnesi veya None
        """
        try:
            user_data = self.db_manager.get_user_by_credentials(username, password)
            
            if user_data:
                user = User()
                user.user_id = user_data['user_id']
                user.username = user_data['username']
                user.email = user_data['email']
                user.password = user_data['password']
                user.created_date = datetime.datetime.strptime(
                    user_data['created_date'], '%Y-%m-%d %H:%M:%S'
                )
                return user
            
            return None
            
        except Exception as e:
            print(f"Kullanıcı bulma hatası: {e}")
            return None
    
    def get_user_habits(self, user_id: int, active_only: bool = True) -> List[Habit]:
        """
        Kullanıcının alışkanlıklarını döndürür
        Args: user_id, sadece aktif olanlar
        Returns: Alışkanlık listesi
        """
        try:
            habits_data = self.db_manager.get_user_habits(user_id, active_only)
            habits = []
            
            for habit_data in habits_data:
                habit = Habit()
                habit.habit_id = habit_data['habit_id']
                habit.user_id = habit_data['user_id']
                habit.name = habit_data['name']
                habit.description = habit_data['description']
                habit.target_frequency = habit_data['target_frequency']
                habit.created_date = datetime.datetime.strptime(
                    habit_data['created_date'], '%Y-%m-%d %H:%M:%S'
                )
                habit.is_active = bool(habit_data['is_active'])
                habits.append(habit)
            
            return habits
            
        except Exception as e:
            print(f"Kullanıcı alışkanlıkları yükleme hatası: {e}")
            return []
    
    def get_habit_records(self, habit_id: int = None, completed_only: bool = None) -> List[HabitRecord]:
        """
        Alışkanlık kayıtlarını döndürür
        Args: habit_id, sadece tamamlananlar
        Returns: Kayıt listesi
        """
        try:
            records_data = self.db_manager.get_habit_records(habit_id, completed_only)
            records = []
            
            for record_data in records_data:
                record = HabitRecord()
                record.record_id = record_data['record_id']
                record.habit_id = record_data['habit_id']
                record.completion_date = datetime.datetime.strptime(
                    record_data['completion_date'], '%Y-%m-%d %H:%M:%S'
                )
                record.is_completed = bool(record_data['is_completed'])
                record.notes = record_data['notes'] or ""
                records.append(record)
            
            return records
            
        except Exception as e:
            print(f"Kayıtları yükleme hatası: {e}")
            return []
    
    def get_today_record(self, habit_id: int) -> HabitRecord:
        """
        Bugünkü kaydı döndürür
        Args: habit_id
        Returns: Bugünkü kayıt veya None
        """
        try:
            record_data = self.db_manager.get_today_record(habit_id)
            
            if record_data:
                record = HabitRecord()
                record.record_id = record_data['record_id']
                record.habit_id = record_data['habit_id']
                record.completion_date = datetime.datetime.strptime(
                    record_data['completion_date'], '%Y-%m-%d %H:%M:%S'
                )
                record.is_completed = bool(record_data['is_completed'])
                record.notes = record_data['notes'] or ""
                return record
            
            return None
            
        except Exception as e:
            print(f"Bugünkü kayıt bulma hatası: {e}")
            return None
    
    def mark_habit_completed(self, habit_id: int, notes: str = "") -> bool:
        """
        Alışkanlığı tamamlanmış olarak işaretler
        Args: habit_id, notlar
        Returns: Başarı durumu
        """
        try:
            # Bugünkü kaydı kontrol et
            today_record = self.get_today_record(habit_id)
            
            if today_record:
                # Mevcut kaydı güncelle
                return self.db_manager.update_habit_record(
                    today_record.record_id, True, notes
                )
            else:
                # Yeni kayıt oluştur
                record_id = self.db_manager.create_habit_record(
                    habit_id,
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    True,
                    notes
                )
                return record_id is not None
                
        except Exception as e:
            print(f"Tamamlama işaretleme hatası: {e}")
            return False
    
    def delete_habit(self, habit_id: int) -> bool:
        """
        Alışkanlığı siler (pasif hale getirir)
        Args: habit_id
        Returns: Başarı durumu
        """
        try:
            return self.db_manager.delete_habit(habit_id)
        except Exception as e:
            print(f"Alışkanlık silme hatası: {e}")
            return False
    
    def get_habit_statistics(self, habit_id: int, days: int = 30) -> Dict[str, Any]:
        """
        Alışkanlık istatistiklerini döndürür
        Args: habit_id, gün sayısı
        Returns: İstatistikler sözlüğü
        """
        try:
            return self.db_manager.get_habit_statistics(habit_id, days)
        except Exception as e:
            print(f"İstatistik alma hatası: {e}")
            return {
                'completion_rate': 0,
                'current_streak': 0,
                'longest_streak': 0,
                'total_completions': 0
            }
    
    def create_backup(self, users: List[User], habits: List[Habit], records: List[HabitRecord]) -> bool:
        """
        Veritabanı yedeği oluşturur
        Args: users, habits, records (uyumluluk için)
        Returns: Başarı durumu
        """
        try:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(self.backup_path, f"backup_{timestamp}.db")
            
            success = self.db_manager.backup_database(backup_file)
            if success:
                print(f"Veritabanı yedeklendi: {backup_file}")
            return success
            
        except Exception as e:
            print(f"Yedekleme hatası: {e}")
            return False
    
    def restore_backup(self, backup_filename: str) -> bool:
        """
        Yedek dosyasından geri yükler
        Args: backup_filename - yedek dosyası adı
        Returns: Başarı durumu
        """
        try:
            backup_file = os.path.join(self.backup_path, backup_filename)
            
            if not os.path.exists(backup_file):
                print(f"Yedek dosyası bulunamadı: {backup_file}")
                return False
            
            # Mevcut veritabanını yedekle
            current_backup = os.path.join(
                self.backup_path, 
                f"current_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            )
            self.db_manager.backup_database(current_backup)
            
            # Yedek dosyasını kopyala
            import shutil
            shutil.copy2(backup_file, self.db_manager.db_path)
            
            print(f"Yedekten geri yüklendi: {backup_file}")
            return True
            
        except Exception as e:
            print(f"Yedekten geri yükleme hatası: {e}")
            return False
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """
        Mevcut yedek dosyalarını listeler
        Returns: Yedek dosyası listesi
        """
        try:
            backup_files = []
            
            if os.path.exists(self.backup_path):
                for filename in os.listdir(self.backup_path):
                    if filename.endswith('.db') and filename.startswith('backup_'):
                        file_path = os.path.join(self.backup_path, filename)
                        file_stat = os.stat(file_path)
                        
                        backup_files.append({
                            'filename': filename,
                            'size': file_stat.st_size,
                            'created': datetime.datetime.fromtimestamp(
                                file_stat.st_ctime
                            ).strftime('%Y-%m-%d %H:%M:%S')
                        })
            
            # Oluşturulma tarihine göre sırala
            backup_files.sort(key=lambda x: x['created'], reverse=True)
            
            return backup_files
            
        except Exception as e:
            print(f"Yedek listeleme hatası: {e}")
            return []
    
    def delete_backup(self, backup_filename: str) -> bool:
        """
        Belirtilen yedek dosyasını siler
        Args: backup_filename - yedek dosyası adı
        Returns: Başarı durumu
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
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Veritabanı bilgilerini döndürür
        Returns: Veritabanı bilgileri
        """
        try:
            return self.db_manager.get_database_info()
        except Exception as e:
            print(f"Veritabanı bilgileri alma hatası: {e}")
            return {}
    
    def validate_data(self) -> bool:
        """
        Veri bütünlüğünü doğrular
        Returns: Veri geçerli ise True
        """
        try:
            # Veritabanı bağlantısını kontrol et
            if not self.db_manager.connection:
                return False
            
            # Tabloların varlığını kontrol et
            tables = self.db_manager.execute_query(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            
            required_tables = ['users', 'habits', 'habit_records']
            existing_tables = [table['name'] for table in tables]
            
            return all(table in existing_tables for table in required_tables)
            
        except Exception as e:
            print(f"Veri doğrulama hatası: {e}")
            return False
    
    def export_data(self, export_filename: str) -> bool:
        """
        Verileri dışa aktarır
        Args: export_filename - dışa aktarılacak dosya adı
        Returns: Başarı durumu
        """
        try:
            import json
            
            # Verileri topla
            users = self.load_users()
            habits = self.load_habits()
            records = self.load_habit_records()
            
            # JSON formatına dönüştür
            data = {
                'users': [user.get_user_info() for user in users],
                'habits': [habit.get_habit_details() for habit in habits],
                'records': [record.get_record_details() for record in records],
                'exported': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Dosyaya yaz
            export_path = os.path.join(
                os.path.dirname(self.db_manager.db_path), 
                export_filename
            )
            
            with open(export_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            
            print(f"Veriler dışa aktarıldı: {export_path}")
            return True
            
        except Exception as e:
            print(f"Dışa aktarma hatası: {e}")
            return False
    
    def close(self):
        """
        Veritabanı bağlantısını kapatır
        """
        try:
            self.db_manager.close()
        except Exception as e:
            print(f"Veritabanı kapatma hatası: {e}")
    
    def __del__(self):
        """
        Destructor - bağlantıyı kapatır
        """
        self.close()
