"""
HabitRecord Model Class
Alışkanlık tamamlama kayıtlarını yöneten sınıf
"""

import datetime
from typing import List


class HabitRecord:
    """
    Alışkanlık kaydı sınıfı
    Alışkanlık tamamlama durumlarını ve streak (sıralı gün) takibini yönetir
    """
    
    def __init__(self, habit_id=None, completion_date=None):
        """
        HabitRecord sınıfı constructor
        """
        self.record_id = None
        self.habit_id = habit_id
        self.completion_date = completion_date or datetime.datetime.now()
        self.is_completed = False
        self.notes = ""
    
    def mark_completed(self, notes=""):
        """
        Alışkanlığı tamamlandı olarak işaretler
        Returns: bool - işlem başarılı ise True
        """
        try:
            self.is_completed = True
            self.completion_date = datetime.datetime.now()
            self.notes = notes
            
            # Record ID atanması
            self.record_id = hash(str(self.habit_id) + str(self.completion_date)) % 10000
            
            return True
            
        except Exception as e:
            print(f"Tamamlama işaretleme hatası: {e}")
            return False
    
    def mark_incomplete(self):
        """
        Alışkanlığı tamamlanmadı olarak işaretler
        Returns: bool - işlem başarılı ise True
        """
        try:
            self.is_completed = False
            return True
            
        except Exception as e:
            print(f"Tamamlanmama işaretleme hatası: {e}")
            return False
    
    def get_completion_status(self):
        """
        Tamamlama durumunu döndürür
        Returns: bool - tamamlanmış ise True
        """
        return self.is_completed
    
    def get_streak(self, all_records):
        """
        Mevcut alışkanlık için streak (sıralı gün) hesaplar
        Args: all_records - tüm kayıtların listesi
        Returns: int - streak sayısı
        """
        try:
            if not all_records:
                return 0
            
            # Bu alışkanlığa ait kayıtları filtrele
            habit_records = [r for r in all_records if r.habit_id == self.habit_id and r.is_completed]
            
            if not habit_records:
                return 0
            
            # Tarihleri sırala
            habit_records.sort(key=lambda x: x.completion_date)
            
            streak = 0
            current_date = datetime.datetime.now().date()
            
            # Bugünden geriye doğru kontrol et
            check_date = current_date
            
            for record in reversed(habit_records):
                if record.completion_date.date() == check_date:
                    streak += 1
                    check_date -= datetime.timedelta(days=1)
                elif record.completion_date.date() < check_date:
                    break
            
            return streak
            
        except Exception as e:
            print(f"Streak hesaplama hatası: {e}")
            return 0
    
    def get_weekly_completion(self, all_records):
        """
        Haftalık tamamlama oranını hesaplar
        Args: all_records - tüm kayıtların listesi
        Returns: dict - haftalık istatistikler
        """
        try:
            if not all_records:
                return {'completed': 0, 'total': 7, 'percentage': 0.0}
            
            # Bu hafta (son 7 gün)
            today = datetime.datetime.now().date()
            week_start = today - datetime.timedelta(days=6)
            
            # Bu alışkanlığa ait bu haftaki kayıtlar
            habit_records = [
                r for r in all_records 
                if (r.habit_id == self.habit_id and 
                    r.is_completed and 
                    week_start <= r.completion_date.date() <= today)
            ]
            
            completed_days = len(set(r.completion_date.date() for r in habit_records))
            total_days = 7
            percentage = (completed_days / total_days) * 100 if total_days > 0 else 0
            
            return {
                'completed': completed_days,
                'total': total_days,
                'percentage': round(percentage, 2)
            }
            
        except Exception as e:
            print(f"Haftalık tamamlama hesaplama hatası: {e}")
            return {'completed': 0, 'total': 7, 'percentage': 0.0}
    
    def get_monthly_completion(self, all_records):
        """
        Aylık tamamlama oranını hesaplar
        Args: all_records - tüm kayıtların listesi
        Returns: dict - aylık istatistikler
        """
        try:
            if not all_records:
                return {'completed': 0, 'total': 30, 'percentage': 0.0}
            
            # Bu ay
            today = datetime.datetime.now()
            month_start = today.replace(day=1)
            
            # Bu alışkanlığa ait bu ayki kayıtlar
            habit_records = [
                r for r in all_records 
                if (r.habit_id == self.habit_id and 
                    r.is_completed and 
                    month_start <= r.completion_date <= today)
            ]
            
            completed_days = len(set(r.completion_date.date() for r in habit_records))
            
            # Ayın gün sayısını hesapla
            if today.month == 12:
                next_month = today.replace(year=today.year + 1, month=1, day=1)
            else:
                next_month = today.replace(month=today.month + 1, day=1)
            
            total_days = (next_month - month_start).days
            percentage = (completed_days / total_days) * 100 if total_days > 0 else 0
            
            return {
                'completed': completed_days,
                'total': total_days,
                'percentage': round(percentage, 2)
            }
            
        except Exception as e:
            print(f"Aylık tamamlama hesaplama hatası: {e}")
            return {'completed': 0, 'total': 30, 'percentage': 0.0}
    
    def get_record_details(self):
        """
        Kayıt detaylarını döndürür
        Returns: dict - kayıt bilgileri
        """
        return {
            'record_id': self.record_id,
            'habit_id': self.habit_id,
            'completion_date': self.completion_date.strftime('%Y-%m-%d %H:%M:%S'),
            'is_completed': self.is_completed,
            'notes': self.notes
        }
    
    def set_notes(self, notes):
        """
        Kayıt notlarını günceller
        Returns: bool - işlem başarılı ise True
        """
        try:
            self.notes = notes
            return True
        except Exception as e:
            print(f"Not güncelleme hatası: {e}")
            return False
    
    def __str__(self):
        """
        String representation
        """
        status = "Tamamlandı" if self.is_completed else "Tamamlanmadı"
        return f"HabitRecord({self.habit_id}, {self.completion_date.strftime('%Y-%m-%d')}, {status})"
