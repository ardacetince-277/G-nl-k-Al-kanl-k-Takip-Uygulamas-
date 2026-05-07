"""
Habit Model Class
Alışkanlık bilgilerini yöneten sınıf
"""

import datetime


class Habit:
    """
    Alışkanlık sınıfı
    Alışkanlık oluşturma, güncelleme ve silme işlemlerini yönetir
    """
    
    def __init__(self, name="", description="", target_frequency=1, user_id=None):
        """
        Habit sınıfı constructor
        """
        self.habit_id = None
        self.user_id = user_id
        self.name = name
        self.description = description
        self.target_frequency = target_frequency
        self.created_date = datetime.datetime.now()
        self.is_active = True
    
    def create_habit(self, name, description, target_frequency, user_id):
        """
        Yeni alışkanlık oluşturur
        Returns: bool - işlem başarılı ise True
        """
        try:
            if not self.validate_habit_data(name, target_frequency):
                return False
            
            self.name = name
            self.description = description
            self.target_frequency = target_frequency
            self.user_id = user_id
            self.created_date = datetime.datetime.now()
            self.is_active = True
            
            # Habit ID atanması
            self.habit_id = hash(name + str(user_id) + str(self.created_date)) % 10000
            
            return True
            
        except Exception as e:
            print(f"Alışkanlık oluşturma hatası: {e}")
            return False
    
    def update_habit(self, name=None, description=None, target_frequency=None):
        """
        Mevcut alışkanlığı günceller
        Returns: bool - güncelleme başarılı ise True
        """
        try:
            if name and self.validate_name(name):
                self.name = name
            
            if description is not None:
                self.description = description
            
            if target_frequency and self.validate_frequency(target_frequency):
                self.target_frequency = target_frequency
            
            return True
            
        except Exception as e:
            print(f"Alışkanlık güncelleme hatası: {e}")
            return False
    
    def delete_habit(self):
        """
        Alışkanlığı siler (pasif hale getirir)
        Returns: bool - silme başarılı ise True
        """
        try:
            self.is_active = False
            return True
            
        except Exception as e:
            print(f"Alışkanlık silme hatası: {e}")
            return False
    
    def get_habit_details(self):
        """
        Alışkanlık detaylarını döndürür
        Returns: dict - alışkanlık bilgileri
        """
        return {
            'habit_id': self.habit_id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'target_frequency': self.target_frequency,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active
        }
    
    def validate_habit_data(self, name, target_frequency):
        """
        Alışkanlık verilerini doğrular
        Returns: bool - veriler geçerli ise True
        """
        return self.validate_name(name) and self.validate_frequency(target_frequency)
    
    def validate_name(self, name):
        """
        Alışkanlık adını doğrular
        Returns: bool - geçerli ise True
        """
        if not name or len(name.strip()) < 2:
            print("Alışkanlık adı en az 2 karakter olmalıdır")
            return False
        return True
    
    def validate_frequency(self, target_frequency):
        """
        Hedef frekansı doğrular
        Returns: bool - geçerli ise True
        """
        if not isinstance(target_frequency, int) or target_frequency < 1:
            print("Hedef frekans 1'den büyük pozitif tam sayı olmalıdır")
            return False
        return True
    
    def activate_habit(self):
        """
        Alışkanlığı aktif hale getirir
        Returns: bool - işlem başarılı ise True
        """
        try:
            self.is_active = True
            return True
        except Exception as e:
            print(f"Alışkanlık aktifleştirme hatası: {e}")
            return False
    
    def deactivate_habit(self):
        """
        Alışkanlığı pasif hale getirir
        Returns: bool - işlem başarılı ise True
        """
        try:
            self.is_active = False
            return True
        except Exception as e:
            print(f"Alışkanlık pasifleştirme hatası: {e}")
            return False
    
    def __str__(self):
        """
        String representation
        """
        status = "Aktif" if self.is_active else "Pasif"
        return f"Habit({self.name}, {self.target_frequency}/gün, {status})"
