"""
Gamification Manager Class
Oyunlaştırma sistemi için XP, seviye ve bonus yönetimi
"""

import datetime
from typing import Dict, List, Optional, Tuple


class GamificationManager:
    """
    Oyunlaştırma yöneticisi sınıfı
    Kullanıcı seviyeleri, XP kazanımı ve bonus sistemi
    """
    
    def __init__(self):
        """
        GamificationManager constructor
        XP ve seviye sistemini başlatır
        """
        # Seviye sistemi ayarları
        self.XP_PER_LEVEL = 100  # Her seviye için gereken XP
        self.STREAK_BONUS_DAYS = 7  # Bonus için gereken seri gün sayısı
        self.STREAK_BONUS_XP = 50  # Seri bonus XP'si
        
        # Zorluk seviyelerine göre XP değerleri
        self.DIFFICULTY_XP = {
            'Düşük': 5,    # Kolay alışkanlıklar için 5 XP
            'Orta': 15,    # Orta zorlukta 15 XP
            'Yüksek': 30   # Zor alışkanlıklar için 30 XP
        }
        
        # Seviye başlıkları ve renkleri
        self.LEVEL_TITLES = {
            1: ("Yeni Başlayan", "#95A5A6"),
            2: ("Acemi", "#95A5A6"),
            3: ("Çırak", "#95A5A6"),
            4: ("Usta Çırak", "#3498DB"),
            5: ("Uzman", "#3498DB"),
            10: ("Usta", "#2ECC71"),
            15: ("Grandmaster", "#F39C12"),
            20: ("Efsane", "#E74C3C"),
            25: ("Tanrısal", "#9B59B6"),
            30: ("Ezici", "#8E44AD")
        }
    
    def calculate_level_from_xp(self, total_xp: int) -> int:
        """
        Toplam XP'den seviyeyi hesaplar
        Args: total_xp - kullanıcının toplam XP'si
        Returns: Kullanıcının seviyesi
        """
        # Her seviye 100 XP gerektirir
        # Seviye 1: 0-99 XP, Seviye 2: 100-199 XP, vb.
        return (total_xp // self.XP_PER_LEVEL) + 1
    
    def calculate_xp_for_next_level(self, total_xp: int) -> int:
        """
        Bir sonraki seviye için gereken XP'yi hesaplar
        Args: total_xp - kullanıcının toplam XP'si
        Returns: Bir sonraki seviye için gereken XP
        """
        current_level = self.calculate_level_from_xp(total_xp)
        xp_for_current_level = (current_level - 1) * self.XP_PER_LEVEL
        xp_for_next_level = current_level * self.XP_PER_LEVEL
        return xp_for_next_level - total_xp
    
    def get_level_progress_percentage(self, total_xp: int) -> float:
        """
        Mevcut seviye için ilerleme yüzdesini hesaplar
        Args: total_xp - kullanıcının toplam XP'si
        Returns: İlerleme yüzdesi (0.0 - 1.0)
        """
        current_level = self.calculate_level_from_xp(total_xp)
        xp_for_current_level = (current_level - 1) * self.XP_PER_LEVEL
        xp_in_current_level = total_xp - xp_for_current_level
        return xp_in_current_level / self.XP_PER_LEVEL
    
    def get_level_title(self, level: int) -> str:
        """
        Seviye başlığını döndürür
        Args: level - seviye numarası
        Returns: Seviye başlığı
        """
        # En yakın seviye başlığını bul
        for level_threshold in sorted(self.LEVEL_TITLES.keys(), reverse=True):
            if level >= level_threshold:
                return self.LEVEL_TITLES[level_threshold][0]
        return "Yeni Başlayan"
    
    def get_level_color(self, level: int) -> str:
        """
        Seviye rengini döndürür
        Args: level - seviye numarası
        Returns: Seviye rengi (hex kodu)
        """
        # En yakın seviye rengini bul
        for level_threshold in sorted(self.LEVEL_TITLES.keys(), reverse=True):
            if level >= level_threshold:
                return self.LEVEL_TITLES[level_threshold][1]
        return "#95A5A6"  # Varsayılan gri renk
    
    def calculate_habit_completion_xp(self, difficulty: str) -> int:
        """
        Alışkanlık tamamlama için XP hesaplar
        Args: difficulty - zorluk seviyesi ('Düşük', 'Orta', 'Yüksek')
        Returns: Kazanılan XP miktarı
        """
        return self.DIFFICULTY_XP.get(difficulty, 5)  # Varsayılan olarak 5 XP
    
    def calculate_streak_bonus(self, current_streak: int) -> int:
        """
        Seri bonusunu hesaplar
        Args: current_streak - mevcut seri gün sayısı
        Returns: Bonus XP miktarı
        """
        # Her 7 günde bir 50 XP bonus
        streak_bonus_count = current_streak // self.STREAK_BONUS_DAYS
        return streak_bonus_count * self.STREAK_BONUS_XP
    
    def check_level_up(self, old_xp: int, new_xp: int) -> Tuple[bool, int, int]:
        """
        Seviye atlayıp atlamadığını kontrol eder
        Args: old_xp - eski XP, new_xp - yeni XP
        Returns: (level_up, old_level, new_level)
        """
        old_level = self.calculate_level_from_xp(old_xp)
        new_level = self.calculate_level_from_xp(new_xp)
        
        level_up = new_level > old_level
        return level_up, old_level, new_level
    
    def get_xp_needed_for_level(self, target_level: int) -> int:
        """
        Belirli bir seviye için gereken toplam XP'yi hesaplar
        Args: target_level - hedef seviye
        Returns: Gereken toplam XP
        """
        return (target_level - 1) * self.XP_PER_LEVEL
    
    def get_level_range(self, level: int) -> Tuple[int, int]:
        """
        Belirli bir seviyenin XP aralığını döndürür
        Args: level - seviye numarası
        Returns: (min_xp, max_xp)
        """
        min_xp = self.get_xp_needed_for_level(level)
        max_xp = self.get_xp_needed_for_level(level + 1) - 1
        return min_xp, max_xp
    
    def get_next_milestone_levels(self, current_level: int, count: int = 3) -> List[int]:
        """
        Bir sonraki kilometre taşı seviyelerini döndürür
        Args: current_level - mevcut seviye, count - kaç seviye gösterileceği
        Returns: Milestone seviyeleri listesi
        """
        milestones = []
        for level in sorted(self.LEVEL_TITLES.keys()):
            if level > current_level:
                milestones.append(level)
                if len(milestones) >= count:
                    break
        return milestones
    
    def format_xp_display(self, total_xp: int) -> str:
        """
        XP'yi kullanıcı dostu formatta gösterir
        Args: total_xp - toplam XP
        Returns: Formatlanmış XP metni
        """
        level = self.calculate_level_from_xp(total_xp)
        xp_for_next = self.calculate_xp_for_next_level(total_xp)
        return f"Seviye {level} • {total_xp} XP • Sonraki seviye için {xp_for_next} XP"
    
    def get_achievement_badges(self, total_xp: int, level: int) -> List[Dict]:
        """
        Kazanılan rozetleri döndürür
        Args: total_xp - toplam XP, level - seviye
        Returns: Rozet listesi
        """
        badges = []
        
        # XP bazlı rozetler
        if total_xp >= 1000:
            badges.append({"name": "Binlik", "icon": "🏆", "description": "1000 XP ulaşıldı"})
        elif total_xp >= 500:
            badges.append({"name": "Beşyüzlük", "icon": "🎯", "description": "500 XP ulaşıldı"})
        elif total_xp >= 100:
            badges.append({"name": "Yüzlük", "icon": "⭐", "description": "100 XP ulaşıldı"})
        elif total_xp >= 50:
            badges.append({"name": "Elli", "icon": "🌟", "description": "50 XP ulaşıldı"})
        elif total_xp >= 10:
            badges.append({"name": "Onluk", "icon": "✨", "description": "10 XP ulaşıldı"})
        
        # Seviye bazlı rozetler
        if level >= 10:
            badges.append({"name": "Usta", "icon": "👑", "description": "Seviye 10 ulaşıldı"})
        elif level >= 5:
            badges.append({"name": "Uzman", "icon": "🎖️", "description": "Seviye 5 ulaşıldı"})
        elif level >= 3:
            badges.append({"name": "Çırak", "icon": "🏅", "description": "Seviye 3 ulaşıldı"})
        
        return badges
    
    def calculate_daily_xp_cap(self, current_level: int) -> int:
        """
        Günlük XP上限unu hesaplar (oyun dengesi için)
        Args: current_level - mevcut seviye
        Returns: Günlük maksimum XP
        """
        # Seviye başına günlük 100 XP limiti
        return 100 + (current_level * 10)
    
    def get_difficulty_color(self, difficulty: str) -> str:
        """
        Zorluk seviyesine göre renk döndürür
        Args: difficulty - zorluk seviyesi
        Returns: Renk kodu
        """
        colors = {
            'Düşük': '#27AE60',    # Yeşil
            'Orta': '#F39C12',     # Turuncu
            'Yüksek': '#E74C3C'    # Kırmızı
        }
        return colors.get(difficulty, '#95A5A6')  # Varsayılan gri
    
    def validate_difficulty(self, difficulty: str) -> bool:
        """
        Zorluk seviyesini doğrular
        Args: difficulty - zorluk seviyesi
        Returns: Geçerli mi?
        """
        return difficulty in self.DIFFICULTY_XP.keys()
    
    def get_all_difficulties(self) -> List[str]:
        """
        Tüm zorluk seviyelerini döndürür
        Returns: Zorluk seviyeleri listesi
        """
        return list(self.DIFFICULTY_XP.keys())
    
    def get_level_statistics(self, total_xp: int) -> Dict:
        """
        Seviye istatistiklerini döndürür
        Args: total_xp - toplam XP
        Returns: Seviye istatistikleri sözlüğü
        """
        level = self.calculate_level_from_xp(total_xp)
        title = self.get_level_title(level)
        color = self.get_level_color(level)
        progress = self.get_level_progress_percentage(total_xp)
        xp_for_next = self.calculate_xp_for_next_level(total_xp)
        
        return {
            'level': level,
            'title': title,
            'color': color,
            'total_xp': total_xp,
            'xp_for_next_level': xp_for_next,
            'progress_percentage': progress,
            'level_range': self.get_level_range(level)
        }
