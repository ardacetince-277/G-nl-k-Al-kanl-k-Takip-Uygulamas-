"""
Gamified Data Manager Class
Oyunlaştırılmış veri yönetimi - XP, seviye ve alışkanlık zorlukları
"""

import datetime
from typing import Dict, List, Optional, Tuple
from DatabaseManager import DatabaseManager
from UserStatsManager import UserStatsManager
from GamificationManager import GamificationManager


class GamifiedDataManager:
    """
    Oyunlaştırılmış veri yöneticisi
    Alışkanlıklar, XP, seviye ve bonus sistemi
    """
    
    def __init__(self):
        """
        GamifiedDataManager constructor
        Veritabanı ve oyunlaştırma sistemlerini başlatır
        """
        # Veritabanı yöneticisi
        self.db_manager = DatabaseManager()
        
        # Oyunlaştırma yöneticileri
        self.user_stats_manager = UserStatsManager(self.db_manager)
        self.gamification = GamificationManager()
        
        # Alışkanlık zorluk tablosunu oluştur
        self.create_habit_difficulty_table()
        
        # Örnek kullanıcı oluştur (test için)
        self.create_default_test_user()
    
    def create_habit_difficulty_table(self):
        """
        Alışkanlık zorluk tablosunu oluşturur
        """
        try:
            # Mevcut habits tablosuna yeni sütunlar ekle
            self.db_manager.execute_query('''
                ALTER TABLE habits ADD COLUMN difficulty TEXT DEFAULT 'Düşük'
            ''')
            
            self.db_manager.execute_query('''
                ALTER TABLE habits ADD COLUMN xp_value INTEGER DEFAULT 5
            ''')
            
            print("Alışkanlık zorluk sütunları eklendi")
            
        except Exception as e:
            # Sütunlar zaten varsa hata vermez
            print(f"Alışkanlık zorluk tablosu güncelleme: {e}")
    
    def create_default_test_user(self):
        """
        Test için varsayılan kullanıcı oluşturur
        """
        try:
            # Öğrenci Test kullanıcısını kontrol et
            query = "SELECT * FROM users WHERE username = ?"
            result = self.db_manager.execute_query(query, ("Öğrenci Test",))
            
            if not result:
                # Yeni test kullanıcısı oluştur
                created_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                query = '''
                    INSERT INTO users (username, email, password, created_date)
                    VALUES (?, ?, ?, ?)
                '''
                
                self.db_manager.execute_query(query, (
                    "Öğrenci Test",
                    "ogrenci@test.com",
                    "test123",
                    created_date
                ))
                
                print("Öğrenci Test kullanıcısı oluşturuldu")
            
            # Kullanıcı ID'sini al
            query = "SELECT user_id FROM users WHERE username = ?"
            result = self.db_manager.execute_query(query, ("Öğrenci Test",))
            
            if result:
                user_id = result[0]['user_id']
                
                # Kullanıcı istatistiklerini oluştur
                self.user_stats_manager.create_user_stats(user_id)
                
                # Başlangıç alışkanlıklarını ekle
                self.add_default_habits(user_id)
                
                return user_id
            
            return None
            
        except Exception as e:
            print(f"Varsayılan kullanıcı oluşturma hatası: {e}")
            return None
    
    def add_default_habits(self, user_id: int):
        """
        Varsayılan alışkanlıkları ekler
        Args: user_id - kullanıcı ID'si
        """
        try:
            default_habits = [
                ("Sabah Egzersizi", "Her sabah 15 dakika egzersiz yap", "Orta", 15),
                ("Kitap Okuma", "Her gün 30 sayfa kitap oku", "Düşük", 5),
                ("Su İçme", "Günde 8 bardak su iç", "Düşük", 5),
                ("Meditasyon", "Her gün 10 dakika meditasyon yap", "Yüksek", 30),
                ("Kod Yazma", "Her gün 1 saat kod yaz", "Yüksek", 30)
            ]
            
            for name, description, difficulty, xp in default_habits:
                # Alışkanlık zaten var mı kontrol et
                query = '''
                    SELECT habit_id FROM habits 
                    WHERE user_id = ? AND name = ?
                '''
                
                result = self.db_manager.execute_query(query, (user_id, name))
                
                if not result:
                    # Yeni alışkanlık ekle
                    created_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    query = '''
                        INSERT INTO habits (user_id, name, description, target_frequency, 
                                         difficulty, xp_value, created_date, is_active)
                        VALUES (?, ?, ?, 1, ?, ?, ?, 1)
                    '''
                    
                    self.db_manager.execute_query(query, (
                        user_id, name, description, difficulty, xp, created_date
                    ))
            
            print("Varsayılan alışkanlıklar eklendi")
            
        except Exception as e:
            print(f"Varsayılan alışkanlıklar ekleme hatası: {e}")
    
    def get_default_user(self) -> Optional[Dict]:
        """
        Varsayılan test kullanıcısını döndürür
        Returns: Kullanıcı bilgileri veya None
        """
        try:
            query = '''
                SELECT * FROM users WHERE username = ?
            '''
            
            result = self.db_manager.execute_query(query, ("Öğrenci Test",))
            
            if result:
                return dict(result[0])
            
            return None
            
        except Exception as e:
            print(f"Varsayılan kullanıcı alma hatası: {e}")
            return None
    
    def create_habit_with_difficulty(self, user_id: int, name: str, description: str, 
                                 difficulty: str, target_frequency: int = 1) -> bool:
        """
        Zorluk seviyeli alışkanlık oluşturur
        Args: user_id - kullanıcı ID, name - alışkanlık adı, description - açıklama
              difficulty - zorluk seviyesi, target_frequency - hedef frekans
        Returns: Başarı durumu
        """
        try:
            # Zorluk seviyesini doğrula
            if not self.gamification.validate_difficulty(difficulty):
                print(f"Geçersiz zorluk seviyesi: {difficulty}")
                return False
            
            # XP değerini hesapla
            xp_value = self.gamification.calculate_habit_completion_xp(difficulty)
            
            created_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            query = '''
                INSERT INTO habits (user_id, name, description, target_frequency, 
                                 difficulty, xp_value, created_date, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            '''
            
            self.db_manager.execute_query(query, (
                user_id, name, description, target_frequency, 
                difficulty, xp_value, created_date
            ))
            
            return True
            
        except Exception as e:
            print(f"Zorlukli alışkanlık oluşturma hatası: {e}")
            return False
    
    def get_user_habits_with_difficulty(self, user_id: int, active_only: bool = True) -> List[Dict]:
        """
        Kullanıcının zorluk seviyeli alışkanlıklarını döndürür
        Args: user_id - kullanıcı ID, active_only - sadece aktif olanlar
        Returns: Alışkanlıklar listesi
        """
        try:
            query = '''
                SELECT * FROM habits WHERE user_id = ?
            '''
            
            if active_only:
                query += ' AND is_active = 1'
            
            query += ' ORDER BY created_date DESC'
            
            results = self.db_manager.execute_query(query, (user_id,))
            
            habits = []
            for result in results:
                habit = dict(result)
                # Zorluk rengini ekle
                habit['difficulty_color'] = self.gamification.get_difficulty_color(
                    habit['difficulty']
                )
                habits.append(habit)
            
            return habits
            
        except Exception as e:
            print(f"Zorlukli alışkanlıklar alma hatası: {e}")
            return []
    
    def complete_habit_with_xp(self, habit_id: int, user_id: int, 
                             notes: str = "") -> Tuple[bool, Dict]:
        """
        Alışkanlığı tamamlar ve XP verir
        Args: habit_id - alışkanlık ID, user_id - kullanıcı ID, notes - notlar
        Returns: (başarı, sonuç bilgileri)
        """
        try:
            # Alışkanlık bilgilerini al
            query = "SELECT * FROM habits WHERE habit_id = ?"
            habit_result = self.db_manager.execute_query(query, (habit_id,))
            
            if not habit_result:
                return False, {"error": "Alışkanlık bulunamadı"}
            
            habit = dict(habit_result[0])
            
            # Bugün tamamlanmış mı kontrol et
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            
            query = '''
                SELECT * FROM habit_records 
                WHERE habit_id = ? AND completion_date = ?
            '''
            
            existing_record = self.db_manager.execute_query(query, (habit_id, today))
            
            if existing_record:
                return False, {"error": "Bugün zaten tamamlanmış"}
            
            # Tamamlama kaydı oluştur
            completion_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            query = '''
                INSERT INTO habit_records (habit_id, completion_date, is_completed, notes)
                VALUES (?, ?, 1, ?)
            '''
            
            self.db_manager.execute_query(query, (habit_id, completion_date, notes))
            
            # XP kazanımı
            xp_gained = habit['xp_value']
            
            # XP'yi kullanıcıya ekle
            success, level_up, old_level, new_level = self.user_stats_manager.add_xp_to_user(
                user_id, xp_gained, f"Alışkanlık tamamlama: {habit['name']}"
            )
            
            if not success:
                return False, {"error": "XP eklenemedi"}
            
            # Seri bonusunu kontrol et
            streak_info = self.user_stats_manager.get_streak_bonus_info(user_id)
            streak_bonus_given = False
            
            if streak_info['can_get_bonus']:
                bonus_success, bonus_level_up, bonus_old_level, bonus_new_level = self.user_stats_manager.award_streak_bonus(user_id)
                
                if bonus_success:
                    streak_bonus_given = True
                    xp_gained += streak_info['bonus_xp']
            
            # Kullanıcı istatistiklerini güncelle
            self.user_stats_manager.update_habit_completion_count(user_id)
            
            # Sonuç bilgileri
            result = {
                "success": True,
                "xp_gained": xp_gained,
                "habit_name": habit['name'],
                "habit_difficulty": habit['difficulty'],
                "level_up": level_up or streak_bonus_given,
                "old_level": old_level,
                "new_level": new_level,
                "streak_bonus_given": streak_bonus_given,
                "streak_bonus_xp": streak_info['bonus_xp'] if streak_bonus_given else 0
            }
            
            return True, result
            
        except Exception as e:
            print(f"Alışkanlık tamamlama hatası: {e}")
            return False, {"error": str(e)}
    
    def get_user_statistics_with_gamification(self, user_id: int) -> Dict:
        """
        Oyunlaştırılmış kullanıcı istatistiklerini döndürür
        Args: user_id - kullanıcı ID
        Returns: İstatistikler sözlüğü
        """
        try:
            # Temel kullanıcı istatistikleri
            user_stats = self.user_stats_manager.get_user_stats(user_id)
            
            if not user_stats:
                return {}
            
            # Alışkanlık istatistikleri
            habits = self.get_user_habits_with_difficulty(user_id, True)
            
            total_habits = len(habits)
            total_xp_potential = sum(habit['xp_value'] for habit in habits)
            
            # Zorluk dağılımı
            difficulty_distribution = {}
            for habit in habits:
                difficulty = habit['difficulty']
                difficulty_distribution[difficulty] = difficulty_distribution.get(difficulty, 0) + 1
            
            # Seri bonus bilgileri
            streak_info = self.user_stats_manager.get_streak_bonus_info(user_id)
            
            # Başarımlar
            achievements = self.user_stats_manager.get_user_achievements(user_id)
            
            # Sıralama
            user_rank = self.user_stats_manager.calculate_user_rank(user_id)
            
            return {
                **user_stats,
                'total_habits': total_habits,
                'total_xp_potential': total_xp_potential,
                'difficulty_distribution': difficulty_distribution,
                'streak_info': streak_info,
                'achievements': achievements,
                'user_rank': user_rank,
                'habits': habits
            }
            
        except Exception as e:
            print(f"Oyunlaştırılmış istatistikler alma hatası: {e}")
            return {}
    
    def get_leaderboard_with_gamification(self, limit: int = 10) -> List[Dict]:
        """
        Oyunlaştırılmış liderlik tablosunu döndürür
        Args: limit - gösterilecek kullanıcı sayısı
        Returns: Liderlik tablosu listesi
        """
        try:
            leaderboard = self.user_stats_manager.get_leaderboard(limit)
            
            # Ek oyunlaştırma bilgileri ekle
            for user in leaderboard:
                user['achievements'] = self.user_stats_manager.get_user_achievements(
                    user['user_id']
                )
                user['habits_count'] = len(self.get_user_habits_with_difficulty(
                    user['user_id'], True
                ))
            
            return leaderboard
            
        except Exception as e:
            print(f"Oyunlaştırılmış liderlik tablosu alma hatası: {e}")
            return []
    
    def get_all_difficulties(self) -> List[Dict]:
        """
        Tüm zorluk seviyelerini döndürür
        Returns: Zorluk seviyeleri listesi
        """
        try:
            difficulties = []
            
            for difficulty in self.gamification.get_all_difficulties():
                difficulties.append({
                    'name': difficulty,
                    'xp_value': self.gamification.calculate_habit_completion_xp(difficulty),
                    'color': self.gamification.get_difficulty_color(difficulty)
                })
            
            return difficulties
            
        except Exception as e:
            print(f"Zorluk seviyeleri alma hatası: {e}")
            return []
    
    def close(self):
        """
        Veritabanı bağlantısını kapatır
        """
        try:
            self.db_manager.close()
        except:
            pass
