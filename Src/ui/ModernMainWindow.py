"""
Modern MainWindow GUI Class with CustomTkinter
CustomTkinter kullanarak koyu mod ve modern yuvarlak köşeli butonlarla arayüz
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import sys
import os

# Modelleri import et
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.User import User
from models.Habit import Habit
from models.HabitRecord import HabitRecord
from services.Statistics import Statistics
from services.DataManager import DataManager

# CustomTkinter ayarları
ctk.set_appearance_mode("dark")  # Koyu mod
ctk.set_default_color_theme("blue")  # Mavi tema


class ModernMainWindow:
    """
    Modern ana pencere sınıfı
    CustomTkinter ile koyu mod ve modern butonlar
    """
    
    def __init__(self):
        """
        Modern MainWindow constructor
        """
        # Ana pencere
        self.root = ctk.CTk()
        self.root.title("✨ Günlük Alışkanlık Takip Uygulaması")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Veri yönetimi
        self.data_manager = DataManager()
        
        # Veri listeleri
        self.users = []
        self.habits = []
        self.records = []
        
        # Mevcut kullanıcı
        self.current_user = None
        
        # Arayüz bileşenleri
        self.tabview = None
        self.habits_tree = None
        self.stats_frame = None
        
        # Verileri yükle
        self.load_data()
        
        # Arayüzü oluştur
        self.create_widgets()
        
        # Eğer kullanıcı yoksa, kayıt ol dialogunu göster
        if not self.users:
            self.show_registration_dialog()
    
    def create_widgets(self):
        """
        Modern ana arayüz bileşenlerini oluşturur
        """
        try:
            # Ana frame
            main_frame = ctk.CTkFrame(self.root)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Kullanıcı bilgisi
            self.create_user_info(main_frame)
            
            # Sekmeli arayüz
            self.create_tabview(main_frame)
            
        except Exception as e:
            messagebox.showerror("Arayüz Hatası", f"Arayüz oluşturulamadı: {e}")
    
    def create_tabview(self, parent):
        """
        Modern sekmeli arayüz oluşturur
        """
        self.tabview = ctk.CTkTabview(parent, width=1100, height=600)
        self.tabview.pack(fill="both", expand=True, pady=(20, 0))
        
        # Sekmeleri ekle
        self.tabview.add("📋 Alışkanlıklar")
        self.tabview.add("📊 İstatistikler")
        self.tabview.add("⚙️ Ayarlar")
        
        # Sekme içerikleri
        self.create_habits_tab()
        self.create_statistics_tab()
        self.create_settings_tab()
    
    def create_user_info(self, parent):
        """
        Modern kullanıcı bilgi bölümü oluşturur
        """
        user_frame = ctk.CTkFrame(parent)
        user_frame.pack(fill="x", pady=(0, 20))
        
        # Kullanıcı bilgisi
        if self.current_user:
            user_text = f"👤 {self.current_user.username} | 📧 {self.current_user.email}"
            status_color = "#4CAF50"  # Yeşil
        else:
            user_text = "⚠️ Kullanıcı giriş yapmamış"
            status_color = "#FF9800"  # Turuncu
        
        user_label = ctk.CTkLabel(
            user_frame, 
            text=user_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=status_color
        )
        user_label.pack(side="left", padx=20, pady=15)
        
        # Kullanıcı değiştir butonu
        change_user_btn = ctk.CTkButton(
            user_frame,
            text="🔄 Kullanıcı Değiştir",
            command=self.show_user_selection,
            width=150,
            height=35,
            fg_color="#2196F3",  # Mavi
            hover_color="#1976D2",
            text_color="white",
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        change_user_btn.pack(side="right", padx=20, pady=15)
    
    def create_habits_tab(self):
        """
        Modern alışkanlıklar sekmesi oluşturur
        """
        tab_frame = self.tabview.tab("📋 Alışkanlıklar")
        
        # Butonlar
        buttons_frame = ctk.CTkFrame(tab_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Modern butonlar
        buttons = [
            ("➕ Yeni Alışkanlık", self.show_add_habit_dialog, "#4CAF50"),
            ("✏️ Düzenle", self.show_edit_habit_dialog, "#2196F3"),
            ("🗑️ Sil", self.delete_habit, "#F44336"),
            ("✅ Tamamla", self.mark_habit_completed, "#FF9800")
        ]
        
        button_container = ctk.CTkFrame(buttons_frame)
        button_container.pack(pady=10)
        
        for text, command, color in buttons:
            btn = ctk.CTkButton(
                button_container,
                text=text,
                command=command,
                width=140,
                height=40,
                fg_color=color,
                hover_color=self.darken_color(color),
                text_color="white",
                corner_radius=12,
                font=ctk.CTkFont(size=11, weight="bold")
            )
            btn.pack(side="left", padx=10)
        
        # Alışkanlıklar listesi
        self.create_modern_habits_list(tab_frame)
    
    def create_modern_habits_list(self, parent):
        """
        Modern alışkanlıklar listesi oluşturur
        """
        # Scroll frame
        list_frame = ctk.CTkScrollableFrame(parent, height=400)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Başlıklar
        headers_frame = ctk.CTkFrame(list_frame)
        headers_frame.pack(fill="x", padx=5, pady=5)
        
        headers = ["ID", "Alışkanlık Adı", "Açıklama", "Hedef", "Durum", "Tarih"]
        header_widths = [50, 200, 250, 80, 100, 120]
        
        for i, (header, width) in enumerate(zip(headers, header_widths)):
            header_label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width,
                anchor="w"
            )
            header_label.pack(side="left", padx=5)
        
        # Alışkanlık kartları
        self.habits_cards_frame = ctk.CTkFrame(list_frame)
        self.habits_cards_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Listeyi güncelle
        self.refresh_habits_list()
    
    def create_statistics_tab(self):
        """
        Modern istatistikler sekmesi oluşturur
        """
        tab_frame = self.tabview.tab("📊 İstatistikler")
        
        # Başlık
        title_label = ctk.CTkLabel(
            tab_frame,
            text="📊 Alışkanlık İstatistikleri",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # İstatistikler için scrollable frame
        self.stats_scroll_frame = ctk.CTkScrollableFrame(tab_frame, height=500)
        self.stats_scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # İstatistikleri göster
        self.update_statistics_display()
    
    def create_settings_tab(self):
        """
        Ayarlar sekmesi oluşturur
        """
        tab_frame = self.tabview.tab("⚙️ Ayarlar")
        
        # Başlık
        title_label = ctk.CTkLabel(
            tab_frame,
            text="⚙️ Uygulama Ayarları",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Tema ayarları
        theme_frame = ctk.CTkFrame(tab_frame)
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        theme_label = ctk.CTkLabel(
            theme_frame,
            text="🎨 Tema Seçimi:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        theme_label.pack(pady=10)
        
        # Tema değiştir butonları
        theme_buttons_frame = ctk.CTkFrame(theme_frame)
        theme_buttons_frame.pack(pady=10)
        
        dark_btn = ctk.CTkButton(
            theme_buttons_frame,
            text="🌙 Koyu Mod",
            command=lambda: self.change_theme("dark"),
            width=120,
            height=40,
            fg_color="#1E1E1E",
            hover_color="#2D2D2D",
            text_color="white",
            corner_radius=10
        )
        dark_btn.pack(side="left", padx=10)
        
        light_btn = ctk.CTkButton(
            theme_buttons_frame,
            text="☀️ Açık Mod",
            command=lambda: self.change_theme("light"),
            width=120,
            height=40,
            fg_color="#F0F0F0",
            hover_color="#E0E0E0",
            text_color="black",
            corner_radius=10
        )
        light_btn.pack(side="left", padx=10)
        
        # Veri yönetimi butonları
        data_frame = ctk.CTkFrame(tab_frame)
        data_frame.pack(fill="x", padx=20, pady=10)
        
        data_label = ctk.CTkLabel(
            data_frame,
            text="💾 Veri Yönetimi:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        data_label.pack(pady=10)
        
        data_buttons_frame = ctk.CTkFrame(data_frame)
        data_buttons_frame.pack(pady=10)
        
        save_btn = ctk.CTkButton(
            data_buttons_frame,
            text="💾 Kaydet",
            command=self.save_data,
            width=100,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45A049",
            text_color="white",
            corner_radius=10
        )
        save_btn.pack(side="left", padx=10)
        
        backup_btn = ctk.CTkButton(
            data_buttons_frame,
            text="📦 Yedekle",
            command=self.create_backup,
            width=100,
            height=40,
            fg_color="#2196F3",
            hover_color="#1976D2",
            text_color="white",
            corner_radius=10
        )
        backup_btn.pack(side="left", padx=10)
    
    def change_theme(self, mode):
        """
        Tema değiştirir
        """
        ctk.set_appearance_mode(mode)
        messagebox.showinfo("Tema Değiştirildi", f"Tema {mode} moduna değiştirildi!")
    
    def darken_color(self, color):
        """
        Renk tonunu koyulaştırır
        """
        # Basit renk koyulaştırma
        if color.startswith("#"):
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            darker = tuple(int(c * 0.8) for c in rgb)
            return f'#{darker[0]:02x}{darker[1]:02x}{darker[2]:02x}'
        return color
    
    def refresh_habits_list(self):
        """
        Alışkanlıklar listesini günceller
        """
        try:
            # Mevcut kartları temizle
            for widget in self.habits_cards_frame.winfo_children():
                widget.destroy()
            
            if not self.current_user:
                no_user_label = ctk.CTkLabel(
                    self.habits_cards_frame,
                    text="⚠️ Lütfen önce kullanıcı giriş yapın!",
                    font=ctk.CTkFont(size=14)
                )
                no_user_label.pack(pady=20)
                return
            
            # Kullanıcının alışkanlıkları
            user_habits = [h for h in self.habits if h.user_id == self.current_user.user_id and h.is_active]
            
            if not user_habits:
                no_habits_label = ctk.CTkLabel(
                    self.habits_cards_frame,
                    text="📝 Henüz alışkanlık eklenmemiş!",
                    font=ctk.CTkFont(size=14)
                )
                no_habits_label.pack(pady=20)
                return
            
            # Her alışkanlık için kart
            for habit in user_habits:
                habit_card = ctk.CTkFrame(self.habits_cards_frame)
                habit_card.pack(fill="x", padx=5, pady=5)
                
                # Kart içeriği
                card_content = ctk.CTkFrame(habit_card)
                card_content.pack(fill="x", padx=10, pady=8)
                
                # Alışkanlık bilgileri
                info_text = f"🎯 {habit.name} | 📝 {habit.description} | 🎯 {habit.target_frequency}/gün"
                info_label = ctk.CTkLabel(
                    card_content,
                    text=info_text,
                    font=ctk.CTkFont(size=12),
                    anchor="w"
                )
                info_label.pack(fill="x")
                
                # Durum ve tarih
                status_text = f"✅ Aktif | 📅 {habit.created_date.strftime('%d.%m.%Y')}"
                status_label = ctk.CTkLabel(
                    card_content,
                    text=status_text,
                    font=ctk.CTkFont(size=10),
                    text_color="#4CAF50"
                )
                status_label.pack(fill="x", pady=(5, 0))
                
        except Exception as e:
            messagebox.showerror("Hata", f"Liste güncellenemedi: {e}")
    
    def update_statistics_display(self):
        """
        İstatistikler ekranını günceller
        """
        try:
            # Mevcut widget'ları temizle
            for widget in self.stats_scroll_frame.winfo_children():
                widget.destroy()
            
            if not self.current_user:
                no_user_label = ctk.CTkLabel(
                    self.stats_scroll_frame,
                    text="⚠️ İstatistikler için kullanıcı girişi yapın!",
                    font=ctk.CTkFont(size=16)
                )
                no_user_label.pack(pady=20)
                return
            
            # Kullanıcının alışkanlıkları
            user_habits = [h for h in self.habits if h.user_id == self.current_user.user_id and h.is_active]
            
            if not user_habits:
                no_habits_label = ctk.CTkLabel(
                    self.stats_scroll_frame,
                    text="📝 Henüz alışkanlık eklenmemiş!",
                    font=ctk.CTkFont(size=16)
                )
                no_habits_label.pack(pady=20)
                return
            
            # Her alışkanlık için istatistik kartı
            for habit in user_habits:
                stats_card = ctk.CTkFrame(self.stats_scroll_frame)
                stats_card.pack(fill="x", padx=10, pady=10)
                
                # Kart başlığı
                title_label = ctk.CTkLabel(
                    stats_card,
                    text=f"🎯 {habit.name}",
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                title_label.pack(pady=10)
                
                # İstatistikler
                stats = Statistics(habit.user_id, habit.habit_id)
                all_stats = stats.get_all_stats(self.records)
                
                # İstatistik grid
                stats_frame = ctk.CTkFrame(stats_card)
                stats_frame.pack(fill="x", padx=10, pady=(0, 10))
                
                # Sol kolon
                left_col = ctk.CTkFrame(stats_frame)
                left_col.pack(side="left", fill="both", expand=True, padx=5)
                
                ctk.CTkLabel(left_col, text="📈 Başarı Oranı", font=ctk.CTkFont(size=12)).pack()
                ctk.CTkLabel(left_col, text=f"%{all_stats.get('completion_rate', 0)}", 
                             font=ctk.CTkFont(size=14, weight="bold"), text_color="#4CAF50").pack()
                
                # Orta kolon
                middle_col = ctk.CTkFrame(stats_frame)
                middle_col.pack(side="left", fill="both", expand=True, padx=5)
                
                ctk.CTkLabel(middle_col, text="🔥 Mevcut Streak", font=ctk.CTkFont(size=12)).pack()
                ctk.CTkLabel(middle_col, text=f"{all_stats.get('current_streak', 0)} gün", 
                             font=ctk.CTkFont(size=14, weight="bold"), text_color="#FF9800").pack()
                
                # Sağ kolon
                right_col = ctk.CTkFrame(stats_frame)
                right_col.pack(side="left", fill="both", expand=True, padx=5)
                
                ctk.CTkLabel(right_col, text="✅ Toplam Tamamlama", font=ctk.CTkFont(size=12)).pack()
                ctk.CTkLabel(right_col, text=f"{all_stats.get('total_completions', 0)}", 
                             font=ctk.CTkFont(size=14, weight="bold"), text_color="#2196F3").pack()
                
        except Exception as e:
            messagebox.showerror("Hata", f"İstatistikler güncellenemedi: {e}")
    
    def show_registration_dialog(self):
        """
        Modern kullanıcı kayıt dialogu
        """
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Yeni Kullanıcı Kaydı")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        
        # Form frame
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form alanları
        ctk.CTkLabel(form_frame, text="👤 Kullanıcı Adı:", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(0, 5))
        username_entry = ctk.CTkEntry(form_frame, width=300, height=35)
        username_entry.pack(pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="📧 E-posta:", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(0, 5))
        email_entry = ctk.CTkEntry(form_frame, width=300, height=35)
        email_entry.pack(pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="🔒 Şifre:", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(0, 5))
        password_entry = ctk.CTkEntry(form_frame, width=300, height=35, show="*")
        password_entry.pack(pady=(0, 20))
        
        def register_user():
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get()
            
            if not username or not email or not password:
                messagebox.showerror("Hata", "Tüm alanları doldurun!")
                return
            
            user = User()
            if user.register(username, email, password):
                self.users.append(user)
                self.current_user = user
                self.save_data()
                self.create_user_info(self.root.winfo_children()[0])
                dialog.destroy()
                messagebox.showinfo("Başarı", "Kullanıcı başarıyla oluşturuldu!")
            else:
                messagebox.showerror("Hata", "Kullanıcı oluşturulamadı!")
        
        # Kayıt butonu
        register_btn = ctk.CTkButton(
            form_frame,
            text="📝 Kayıt Ol",
            command=register_user,
            width=200,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45A049",
            text_color="white",
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        register_btn.pack(pady=10)
    
    def show_add_habit_dialog(self):
        """
        Modern alışkanlık ekleme dialogu
        """
        if not self.current_user:
            messagebox.showwarning("Uyarı", "Önce kullanıcı girişi yapın!")
            return
        
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Yeni Alışkanlık Ekle")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # Form frame
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form alanları
        ctk.CTkLabel(form_frame, text="🎯 Alışkanlık Adı:", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(0, 5))
        name_entry = ctk.CTkEntry(form_frame, width=300, height=35)
        name_entry.pack(pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="📝 Açıklama:", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(0, 5))
        desc_entry = ctk.CTkEntry(form_frame, width=300, height=35)
        desc_entry.pack(pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="🎯 Hedef (gün):", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(0, 5))
        freq_entry = ctk.CTkEntry(form_frame, width=300, height=35)
        freq_entry.pack(pady=(0, 20))
        freq_entry.insert(0, "1")
        
        def add_habit():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()
            
            try:
                frequency = int(freq_entry.get())
            except ValueError:
                messagebox.showerror("Hata", "Hedef bir tam sayı olmalıdır!")
                return
            
            if not name:
                messagebox.showerror("Hata", "Alışkanlık adı boş olamaz!")
                return
            
            habit = Habit()
            if habit.create_habit(name, description, frequency, self.current_user.user_id):
                self.habits.append(habit)
                self.save_data()
                self.refresh_habits_list()
                dialog.destroy()
                messagebox.showinfo("Başarı", "Alışkanlık başarıyla eklendi!")
            else:
                messagebox.showerror("Hata", "Alışkanlık eklenemedi!")
        
        # Ekle butonu
        add_btn = ctk.CTkButton(
            form_frame,
            text="➕ Ekle",
            command=add_habit,
            width=200,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45A049",
            text_color="white",
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        add_btn.pack(pady=10)
    
    def show_edit_habit_dialog(self):
        """
        Modern alışkanlık düzenleme dialogu
        """
        # Basit implementasyon
        messagebox.showinfo("Bilgi", "Düzenleme özelliği yakında eklenecek!")
    
    def delete_habit(self):
        """
        Alışkanlık siler
        """
        # Basit implementasyon
        messagebox.showinfo("Bilgi", "Silme özelliği seçilen alışkanlık için çalışacak!")
    
    def mark_habit_completed(self):
        """
        Alışkanlığı tamamlandı olarak işaretler
        """
        # Basit implementasyon
        messagebox.showinfo("Bilgi", "Tamamlama özelliği seçilen alışkanlık için çalışacak!")
    
    def show_user_selection(self):
        """
        Kullanıcı seçim dialogu
        """
        if not self.users:
            messagebox.showinfo("Bilgi", "Henüz kullanıcı bulunmuyor!")
            return
        
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Kullanıcı Seç")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        
        # Form frame
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(form_frame, text="👤 Kullanıcı Seçin:", font=ctk.CTkFont(size=12)).pack(pady=10)
        
        # Kullanıcı seçimi
        user_names = [user.username for user in self.users]
        user_combo = ctk.CTkComboBox(form_frame, values=user_names, width=200, height=35)
        user_combo.pack(pady=10)
        if user_names:
            user_combo.set(user_names[0])
        
        def select_user():
            username = user_combo.get()
            for user in self.users:
                if user.username == username:
                    self.current_user = user
                    self.create_user_info(self.root.winfo_children()[0])
                    self.refresh_habits_list()
                    self.update_statistics_display()
                    dialog.destroy()
                    messagebox.showinfo("Başarı", f"{username} kullanıcısı seçildi!")
                    break
        
        # Seç butonu
        select_btn = ctk.CTkButton(
            form_frame,
            text="✅ Seç",
            command=select_user,
            width=150,
            height=35,
            fg_color="#2196F3",
            hover_color="#1976D2",
            text_color="white",
            corner_radius=8
        )
        select_btn.pack(pady=10)
    
    def save_data(self):
        """
        Verileri kaydeder
        """
        try:
            self.data_manager.save_data(self.users, self.habits, self.records)
            messagebox.showinfo("Başarı", "Veriler başarıyla kaydedildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Veri kaydedilemedi: {e}")
    
    def load_data(self):
        """
        Verileri yükler
        """
        try:
            data = self.data_manager.load_data()
            
            # Verileri nesnelere dönüştür
            self.users = []
            for user_data in data.get('users', []):
                user = User()
                user.user_id = user_data.get('user_id')
                user.username = user_data.get('username')
                user.email = user_data.get('email')
                user.password = user_data.get('password')
                user.created_date = datetime.datetime.strptime(user_data.get('created_date'), '%Y-%m-%d %H:%M:%S')
                self.users.append(user)
            
            self.habits = []
            for habit_data in data.get('habits', []):
                habit = Habit()
                habit.habit_id = habit_data.get('habit_id')
                habit.user_id = habit_data.get('user_id')
                habit.name = habit_data.get('name')
                habit.description = habit_data.get('description')
                habit.target_frequency = habit_data.get('target_frequency')
                habit.created_date = datetime.datetime.strptime(habit_data.get('created_date'), '%Y-%m-%d %H:%M:%S')
                habit.is_active = habit_data.get('is_active', True)
                self.habits.append(habit)
            
            self.records = []
            for record_data in data.get('records', []):
                record = HabitRecord()
                record.record_id = record_data.get('record_id')
                record.habit_id = record_data.get('habit_id')
                record.completion_date = datetime.datetime.strptime(record_data.get('completion_date'), '%Y-%m-%d %H:%M:%S')
                record.is_completed = record_data.get('is_completed', False)
                record.notes = record_data.get('notes', '')
                self.records.append(record)
            
            # İlk kullanıcıyı mevcut kullanıcı yap
            if self.users and not self.current_user:
                self.current_user = self.users[0]
                
        except Exception as e:
            messagebox.showerror("Hata", f"Veriler yüklenemedi: {e}")
    
    def create_backup(self):
        """
        Veri yedeği oluşturur
        """
        try:
            if self.data_manager.create_backup(self.users, self.habits, self.records):
                messagebox.showinfo("Başarı", "Yedek başarıyla oluşturuldu!")
            else:
                messagebox.showerror("Hata", "Yedek oluşturulamadı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Yedekleme hatası: {e}")
    
    def run(self):
        """
        Uygulamayı başlatır
        """
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Uygulama Hatası", f"Uygulama çalıştırılamadı: {e}")


if __name__ == "__main__":
    app = ModernMainWindow()
    app.run()
