"""
Statistics Service Class
İstatistik hesaplama ve yönetim işlemlerini yöneten sınıf
"""

import datetime
from typing import List, Dict


class Statistics:
    """
    İstatistik sınıfı
    Alışkanlık tamamlama oranları, streak hesaplama ve diğer istatistikleri yönetir
    """
    
    def __init__(self, user_id=None, habit_id=None):
        """
        Statistics sınıfı constructor
        """
        self.user_id = user_id
        self.habit_id = habit_id
        self.completion_rate = 0.0
        self.current_streak = 0
        self.longest_streak = 0
        self.total_completions = 0
    
    def calculate_completion_rate(self, all_records, days=30):
        """
        Belirtilen gün sayısı için tamamlama oranını hesaplar
        Args: all_records - tüm kayıtlar, days - hesaplanacak gün sayısı
        Returns: float - tamamlama yüzdesi
        """
        try:
            if not all_records:
                return 0.0
            
            # Belirtilen gün aralığı
            today = datetime.datetime.now().date()
            start_date = today - datetime.timedelta(days=days)
            
            # Bu alışkanlığa ait kayıtları filtrele
            habit_records = [
                r for r in all_records 
                if (r.habit_id == self.habit_id and 
                    r.is_completed and 
                    start_date <= r.completion_date.date() <= today)
            ]
            
            # Benzersiz tamamlanan günler
            completed_days = len(set(r.completion_date.date() for r in habit_records))
            
            # Tamamlama oranını hesapla
            completion_rate = (completed_days / days) * 100 if days > 0 else 0.0
            self.completion_rate = round(completion_rate, 2)
            
            return self.completion_rate
            
        except Exception as e:
            print(f"Tamamlama oranı hesaplama hatası: {e}")
            return 0.0
    
    def calculate_streak(self, all_records):
        """
        Mevcut streak (sıralı gün) hesaplar
        Args: all_records - tüm kayıtlar
        Returns: int - streak sayısı
        """
        try:
            if not all_records:
                self.current_streak = 0
                return 0
            
            # Bu alışkanlığa ait tamamlanmış kayıtları filtrele
            habit_records = [
                r for r in all_records 
                if r.habit_id == self.habit_id and r.is_completed
            ]
            
            if not habit_records:
                self.current_streak = 0
                return 0
            
            # Tarihleri sırala
            habit_records.sort(key=lambda x: x.completion_date)
            
            streak = 0
            current_date = datetime.datetime.now().date()
            
            # Bugünden geriye doğru kontrol et
            check_date = current_date
            
            # Önce bugün tamamlanmış mı kontrol et
            today_completed = any(
                r.completion_date.date() == current_date for r in habit_records
            )
            
            if not today_completed:
                # Eğer bugün tamamlanmadıysa, dünden başla
                check_date = current_date - datetime.timedelta(days=1)
            
            # Sıralı günleri say
            while True:
                day_completed = any(
                    r.completion_date.date() == check_date for r in habit_records
                )
                
                if day_completed:
                    streak += 1
                    check_date -= datetime.timedelta(days=1)
                else:
                    break
            
            self.current_streak = streak
            return streak
            
        except Exception as e:
            print(f"Streak hesaplama hatası: {e}")
            self.current_streak = 0
            return 0
    
    def calculate_longest_streak(self, all_records):
        """
        En uzun streak'i hesaplar
        Args: all_records - tüm kayıtlar
        Returns: int - en uzun streak
        """
        try:
            if not all_records:
                self.longest_streak = 0
                return 0
            
            # Bu alışkanlığa ait tamamlanmış kayıtları filtrele
            habit_records = [
                r for r in all_records 
                if r.habit_id == self.habit_id and r.is_completed
            ]
            
            if not habit_records:
                self.longest_streak = 0
                return 0
            
            # Tarihleri sırala
            habit_records.sort(key=lambda x: x.completion_date)
            
            longest_streak = 0
            current_streak = 0
            
            # Benzersiz tarihleri al
            unique_dates = list(set(r.completion_date.date() for r in habit_records))
            unique_dates.sort()
            
            # Sıralı günleri hesapla
            for i, date in enumerate(unique_dates):
                if i == 0:
                    current_streak = 1
                else:
                    prev_date = unique_dates[i - 1]
                    if date == prev_date + datetime.timedelta(days=1):
                        current_streak += 1
                    else:
                        if current_streak > longest_streak:
                            longest_streak = current_streak
                        current_streak = 1
                
                if current_streak > longest_streak:
                    longest_streak = current_streak
            
            self.longest_streak = longest_streak
            return longest_streak
            
        except Exception as e:
            print(f"En uzun streak hesaplama hatası: {e}")
            self.longest_streak = 0
            return 0
    
    def get_weekly_stats(self, all_records):
        """
        Haftalık istatistikleri döndürür
        Args: all_records - tüm kayıtlar
        Returns: dict - haftalık istatistikler
        """
        try:
            if not all_records:
                return {
                    'week_start': None,
                    'week_end': None,
                    'completed_days': 0,
                    'total_days': 7,
                    'completion_rate': 0.0,
                    'daily_breakdown': []
                }
            
            # Hafta aralığı
            today = datetime.datetime.now().date()
            week_start = today - datetime.timedelta(days=6)
            week_end = today
            
            # Bu haftaki kayıtları filtrele
            week_records = [
                r for r in all_records 
                if (r.habit_id == self.habit_id and 
                    r.is_completed and 
                    week_start <= r.completion_date.date() <= week_end)
            ]
            
            # Günlük döküm
            daily_breakdown = []
            completed_days = 0
            
            for i in range(7):
                check_date = week_start + datetime.timedelta(days=i)
                day_completed = any(
                    r.completion_date.date() == check_date for r in week_records
                )
                
                if day_completed:
                    completed_days += 1
                
                daily_breakdown.append({
                    'date': check_date.strftime('%Y-%m-%d'),
                    'day_name': check_date.strftime('%A'),
                    'completed': day_completed
                })
            
            completion_rate = (completed_days / 7) * 100
            
            return {
                'week_start': week_start.strftime('%Y-%m-%d'),
                'week_end': week_end.strftime('%Y-%m-%d'),
                'completed_days': completed_days,
                'total_days': 7,
                'completion_rate': round(completion_rate, 2),
                'daily_breakdown': daily_breakdown
            }
            
        except Exception as e:
            print(f"Haftalık istatistik hesaplama hatası: {e}")
            return {}
    
    def get_monthly_stats(self, all_records):
        """
        Aylık istatistikleri döndürür
        Args: all_records - tüm kayıtlar
        Returns: dict - aylık istatistikler
        """
        try:
            if not all_records:
                return {
                    'month': None,
                    'year': None,
                    'completed_days': 0,
                    'total_days': 30,
                    'completion_rate': 0.0
                }
            
            # Ay aralığı
            today = datetime.datetime.now()
            month_start = today.replace(day=1)
            
            # Ayın gün sayısını hesapla
            if today.month == 12:
                next_month = today.replace(year=today.year + 1, month=1, day=1)
            else:
                next_month = today.replace(month=today.month + 1, day=1)
            
            total_days = (next_month - month_start).days
            
            # Bu ayki kayıtları filtrele
            month_records = [
                r for r in all_records 
                if (r.habit_id == self.habit_id and 
                    r.is_completed and 
                    month_start <= r.completion_date <= today)
            ]
            
            # Benzersiz tamamlanan günler
            completed_days = len(set(r.completion_date.date() for r in month_records))
            completion_rate = (completed_days / total_days) * 100 if total_days > 0 else 0
            
            return {
                'month': today.strftime('%B'),
                'year': today.year,
                'completed_days': completed_days,
                'total_days': total_days,
                'completion_rate': round(completion_rate, 2)
            }
            
        except Exception as e:
            print(f"Aylık istatistik hesaplama hatası: {e}")
            return {}
    
    def get_all_stats(self, all_records):
        """
        Tüm istatistikleri bir arada döndürür
        Args: all_records - tüm kayıtlar
        Returns: dict - tüm istatistikler
        """
        try:
            # Tüm hesaplamaları yap
            completion_rate = self.calculate_completion_rate(all_records)
            current_streak = self.calculate_streak(all_records)
            longest_streak = self.calculate_longest_streak(all_records)
            weekly_stats = self.get_weekly_stats(all_records)
            monthly_stats = self.get_monthly_stats(all_records)
            
            # Toplam tamamlamaları hesapla
            total_completions = len([
                r for r in all_records 
                if r.habit_id == self.habit_id and r.is_completed
            ])
            self.total_completions = total_completions
            
            return {
                'habit_id': self.habit_id,
                'completion_rate': completion_rate,
                'current_streak': current_streak,
                'longest_streak': longest_streak,
                'total_completions': total_completions,
                'weekly_stats': weekly_stats,
                'monthly_stats': monthly_stats
            }
            
        except Exception as e:
            print(f"Tüm istatistikleri getirme hatası: {e}")
            return {}
    
    def get_summary_text(self):
        """
        İstatistik özetini metin olarak döndürür
        Returns: str - istatistik özeti
        """
        return (f"Başarı Oranı: %{self.completion_rate} | "
                f"Mevcut Streak: {self.current_streak} gün | "
                f"En Uzun Streak: {self.longest_streak} gün | "
                f"Toplam Tamamlama: {self.total_completions}")
    
    def __str__(self):
        """
        String representation
        """
        return f"Statistics(Habit {self.habit_id}, %{self.completion_rate}, Streak: {self.current_streak})"
