"""
Database Manager Class
SQLite veritabanı yönetimi için sınıf
"""

import sqlite3
import os
import datetime
from typing import List, Dict, Any, Optional


class DatabaseManager:
    """
    SQLite veritabanı yönetimi sınıfı
    Verilerin kalıcı olarak saklanmasını sağlar
    """
    
    def __init__(self, db_path: str = "data/habits.db"):
        """
        DatabaseManager constructor
        Args: db_path - veritabanı dosya yolu
        """
        self.db_path = db_path
        self.connection = None
        
        # Veritabanı klasörünü oluştur
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Veritabanına bağlan
        self.connect()
        
        # Tabloları oluştur
        self.create_tables()
    
    def connect(self):
        """
        Veritabanına bağlanır
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            # Satır adlarına erişim için
            self.connection.row_factory = sqlite3.Row
            print(f"Veritabanına bağlandı: {self.db_path}")
            return True
        except Exception as e:
            print(f"Veritabanı bağlantı hatası: {e}")
            return False
    
    def create_tables(self):
        """
        Gerekli tabloları oluşturur
        """
        try:
            cursor = self.connection.cursor()
            
            # Kullanıcılar tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    created_date TEXT NOT NULL
                )
            ''')
            
            # Alışkanlıklar tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS habits (
                    habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    target_frequency INTEGER NOT NULL DEFAULT 1,
                    created_date TEXT NOT NULL,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Alışkanlık kayıtları tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS habit_records (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completion_date TEXT NOT NULL,
                    is_completed INTEGER NOT NULL DEFAULT 0,
                    notes TEXT,
                    FOREIGN KEY (habit_id) REFERENCES habits (habit_id)
                )
            ''')
            
            # İndeksler oluştur
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_habits_user_id ON habits (user_id)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_habit_records_habit_id ON habit_records (habit_id)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_habit_records_date ON habit_records (completion_date)
            ''')
            
            self.connection.commit()
            print("Tablolar başarıyla oluşturuldu/güncellendi")
            
        except Exception as e:
            print(f"Tablo oluşturma hatası: {e}")
    
    def close(self):
        """
        Veritabanı bağlantısını kapatır
        """
        if self.connection:
            self.connection.close()
            print("Veritabanı bağlantısı kapatıldı")
    
    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """
        SQL sorgusu çalıştırır
        Args: query - SQL sorgusu, params - parametreler
        Returns: Sonuç listesi
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            self.connection.commit()
            return results
        except Exception as e:
            print(f"Sorgu hatası: {e}")
            return []
    
    def execute_many(self, query: str, params_list: List[tuple]) -> bool:
        """
        Çoklu SQL sorgusu çalıştırır
        Args: query - SQL sorgusu, params_list - parametre listesi
        Returns: Başarı durumu
        """
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, params_list)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Çoklu sorgu hatası: {e}")
            return False
    
    def get_last_insert_id(self) -> int:
        """
        Son eklenen kaydın ID'sini döndürür
        Returns: Son kayıt ID
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT last_insert_rowid()")
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Son ID alma hatası: {e}")
            return 0
    
    # KULLANICI İŞLEMLERİ
    def create_user(self, username: str, email: str, password: str) -> Optional[int]:
        """
        Yeni kullanıcı oluşturur
        Args: username, email, password
        Returns: Kullanıcı ID veya None
        """
        try:
            created_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = '''
                INSERT INTO users (username, email, password, created_date)
                VALUES (?, ?, ?, ?)
            '''
            self.execute_query(query, (username, email, password))
            return self.get_last_insert_id()
        except Exception as e:
            print(f"Kullanıcı oluşturma hatası: {e}")
            return None
    
    def get_user_by_credentials(self, username: str, password: str) -> Optional[sqlite3.Row]:
        """
        Kullanıcı adı ve şifre ile kullanıcı bulur
        Args: username, password
        Returns: Kullanıcı bilgileri veya None
        """
        query = '''
            SELECT * FROM users WHERE username = ? AND password = ?
        '''
        results = self.execute_query(query, (username, password))
        return results[0] if results else None
    
    def get_all_users(self) -> List[sqlite3.Row]:
        """
        Tüm kullanıcıları döndürür
        Returns: Kullanıcı listesi
        """
        query = "SELECT * FROM users ORDER BY created_date"
        return self.execute_query(query)
    
    def update_user(self, user_id: int, username: str = None, email: str = None) -> bool:
        """
        Kullanıcı bilgilerini günceller
        Args: user_id, yeni kullanıcı adı, yeni e-posta
        Returns: Başarı durumu
        """
        try:
            if username:
                query = "UPDATE users SET username = ? WHERE user_id = ?"
                self.execute_query(query, (username, user_id))
            
            if email:
                query = "UPDATE users SET email = ? WHERE user_id = ?"
                self.execute_query(query, (email, user_id))
            
            return True
        except Exception as e:
            print(f"Kullanıcı güncelleme hatası: {e}")
            return False
    
    # ALIŞKANLIK İŞLEMLERİ
    def create_habit(self, user_id: int, name: str, description: str, target_frequency: int) -> Optional[int]:
        """
        Yeni alışkanlık oluşturur
        Args: user_id, name, description, target_frequency
        Returns: Alışkanlık ID veya None
        """
        try:
            created_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = '''
                INSERT INTO habits (user_id, name, description, target_frequency, created_date, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            '''
            self.execute_query(query, (user_id, name, description, target_frequency, created_date))
            return self.get_last_insert_id()
        except Exception as e:
            print(f"Alışkanlık oluşturma hatası: {e}")
            return None
    
    def get_user_habits(self, user_id: int, active_only: bool = True) -> List[sqlite3.Row]:
        """
        Kullanıcının alışkanlıklarını döndürür
        Args: user_id, sadece aktif olanlar
        Returns: Alışkanlık listesi
        """
        if active_only:
            query = '''
                SELECT * FROM habits 
                WHERE user_id = ? AND is_active = 1 
                ORDER BY created_date
            '''
        else:
            query = '''
                SELECT * FROM habits 
                WHERE user_id = ? 
                ORDER BY created_date
            '''
        
        return self.execute_query(query, (user_id,))
    
    def update_habit(self, habit_id: int, name: str = None, description: str = None, target_frequency: int = None) -> bool:
        """
        Alışkanlık bilgilerini günceller
        Args: habit_id, yeni ad, yeni açıklama, yeni hedef
        Returns: Başarı durumu
        """
        try:
            updates = []
            params = []
            
            if name:
                updates.append("name = ?")
                params.append(name)
            
            if description is not None:
                updates.append("description = ?")
                params.append(description)
            
            if target_frequency:
                updates.append("target_frequency = ?")
                params.append(target_frequency)
            
            if updates:
                query = f"UPDATE habits SET {', '.join(updates)} WHERE habit_id = ?"
                params.append(habit_id)
                self.execute_query(query, tuple(params))
            
            return True
        except Exception as e:
            print(f"Alışkanlık güncelleme hatası: {e}")
            return False
    
    def delete_habit(self, habit_id: int) -> bool:
        """
        Alışkanlığı siler (pasif hale getirir)
        Args: habit_id
        Returns: Başarı durumu
        """
        try:
            query = "UPDATE habits SET is_active = 0 WHERE habit_id = ?"
            self.execute_query(query, (habit_id,))
            return True
        except Exception as e:
            print(f"Alışkanlık silme hatası: {e}")
            return False
    
    # ALIŞKANLIK KAYDI İŞLEMLERİ
    def create_habit_record(self, habit_id: int, completion_date: str, is_completed: bool = True, notes: str = "") -> Optional[int]:
        """
        Yeni alışkanlık kaydı oluşturur
        Args: habit_id, completion_date, is_completed, notes
        Returns: Kayıt ID veya None
        """
        try:
            query = '''
                INSERT INTO habit_records (habit_id, completion_date, is_completed, notes)
                VALUES (?, ?, ?, ?)
            '''
            self.execute_query(query, (habit_id, completion_date, is_completed, notes))
            return self.get_last_insert_id()
        except Exception as e:
            print(f"Kayıt oluşturma hatası: {e}")
            return None
    
    def get_habit_records(self, habit_id: int = None, completed_only: bool = None) -> List[sqlite3.Row]:
        """
        Alışkanlık kayıtlarını döndürür
        Args: habit_id, sadece tamamlananlar
        Returns: Kayıt listesi
        """
        query = "SELECT * FROM habit_records WHERE 1=1"
        params = []
        
        if habit_id:
            query += " AND habit_id = ?"
            params.append(habit_id)
        
        if completed_only is not None:
            query += " AND is_completed = ?"
            params.append(completed_only)
        
        query += " ORDER BY completion_date DESC"
        
        return self.execute_query(query, tuple(params))
    
    def get_today_record(self, habit_id: int) -> Optional[sqlite3.Row]:
        """
        Bugünkü kaydı döndürür
        Args: habit_id
        Returns: Bugünkü kayıt veya None
        """
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        query = '''
            SELECT * FROM habit_records 
            WHERE habit_id = ? AND DATE(completion_date) = ?
            ORDER BY completion_date DESC
            LIMIT 1
        '''
        results = self.execute_query(query, (habit_id, today))
        return results[0] if results else None
    
    def update_habit_record(self, record_id: int, is_completed: bool = None, notes: str = None) -> bool:
        """
        Alışkanlık kaydını günceller
        Args: record_id, tamamlanma durumu, notlar
        Returns: Başarı durumu
        """
        try:
            updates = []
            params = []
            
            if is_completed is not None:
                updates.append("is_completed = ?")
                params.append(is_completed)
            
            if notes is not None:
                updates.append("notes = ?")
                params.append(notes)
            
            if updates:
                query = f"UPDATE habit_records SET {', '.join(updates)} WHERE record_id = ?"
                params.append(record_id)
                self.execute_query(query, tuple(params))
            
            return True
        except Exception as e:
            print(f"Kayıt güncelleme hatası: {e}")
            return False
    
    # İSTATİSTİK İŞLEMLERİ
    def get_habit_statistics(self, habit_id: int, days: int = 30) -> Dict[str, Any]:
        """
        Alışkanlık istatistiklerini döndürür
        Args: habit_id, gün sayısı
        Returns: İstatistikler sözlüğü
        """
        try:
            # Başarı oranı
            start_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
            
            query = '''
                SELECT COUNT(DISTINCT DATE(completion_date)) as completed_days
                FROM habit_records 
                WHERE habit_id = ? AND is_completed = 1 
                AND DATE(completion_date) >= ?
            '''
            result = self.execute_query(query, (habit_id, start_date))
            completed_days = result[0]['completed_days'] if result else 0
            completion_rate = (completed_days / days) * 100 if days > 0 else 0
            
            # Mevcut streak
            streak = self.calculate_streak(habit_id)
            
            # En uzun streak
            longest_streak = self.calculate_longest_streak(habit_id)
            
            # Toplam tamamlama
            query = '''
                SELECT COUNT(*) as total_completions
                FROM habit_records 
                WHERE habit_id = ? AND is_completed = 1
            '''
            result = self.execute_query(query, (habit_id,))
            total_completions = result[0]['total_completions'] if result else 0
            
            return {
                'completion_rate': round(completion_rate, 2),
                'current_streak': streak,
                'longest_streak': longest_streak,
                'total_completions': total_completions
            }
            
        except Exception as e:
            print(f"İstatistik hesaplama hatası: {e}")
            return {
                'completion_rate': 0,
                'current_streak': 0,
                'longest_streak': 0,
                'total_completions': 0
            }
    
    def calculate_streak(self, habit_id: int) -> int:
        """
        Mevcut streak'i hesaplar
        Args: habit_id
        Returns: Streak sayısı
        """
        try:
            # Son tamamlanan kayıtları al (son 100 gün)
            query = '''
                SELECT DISTINCT DATE(completion_date) as completion_date
                FROM habit_records 
                WHERE habit_id = ? AND is_completed = 1
                ORDER BY completion_date DESC
                LIMIT 100
            '''
            results = self.execute_query(query, (habit_id,))
            
            if not results:
                return 0
            
            streak = 0
            current_date = datetime.datetime.now().date()
            
            # Bugünden geriye doğru kontrol et
            check_date = current_date
            
            # Önce bugün tamamlanmış mı kontrol et
            today_completed = any(
                datetime.datetime.strptime(row['completion_date'], '%Y-%m-%d').date() == current_date 
                for row in results
            )
            
            if not today_completed:
                # Eğer bugün tamamlanmadıysa, dünden başla
                check_date = current_date - datetime.timedelta(days=1)
            
            # Sıralı günleri say
            while True:
                day_completed = any(
                    datetime.datetime.strptime(row['completion_date'], '%Y-%m-%d').date() == check_date 
                    for row in results
                )
                
                if day_completed:
                    streak += 1
                    check_date -= datetime.timedelta(days=1)
                else:
                    break
            
            return streak
            
        except Exception as e:
            print(f"Streak hesaplama hatası: {e}")
            return 0
    
    def calculate_longest_streak(self, habit_id: int) -> int:
        """
        En uzun streak'i hesaplar
        Args: habit_id
        Returns: En uzun streak
        """
        try:
            query = '''
                SELECT DISTINCT DATE(completion_date) as completion_date
                FROM habit_records 
                WHERE habit_id = ? AND is_completed = 1
                ORDER BY completion_date ASC
            '''
            results = self.execute_query(query, (habit_id,))
            
            if not results:
                return 0
            
            longest_streak = 0
            current_streak = 0
            
            # Benzersiz tarihleri al
            dates = [
                datetime.datetime.strptime(row['completion_date'], '%Y-%m-%d').date() 
                for row in results
            ]
            
            # Sıralı günleri hesapla
            for i, date in enumerate(dates):
                if i == 0:
                    current_streak = 1
                else:
                    prev_date = dates[i - 1]
                    if date == prev_date + datetime.timedelta(days=1):
                        current_streak += 1
                    else:
                        if current_streak > longest_streak:
                            longest_streak = current_streak
                        current_streak = 1
                
                if current_streak > longest_streak:
                    longest_streak = current_streak
            
            return longest_streak
            
        except Exception as e:
            print(f"En uzun streak hesaplama hatası: {e}")
            return 0
    
    # VERİ YEDekLEME
    def backup_database(self, backup_path: str) -> bool:
        """
        Veritabanını yedekler
        Args: backup_path - yedek yolu
        Returns: Başarı durumu
        """
        try:
            # Yedekleme klasörünü oluştur
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # Veritabanını kopyala
            import shutil
            shutil.copy2(self.db_path, backup_path)
            
            print(f"Veritabanı yedeklendi: {backup_path}")
            return True
        except Exception as e:
            print(f"Yedekleme hatası: {e}")
            return False
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Veritabanı bilgilerini döndürür
        Returns: Veritabanı bilgileri
        """
        try:
            # Tablo sayıları
            users_count = self.execute_query("SELECT COUNT(*) as count FROM users")[0]['count']
            habits_count = self.execute_query("SELECT COUNT(*) as count FROM habits")[0]['count']
            records_count = self.execute_query("SELECT COUNT(*) as count FROM habit_records")[0]['count']
            
            # Dosya boyutu
            file_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            
            return {
                'file_path': self.db_path,
                'file_size': file_size,
                'users_count': users_count,
                'habits_count': habits_count,
                'records_count': records_count,
                'exists': os.path.exists(self.db_path)
            }
        except Exception as e:
            print(f"Veritabanı bilgileri alma hatası: {e}")
            return {}
    
    def __del__(self):
        """
        Destructor - bağlantıyı kapatır
        """
        self.close()
