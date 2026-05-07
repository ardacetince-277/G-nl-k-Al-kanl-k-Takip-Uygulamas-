# Günlük Alışkanlık Takip Uygulaması - Gereksinim Analizi

## Proje Adı
Günlük Alışkanlık Takip Uygulaması

## Proje Amacı
Kullanıcıların günlük alışkanlıklarını takip etmelerini sağlayan, basit ve kullanıcı dostu bir masaüstü uygulaması geliştirmek.

## Fonksiyonel Gereksinimler

### 1. Kullanıcı Yönetimi
- Kullanıcı kayıt olabilme
- Kullanıcı giriş yapabilme
- Kullanıcı bilgilerini güncelleme

### 2. Alışkanlık Yönetimi
- Yeni alışkanlık ekleme
- Mevcut alışkanlıkları görüntüleme
- Alışkanlık silme
- Alışkanlık düzenleme

### 3. Takip Özellikleri
- Günlük alışkanlık tamamlama kaydı
- Haftalık/aylık istatistikler
- Başarı yüzdesi hesaplama
- Streak (sıralı gün) takibi

### 4. Veri Yönetimi
- Verileri dosyaya kaydetme
- Verileri dosyadan yükleme
- Veri yedekleme

## Non-Fonksiyonel Gereksinimler

### 1. Kullanılabilirlik
- Basit ve anlaşılır arayüz
- Türkçe dil desteği
- Hızlı yanıt süresi

### 2. Güvenilirlik
- Veri kaybı olmaması
- Hata yönetimi mekanizmaları
- Veri bütünlüğü

### 3. Performans
- Hızlı veri işleme
- Düşük kaynak kullanımı
- Uyumlu çalışma

## Kullanıcırolleri
- **Standart Kullanıcı**: Uygulamayı kullanarak alışkanlıklarını takip eden kişi

## Kullanım Senaryoları

### Senaryo 1: Yeni Alışkanlık Ekleme
1. Kullanıcı uygulamayı açar
2. "Yeni Alışkanlık Ekle" butonuna tıklar
3. Alışkanlık adını, açıklamasını ve hedefini girer
4. "Kaydet" butonuna tıklar
5. Sistem alışkanlığı kaydeder ve başarı mesajı gösterir

### Senaryo 2: Günlük Alışkanlık Tamamlama
1. Kullanıcı uygulamayı açar
2. Bugünkü alışkanlık listesini görür
3. Tamamladığı alışkanlığın yanındaki kutucuğu işaretler
4. Sistem tamamlama kaydını tutar

### Senaryo 3: İstatistikleri Görüntüleme
1. Kullanıcı "İstatistikler" menüsüne tıklar
2. Haftalık/aylık başarı oranlarını görür
3. En çok tamamladığı alışkanlıkları görür
4. Streak (sıralı gün) bilgisini görür

## Teknik Kısıtlamalar
- Python programlama dili kullanılacak
- Tkinter kütüphanesi ile GUI geliştirilecek
- Nesne yönelimli programlama prensipleri uygulanacak
- Veriler JSON formatında saklanacak
- Tek dosya 1000 satırı geçmeyecek şekilde modüler tasarım yapılacak

## Varsayımlar
- Kullanıcının bilgisayarında Python kurulu olduğu varsayılır
- Kullanıcının temel bilgisayar kullanabildiği varsayılır
