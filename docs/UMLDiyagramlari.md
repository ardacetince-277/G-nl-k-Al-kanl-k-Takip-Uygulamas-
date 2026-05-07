# Günlük Alışkanlık Takip Uygulaması - UML Diyagramları

## 1. Use Case Diyagramı

### Aktörler
- **Kullanıcı**: Uygulamayı kullanan standart kullanıcı

### Use Case'ler

#### Kullanıcı Yönetimi
- **UC1: Kayıt Ol**: Kullanıcı sisteme yeni hesap oluşturur
- **UC2: Giriş Yap**: Kullanıcı sisteme giriş yapar
- **UC3: Profil Güncelle**: Kullanıcı profil bilgilerini günceller

#### Alışkanlık Yönetimi
- **UC4: Alışkanlık Ekle**: Yeni alışkanlık oluşturur
- **UC5: Alışkanlık Listele**: Mevcut alışkanlıkları görüntüler
- **UC6: Alışkanlık Düzenle**: Mevcut alışkanlığı günceller
- **UC7: Alışkanlık Sil**: Alışkanlığı sistemden kaldırır

#### Takip İşlemleri
- **UC8: Alışkanlık Tamamla**: Günlük alışkanlığı tamamladığını işaretler
- **UC9: İstatistik Görüntüle**: Haftalık/aylık istatistikleri görüntüler
- **UC10: İlerleme Görüntüle**: Genel ilerlemeyi ve başarı oranını görüntüler

#### Veri Yönetimi
- **UC11: Veri Kaydet**: Verileri dosyaya kaydeder
- **UC12: Veri Yükle**: Kaydedilmiş verileri yükler
- **UC13: Veri Yedekle**: Veri yedeği oluşturur

### Use Case Diyagramı (Metinsel Temsil)
```
              +-------------------+
              |      Kullanıcı    |
              +-------------------+
                       |
      +----------------+-----------------+
      |                |                 |
+-----+-----+    +-----+-----+    +-----+-----+
| Kayıt Ol  |    | Giriş Yap |    | Profil    |
+-----------+    +-----------+    | Güncelle  |
                                +-----------+
                                     |
      +----------------+-------------+-----------------+
      |                |             |                 |
+-----+-----+    +-----+-----+ +-----+-----+    +-----+-----+
| Alışkanlık |    | Alışkanlık| | Alışkanlık|    | Alışkanlık|
| Ekle       |    | Listele   | | Düzenle   |    | Sil       |
+-----------+    +-----------+ +-----------+    +-----------+
                                     |
      +----------------+-------------+-----------------+
      |                |             |                 |
+-----+-----+    +-----+-----+ +-----+-----+    +-----+-----+
| Alışkanlık|    | İstatistik| | İlerleme  |    | Veri      |
| Tamamla    |    | Görüntüle | | Görüntüle |    | Yönetimi  |
+-----------+    +-----------+ +-----------+    +-----------+
```

## 2. Class Diyagramı

### Sınıflar ve Özellikleri

#### 1. Kullanıcı Sınıfı (User)
```python
class User:
    # Özellikler
    - user_id: int
    - username: str
    - email: str
    - password: str
    - created_date: datetime
    
    # Metotlar
    + register(): bool
    + login(): bool
    + update_profile(): bool
    + validate_input(): bool
```

#### 2. Alışkanlık Sınıfı (Habit)
```python
class Habit:
    # Özellikler
    - habit_id: int
    - user_id: int
    - name: str
    - description: str
    - target_frequency: int
    - created_date: datetime
    - is_active: bool
    
    # Metotlar
    + create_habit(): bool
    + update_habit(): bool
    + delete_habit(): bool
    + get_habit_details(): dict
```

#### 3. Alışkanlık Kaydı Sınıfı (HabitRecord)
```python
class HabitRecord:
    # Özellikler
    - record_id: int
    - habit_id: int
    - completion_date: datetime
    - is_completed: bool
    - notes: str
    
    # Metotlar
    + mark_completed(): bool
    + get_completion_status(): bool
    + get_streak(): int
```

#### 4. İstatistik Sınıfı (Statistics)
```python
class Statistics:
    # Özellikler
    - user_id: int
    - habit_id: int
    - completion_rate: float
    - current_streak: int
    - longest_streak: int
    - total_completions: int
    
    # Metotlar
    + calculate_completion_rate(): float
    + calculate_streak(): int
    + get_weekly_stats(): dict
    + get_monthly_stats(): dict
```

#### 5. Veri Yönetimi Sınıfı (DataManager)
```python
class DataManager:
    # Özellikler
    - file_path: str
    - backup_path: str
    
    # Metotlar
    + save_data(): bool
    + load_data(): dict
    + create_backup(): bool
    + restore_backup(): bool
    + validate_data(): bool
```

### Class İlişkileri

#### Kalıtım İlişkileri
- Yok (Her sınıf bağımsız)

#### Birliktelik İlişkileri
- **User** 1..* **Habit**: Bir kullanıcının birden fazla alışkanlığı olabilir
- **Habit** 1..* **HabitRecord**: Bir alışkanlığın birden fazla kaydı olabilir
- **User** 1..* **Statistics**: Bir kullanıcının birden fazla istatistiği olabilir
- **Habit** 1..* **Statistics**: Bir alışkanlığın birden fazla istatistiği olabilir
- **DataManager** ile diğer sınıflar: Veri yönetimi için kullanılır

### Class Diyagramı (Metinsel Temsil)
```
+-----------+       1..*     +-----------+
|   User    |◄----------------|   Habit   |
+-----------+                +-----------+
| -user_id  |                | -habit_id |
| -username |                | -name     |
| -email    |                | -desc     |
+-----------+                +-----------+
| +register |                | +create   |
| +login    |                | +update   |
| +update   |                | +delete   |
+-----------+                +-----------+
       |                           |
       | 1..*                      | 1..*
       |                           |
+-----------+                +-----------+
| Statistics|                |HabitRecord|
+-----------+                +-----------+
| -user_id  |                | -record_id|
| -habit_id |                | -habit_id |
| -rate     |                | -date     |
+-----------+                +-----------+
| +calc_rate|                | +mark     |
| +calc_streak|              | +get_status|
| +get_weekly|               +-----------+
+-----------+                    

+-------------+
| DataManager |
+-------------+
| -file_path  |
| -backup_path|
+-------------+
| +save       |
| +load       |
| +backup     |
| +restore    |
+-------------+
```

## 3. Sıra Diyagramı (Örnek: Alışkanlık Tamamlama)

```
Kullanıcı        UI         Controller        Habit        HabitRecord
   |              |              |              |              |
   |--------------->|              |              |              |
   | Tamamla       |              |              |              |
   | butonuna tıkla|              |              |              |
   |              |------------->|              |              |
   |              | İsteği işle   |              |              |
   |              |------------->|              |              |
   |              |              | Kaydı oluştur|              |
   |              |              |------------->|              |
   |              |              |              | Kaydet       |
   |              |              |<-------------|              |
   |              |              | Başarı dön   |              |
   |              |<-------------|              |              |
   |              | Güncelleme    |              |              |
   |              | göster        |              |              |
   |<-------------|              |              |              |
   | Onay mesajı  |              |              |              |
```

## 4. Aktivite Diyagramı (Örnek: Yeni Alışkanlık Ekleme)

```
[Başla]
   |
   v
[Kullanıcı giriş yapmış mı?]
   |
   |--Hayır-->[Giriş sayfasına yönlendir]
   |
   v
[Alışkanlık formunu göster]
   |
   v
[Kullanıcı bilgileri girer]
   |
   v
[Verileri doğrula]
   |
   |--Geçersiz-->[Hata mesajı göster]----|
   |                                    |
   v                                    |
[Geçerli]                               |
   |                                    |
   v                                    |
[Alışkanlığı veritabanına kaydet]       |
   |                                    |
   v                                    |
[Başarı mesajı göster]                  |
   |                                    |
   v                                    |
[Alışkanlık listesini güncelle]--------|
   |
   v
[Bit]
```
