"""
Main Application Entry Point
Günlük Alışkanlık Takip Uygulaması ana başlangıç dosyası
"""

import sys
import os

# Src klasörünü Python path'ine ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ui.MainWindow import MainWindow


def main():
    """
    Ana uygulama fonksiyonu
    """
    try:
        # Uygulamayı başlat
        app = MainWindow()
        app.run()
        
    except KeyboardInterrupt:
        print("\nUygulama kullanıcı tarafından sonlandırıldı.")
    except Exception as e:
        print(f"Uygulama başlatma hatası: {e}")
        input("Çıkmak için Enter tuşuna basın...")


if __name__ == "__main__":
    main()
