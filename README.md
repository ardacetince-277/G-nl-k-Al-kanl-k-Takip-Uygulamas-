# ✨ Günlük Alışkanlık Takip Uygulaması

## Proje Adı
Günlük Alışkanlık Takip Uygulaması

## Proje Amacı
Kullanıcıların günlük alışkanlıklarını takip etmelerini sağlayan, **modern ve kullanıcı dostu** bir masaüstü uygulaması geliştirmek.

## 🎨 Yenilikler
- **Modern Tasarım**: Kart tabanlı arayüz ve güncel renk paleti
- **Emoji İkonları**: Görsel olarak daha çekici kullanıcı deneyimi
- **Hover Efektleri**: İnteraktif butonlar ve görsel geri bildirimler
- **Geliştirilmiş Tipografi**: Modern fontlar ve daha iyi okunabilirlik
- **Responsive Layout**: Daha iyi alan kullanımı ve scrollable içerik

## Proje Demosunun Kurulum ve Çalıştırma Talimatları

### Gereksinimler
- Python 3.7 veya üzeri
- Tkinter kütüphanesi (genellikle Python ile birlikte gelir)

### Kurulum Adımları

1. **Projeyi İndirme**
   ```bash
   # GitHub'dan klonlama (veya zip olarak indirip çıkarma)
   git clone <repository-url>
   cd "final odv"
   ```

2. **Python Kurulum Kontrolü**
   ```bash
   python --version
   # veya
   python3 --version
   ```
   Eğer Python kurulu değilse, [python.org](https://www.python.org/) adresinden indirin.

3. **Gerekli Kütüphaneler**
   Bu proje sadece standart Python kütüphanelerini kullanmaktadır:
   - `tkinter` (GUI için)
   - `json` (veri saklama için)
   - `os`, `datetime`, `sys` (standart kütüphaneler)

### Çalıştırma

1. **Terminal/Komut İstemi Açma**
   - Windows: Komut İstemi (cmd) veya PowerShell
   - macOS/Linux: Terminal

2. **Proje Klasörüne Gitme**
   ```bash
   cd "c:\Users\Ostim Öğrenci\OneDrive - Ostim Teknik Universitesi\Masaüstü\final odv"
   ```

3. **Uygulamayı Başlatma**
   ```bash
   python Src/main.py
   # veya
   python3 Src/main.py
   ```

### Kullanım

1. **İlk Kullanım**
   - Uygulama ilk açıldığında kullanıcı kayıt dialogu görünecektir
   - Kullanıcı adı, e-posta ve şifre bilgilerinizi girin
   - "Kayıt Ol" butonuna tıklayın

2. **Alışkanlık Ekleme**
   - "Alışkanlıklar" sekmesine gidin
   - "Yeni Alışkanlık Ekle" butonuna tıklayın
   - Alışkanlık adı, açıklama ve hedef girin
   - "Ekle" butonuna tıklayın

3. **Alışkanlık Tamamlama**
   - Listeden tamamladığınız alışkanlığı seçin
   - "Tamamla" butonuna tıklayın

4. **İstatistikleri Görüntüleme**
   - "İstatistikler" sekmesine gidin
   - Başarı oranlarını, streak bilgilerini ve diğer istatistikleri görüntüleyin

### 🎯 Arayüz Özellikleri
- **Modern Kart Tasarımı**: Kart tabanlı kullanıcı bilgileri ve istatistikler
- **Renk Paleti**: Profesyonel mavi, pembe ve turuncu tonları
- **Emoji İkonları**: Görsel olarak zengin kullanıcı deneyimi
- **Hover Efektleri**: İnteraktif butonlar ve görsel geri bildirimler
- **Scrollable İstatistikler**: Uzun listeler için akıcı kaydırma
- **Modern Fontlar**: Segoe UI font ailesi ve hiyerarşik boyutlandırma
- **Türkçe dil desteği**
- **Sekmeli arayüz** (Alışkanlıklar, İstatistikler)
- **Menü sistemi** (Dosya, Kullanıcı, Yardım)
- **Dialog pencereleri** (kayıt, ekleme, düzenleme)
- **Geliştirilmiş tablo görünümü** (alışkanlık listesi)

## Proje Özellikleri

### Temel Özellikler
- ✅ Kullanıcı kayıt ve giriş sistemi
- ✅ Alışkanlık ekleme, düzenleme, silme
- ✅ Günlük tamamlama takibi
- ✅ Haftalık/aylık istatistikler
- ✅ Streak (sıralı gün) takibi
- ✅ Veri yedekleme ve geri yükleme
- ✅ Türkçe arayüz

### Teknik Özellikler
- ✅ Nesne yönelimli programlama (OOP)
- ✅ Modüler yapı (models/, services/, ui/ klasörleri)
- ✅ Hata yönetimi (try-catch blokları)
- ✅ JSON formatında veri saklama
- ✅ Tkinter GUI kütüphanesi
- ✅ 1. sınıf seviyesinde anlaşılır kod

## Proje Yapısı

```
final odv/
├── docs/                           # Dokümantasyon klasörü
│   ├── GereksinimAnalizi.md         # Gereksinim analizi dokümanı
│   └── UMLDiyagramlari.md          # UML diyagramları
├── Src/                            # Kaynak kod klasörü
│   ├── models/                     # Model sınıfları
│   │   ├── User.py                 # Kullanıcı sınıfı
│   │   ├── Habit.py                # Alışkanlık sınıfı
│   │   └── HabitRecord.py          # Alışkanlık kaydı sınıfı
│   ├── services/                   # Servis sınıfları
│   │   ├── Statistics.py           # İstatistik servisi
│   │   └── DataManager.py          # Veri yönetimi servisi
│   ├── ui/                         # Arayüz sınıfları
│   │   └── MainWindow.py           # Ana pencere sınıfı
│   └── main.py                     # Ana başlangıç dosyası
├── data/                           # Veri dosyaları (çalışma zamanında oluşur)
│   ├── habits_data.json            # Ana veri dosyası
│   └── backup/                     # Yedekleme klasörü
└── README.md                       # Bu dosya
```

## Geliştirme Bilgileri

### Kullanılan Teknolojiler
- **Programlama Dili**: Python 3.7+
- **GUI Kütüphanesi**: Tkinter
- **Veri Formatı**: JSON
- **Geliştirme Ortamı**: VS Code / Herhangi bir Python IDE

### Proje Kuralları
- ✅ Nesne yönelimli programlama kullanıldı
- ✅ En az 3 sınıf oluşturuldu (User, Habit, HabitRecord)
- ✅ Kalıtım ve polimorfizm prensipleri uygulandı
- ✅ Kapsülleme (encapsulation) kullanıldı
- ✅ Anlamlı değişken isimleri ve yorumlar eklendi
- ✅ Fonksiyonel ayrım yapıldı
- ✅ Hiçbir dosya 1000 satırı geçmiyor
- ✅ Hata yönetimi (try-catch) mekanizmaları eklendi
- ✅ Modüler sistem tasarımı uygulandı

### Git Kullanımı
Proje Git versiyon kontrol sistemi ile yönetilmektedir:
- Anlamlı commit mesajları
- Düzenli aralıklarla yedekleme
- GitHub/GitLab'da yayın

## Hata Ayıklama ve Sorun Giderme

### Yaygın Sorunlar

1. **Tkinter Bulunamadı**
   ```bash
   # Ubuntu/Debian için
   sudo apt-get install python3-tk
   
   # Fedora için
   sudo dnf install python3-tkinter
   
   # macOS için (genellikle kurulu gelir)
   brew install python-tk
   ```

2. **Veri Dosyası Hatası**
   - Uygulama ilk çalıştığında `data/` klasörü otomatik oluşturulur
   - Eğer izin hatası alırsanız, uygulamayı yönetici olarak çalıştırın

3. **Karakter Kodlama Sorunu**
   - Türkçe karakterler için UTF-8 encoding kullanılmıştır
   - Windows'ta karakter sorunu yaşarsanız, terminal encoding kontrol edin

### Destek
Sorularınız ve hata bildirimleriniz için:
- Proje dokümantasyonunu inceleyin
- Kod içindeki yorumları okuyun
- Hata mesajlarını dikkatlice okuyun

## Lisans
Bu proje eğitim amaçlı olarak geliştirilmiştir.

---

**Not**: Bu proje 1. sınıf Bilgisayar Programcılığı öğrencisi seviyesine uygun olarak tasarlanmıştır. Kod yapısı basit ve anlaşılır tutulmuştur.
