"""
User Model Class
Kullanıcı bilgilerini yöneten sınıf
"""

import datetime
import re


class User:
    """
    Kullanıcı sınıfı
    Kullanıcı kayıt, giriş ve profil yönetimi işlemlerini yönetir
    """
    
    def __init__(self, username="", email="", password=""):
        """
        User sınıfı constructor
        """
        self.user_id = None
        self.username = username
        self.email = email
        self.password = password
        self.created_date = datetime.datetime.now()
    
    def register(self, username, email, password):
        """
        Yeni kullanıcı kaydı oluşturur
        Returns: bool - işlem başarılı ise True
        """
        try:
            # Giriş doğrulama
            if not self.validate_input(username, email, password):
                return False
            
            self.username = username
            self.email = email
            self.password = password  # Gerçek uygulamada hash'lenmeli
            self.created_date = datetime.datetime.now()
            
            # User ID atanması (basit artan sayı)
            self.user_id = hash(username + email) % 10000
            
            return True
            
        except Exception as e:
            print(f"Kayıt hatası: {e}")
            return False
    
    def login(self, username, password):
        """
        Kullanıcı girişi kontrolü
        Returns: bool - giriş başarılı ise True
        """
        try:
            if self.username == username and self.password == password:
                return True
            return False
            
        except Exception as e:
            print(f"Giriş hatası: {e}")
            return False
    
    def update_profile(self, new_username=None, new_email=None):
        """
        Kullanıcı profil bilgilerini günceller
        Returns: bool - güncelleme başarılı ise True
        """
        try:
            if new_username and self.validate_username(new_username):
                self.username = new_username
            
            if new_email and self.validate_email(new_email):
                self.email = new_email
            
            return True
            
        except Exception as e:
            print(f"Profil güncelleme hatası: {e}")
            return False
    
    def validate_input(self, username, email, password):
        """
        Kullanıcı giriş bilgilerini doğrular
        Returns: bool - tüm bilgiler geçerli ise True
        """
        return (self.validate_username(username) and 
                self.validate_email(email) and 
                self.validate_password(password))
    
    def validate_username(self, username):
        """
        Kullanıcı adını doğrular
        Returns: bool - geçerli ise True
        """
        if not username or len(username) < 3:
            print("Kullanıcı adı en az 3 karakter olmalıdır")
            return False
        return True
    
    def validate_email(self, email):
        """
        E-posta adresini doğrular
        Returns: bool - geçerli ise True
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            print("Geçersiz e-posta formatı")
            return False
        return True
    
    def validate_password(self, password):
        """
        Şifreyi doğrular
        Returns: bool - geçerli ise True
        """
        if not password or len(password) < 6:
            print("Şifre en az 6 karakter olmalıdır")
            return False
        return True
    
    def get_user_info(self):
        """
        Kullanıcı bilgilerini döndürür
        Returns: dict - kullanıcı bilgileri
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __str__(self):
        """
        String representation
        """
        return f"User({self.username}, {self.email})"
