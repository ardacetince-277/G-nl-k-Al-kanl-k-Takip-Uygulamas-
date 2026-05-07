"""
User Statistics Manager Class
Kullanıcı istatistikleri, XP ve seviye yönetimi
"""

import datetime
from typing import Dict, List, Optional
from DatabaseManager import DatabaseManager
from GamificationManager import GamificationManager


class UserStatsManager:
    """
    Kullanıcı istatistikleri yöneticisi
    XP, seviye ve bonus takibi
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        UserStatsManager constructor
        Args: db_manager - veritabanı yöneticisi
        """
        self.db_manager = db_manager
        self.gamification = GamificationManager()
        
        # Kullanıcı istatistikleri tablosunu oluştur
        self.create_user_stats_table()
    
    def create_user_stats_table(self):
        """
        Kullanıcı istatistikleri tablosunu oluşturur
        """
        try:
            # Kullanıcı istatistikleri tablosu
            self.db_manager.execute_query('''
                CREATE TABLE IF NOT EXISTS user_stats (
                    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    total_xp INTEGER NOT NULL DEFAULT 0,
                    current_level INTEGER NOT NULL DEFAULT 1,
                    streak_bonus_date TEXT,
                    last_level_up_date TEXT,
                    total_habits_completed INTEGER NOT NULL DEFAULT 0,
                    longest_streak INTEGER NOT NULL DEFAULT 0,
                    created_date TEXT NOT NULL,
                    updated_date TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # İndeksler
            self.db_manager.execute_query('''
                CREATE INDEX IF NOT EXISTS idx_user_stats_user_id ON user_stats (user_id)
            ''')
            
            print("Kullanıcı istatistikleri tablosu oluşturuldu/güncellendi")
            
        except Exception as e:
            print(f"Kullanıcı istatistikleri tablosu oluşturma hatası: {e}")
    
    def create_user_stats(self, user_id: int) -> bool:
        """
        Yeni kullanıcı için istatistik kaydı oluşturur
        Args: user_id - kullanıcı ID'si
        Returns: Başarı durumu
        """
        try:
            created_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            query = '''
                INSERT INTO user_stats (user_id, total_xp, current_level, created_date, updated_date)
                VALUES (?, 0, 1, ?, ?)
            '''
            
            self.db_manager.execute_query(query, (user_id, created_date, created_date))
            return True
            
        except Exception as e:
            print(f"Kullanıcı istatistikleri oluşturma hatası: {e}")
            return False
    
    def get_user_stats(self, user_id: int) -> Optional[Dict]:
        """
        Kullanıcının istatistiklerini döndürür
        Args: user_id - kullanıcı ID'si
        Returns: İstatistikler sözlüğü veya None
        """
        try:
            query = '''
                SELECT * FROM user_stats WHERE user_id = ?
            '''
            
            results = self.db_manager.execute_query(query, (user_id,))
            
            if results:
                stats = dict(results[0])
                # Seviye bilgilerini güncelle
                level_info = self.gamification.get_level_statistics(stats['total_xp'])
                stats.update(level_info)
                return stats
            
            return None
            
        except Exception as e:
            print(f"Kullanıcı istatistikleri alma hatası: {e}")
            return None
    
    def add_xp_to_user(self, user_id: int, xp_amount: int, reason: str = "") -> bool:
        """
        Kullanıcıya XP ekler
        Args: user_id - kullanıcı ID'si, xp_amount - XP miktarı, reason - XP kazanım sebebi
        Returns: Başarı durumu
        """
        try:
            # Mevcut istatistikleri al
            current_stats = self.get_user_stats(user_id)
            
            if not current_stats:
                # İstatistik yoksa oluştur
                self.create_user_stats(user_id)
                current_stats = self.get_user_stats(user_id)
            
            if not current_stats:
                return False
            
            old_xp = current_stats['total_xp']
            new_xp = old_xp + xp_amount
            
            # Seviye atlama kontrolü
            level_up, old_level, new_level = self.gamification.check_level_up(old_xp, new_xp)
            
            updated_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # İstatistikleri güncelle
            query = '''
                UPDATE user_stats 
                SET total_xp = ?, current_level = ?, updated_date = ?
                WHERE user_id = ?
            '''
            
            self.db_manager.execute_query(query, (new_xp, new_level, updated_date, user_id))
            
            # Seviye atlandıysa özel güncelleme
            if level_up:
                self.update_level_up_info(user_id, new_level)
                return True, level_up, old_level, new_level
            
            return True, False, old_level, new_level
            
        except Exception as e:
            print(f"XP ekleme hatası: {e}")
            return False, False, 0, 0
    
    def update_level_up_info(self, user_id: int, new_level: int) -> bool:
        """
        Seviye atlama bilgilerini günceller
        Args: user_id - kullanıcı ID'si, new_level - yeni seviye
        Returns: Başarı durumu
        """
        try:
            level_up_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            query = '''
                UPDATE user_stats 
                SET last_level_up_date = ?
                WHERE user_id = ?
            '''
            
            self.db_manager.execute_query(query, (level_up_date, user_id))
            return True
            
        except Exception as e:
            print(f"Seviye atlama bilgisi güncelleme hatası: {e}")
            return False
    
    def update_streak_bonus_date(self, user_id: int) -> bool:
        """
        Seri bonus tarihini günceller
        Args: user_id - kullanıcı ID'si
        Returns: Başarı durumu
        """
        try:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            
            query = '''
                UPDATE user_stats 
                SET streak_bonus_date = ?
                WHERE user_id = ?
            '''
            
            self.db_manager.execute_query(query, (today, user_id))
            return True
            
        except Exception as e:
            print(f"Seri bonus tarihi güncelleme hatası: {e}")
            return False
    
    def get_streak_bonus_info(self, user_id: int) -> Dict:
        """
        Seri bonus bilgilerini döndürür
        Args: user_id - kullanıcı ID'si
        Returns: Seri bonus bilgileri
        """
        try:
            stats = self.get_user_stats(user_id)
            
            if not stats:
                return {
                    'can_get_bonus': False,
                    'days_until_bonus': 7,
                    'current_streak': 0,
                    'bonus_xp': 0
                }
            
            # Kullanıcının mevcut serisini al
            from DataManagerDB import DataManagerDB
            data_manager = DataManagerDB()
            user_habits = data_manager.get_user_habits(user_id, True)
            
            max_streak = 0
            for habit in user_habits:
                habit_stats = data_manager.get_habit_statistics(habit.habit_id, 30)
                streak = habit_stats.get('current_streak', 0)
                max_streak = max(max_streak, streak)
            
            # Bugünkü seri bonus kontrolü
            today = datetime.datetime.now().date()
            last_bonus_date = None
            
            if stats['streak_bonus_date']:
                last_bonus_date = datetime.datetime.strptime(
                    stats['streak_bonus_date'], '%Y-%m-%d'
                ).date()
            
            days_since_bonus = (today - last_bonus_date).days if last_bonus_date else 999
            
            can_get_bonus = max_streak >= 7 and days_since_bonus >= 7
            days_until_bonus = max(0, 7 - (days_since_bonus % 7)) if max_streak >= 7 else (7 - max_streak)
            
            return {
                'can_get_bonus': can_get_bonus,
                'days_until_bonus': days_until_bonus,
                'current_streak': max_streak,
                'bonus_xp': self.gamification.STREAK_BONUS_XP,
                'last_bonus_date': stats['streak_bonus_date']
            }
            
        except Exception as e:
            print(f"Seri bonus bilgileri alma hatası: {e}")
            return {
                'can_get_bonus': False,
                'days_until_bonus': 7,
                'current_streak': 0,
                'bonus_xp': 0
            }
    
    def award_streak_bonus(self, user_id: int) -> bool:
        """
        Seri bonusu verir
        Args: user_id - kullanıcı ID'si
        Returns: Başarı durumu
        """
        try:
            bonus_info = self.get_streak_bonus_info(user_id)
            
            if not bonus_info['can_get_bonus']:
                return False
            
            # Bonus XP'sini ekle
            success, level_up, old_level, new_level = self.add_xp_to_user(
                user_id, 
                bonus_info['bonus_xp'], 
                f"Seri Bonus: {bonus_info['current_streak']} gün"
            )
            
            if success:
                # Bonus tarihini güncelle
                self.update_streak_bonus_date(user_id)
                return True, level_up, old_level, new_level
            
            return False, False, 0, 0
            
        except Exception as e:
            print(f"Seri bonus verme hatası: {e}")
            return False, False, 0, 0
    
    def update_habit_completion_count(self, user_id: int) -> bool:
        """
        Tamamlanan alışkanlık sayısını günceller
        Args: user_id - kullanıcı ID'si
        Returns: Başarı durumu
        """
        try:
            # Kullanıcının toplam tamamlama sayısını hesapla
            from DataManagerDB import DataManagerDB
            data_manager = DataManagerDB()
            user_habits = data_manager.get_user_habits(user_id, True)
            
            total_completions = 0
            longest_streak = 0
            
            for habit in user_habits:
                habit_stats = data_manager.get_habit_statistics(habit.habit_id)
                total_completions += habit_stats.get('total_completions', 0)
                longest_streak = max(longest_streak, habit_stats.get('longest_streak', 0))
            
            # İstatistikleri güncelle
            query = '''
                UPDATE user_stats 
                SET total_habits_completed = ?, longest_streak = ?
                WHERE user_id = ?
            '''
            
            self.db_manager.execute_query(query, (total_completions, longest_streak, user_id))
            return True
            
        except Exception as e:
            print(f"Alışkanlık tamamlama sayısı güncelleme hatası: {e}")
            return False
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """
        Liderlik tablosunu döndürür
        Args: limit - gösterilecek kullanıcı sayısı
        Returns: Liderlik tablosu listesi
        """
        try:
            query = '''
                SELECT us.*, u.username, u.email
                FROM user_stats us
                JOIN users u ON us.user_id = u.user_id
                ORDER BY us.total_xp DESC
                LIMIT ?
            '''
            
            results = self.db_manager.execute_query(query, (limit,))
            
            leaderboard = []
            for i, result in enumerate(results, 1):
                stats = dict(result)
                # Seviye bilgilerini ekle
                level_info = self.gamification.get_level_statistics(stats['total_xp'])
                stats.update(level_info)
                stats['rank'] = i
                leaderboard.append(stats)
            
            return leaderboard
            
        except Exception as e:
            print(f"Liderlik tablosu alma hatası: {e}")
            return []
    
    def get_user_achievements(self, user_id: int) -> List[Dict]:
        """
        Kullanıcının başarımlarını döndürür
        Args: user_id - kullanıcı ID'si
        Returns: Başarımlar listesi
        """
        try:
            stats = self.get_user_stats(user_id)
            
            if not stats:
                return []
            
            # GamificationManager'dan rozetleri al
            badges = self.gamification.get_achievement_badges(
                stats['total_xp'], 
                stats['current_level']
            )
            
            # Ek başarımlar
            if stats['total_habits_completed'] >= 100:
                badges.append({
                    "name": "Yüz Tamamlama", 
                    "icon": "💯", 
                    "description": "100 alışkanlık tamamlama"
                })
            elif stats['total_habits_completed'] >= 50:
                badges.append({
                    "name": "Elli Tamamlama", 
                    "icon": "🔟", 
                    "description": "50 alışkanlık tamamlama"
                })
            
            if stats['longest_streak'] >= 30:
                badges.append({
                    "name": "Ay Serisi", 
                    "icon": "📅", 
                    "description": "30 gün seri tamamlama"
                })
            elif stats['longest_streak'] >= 14:
                badges.append({
                    "name": "İki Haftalık", 
                    "icon": "📆", 
                    "description": "14 gün seri tamamlama"
                })
            
            return badges
            
        except Exception as e:
            print(f"Başarımları alma hatası: {e}")
            return []
    
    def get_user_progress_history(self, user_id: int, days: int = 30) -> List[Dict]:
        """
        Kullanıcının ilerleme geçmişini döndürür
        Args: user_id - kullanıcı ID'si, days - gün sayısı
        Returns: İlerleme geçmişi listesi
        """
        try:
            # Bu metod için daha karmaşık bir implementasyon gerekir
            # Şimdilik basit bir geçmiş döndürelim
            stats = self.get_user_stats(user_id)
            
            if not stats:
                return []
            
            # Son 30 günün ilerlemesi (basit örnek)
            history = []
            current_date = datetime.datetime.now()
            
            for i in range(days):
                date = current_date - datetime.timedelta(days=i)
                # Gerçek implementasyon için veritabanından geçmiş verileri çekmek gerekir
                history.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'xp_gained': 0,  # Bu değer veritabanından gelmeli
                    'habits_completed': 0,  # Bu değer veritabanından gelmeli
                    'level': stats['current_level']  # Bu değer güncellenmeli
                })
            
            return history[::-1]  # En eski en başta
            
        except Exception as e:
            print(f"İlerleme geçmişi alma hatası: {e}")
            return []
    
    def calculate_user_rank(self, user_id: int) -> int:
        """
        Kullanıcının sıralamasını hesaplar
        Args: user_id - kullanıcı ID'si
        Returns: Sıralama numarası
        """
        try:
            query = '''
                SELECT COUNT(*) + 1 as user_rank
                FROM user_stats us1
                WHERE us1.total_xp > (
                    SELECT us2.total_xp 
                    FROM user_stats us2 
                    WHERE us2.user_id = ?
                )
            '''
            
            result = self.db_manager.execute_query(query, (user_id,))
            
            if result:
                return result[0]['user_rank']
            
            return 0
            
        except Exception as e:
            print(f"Kullanıcı sıralaması hesaplama hatası: {e}")
            return 0
