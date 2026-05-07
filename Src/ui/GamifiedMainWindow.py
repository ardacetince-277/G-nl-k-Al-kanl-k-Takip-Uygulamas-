"""
Oyunlaştırılmış Ana Pencere
Gamified Daily Habit Tracker - XP, Seviye ve Bonus Sistemi
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import datetime
import sys
import os

# Modelleri import et
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.User import User
from models.Habit import Habit
from models.HabitRecord import HabitRecord

# Services import et
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
from GamifiedDataManager import GamifiedDataManager
from GamificationManager import GamificationManager

# CustomTkinter ayarları
ctk.set_appearance_mode("dark")  # Koyu mod
ctk.set_default_color_theme("blue")  # Mavi tema


class GamifiedMainWindow:
    """
    Oyunlaştırılmış ana pencere sınıfı
    XP, seviye ve bonus sistemi ile alışkanlık takibi
    """
    
    def __init__(self):
        """
        GamifiedMainWindow constructor
        """
        # Ana pencere oluştur
        self.root = ctk.CTk()
        self.root.title("🎮 Oyunlaştırılmış Alışkanlık Takip Uygulaması")
        self.root.geometry("1400x900")  # Daha büyük ekran
        self.root.resizable(True, True)
        
        # Veri yönetimi - Oyunlaştırılmış sistem
        self.data_manager = GamifiedDataManager()
        
        # Oyunlaştırma yöneticisi
        self.gamification = GamificationManager()
        
        # Varsayılan test kullanıcısı
        self.current_user = self.data_manager.get_default_user()
        
        # Arayüz bileşenleri
        self.level_panel = None
        self.level_progress_bar = None
        self.xp_label = None
        self.level_title_label = None
        self.tabview = None
        self.habits_frame = None
        self.stats_frame = None
        self.leaderboard_frame = None
        
        # Verileri yükle
        self.load_user_data()
        
        # Arayüzü oluştur
        self.create_widgets()
        
        # Ana ekranı direkt göster (giriş sorununu aşmak için)
        if self.current_user:
            self.show_main_interface()
        else:
            messagebox.showerror("Hata", "Test kullanıcısı oluşturulamadı!")
    
    def create_widgets(self):
        """
        Ana arayüz bileşenlerini oluşturur
        """
        try:
            # Ana frame
            main_frame = ctk.CTkFrame(self.root)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Seviye paneli (en üstte)
            self.create_level_panel(main_frame)
            
            # Sekmeli arayüz
            self.create_tabview(main_frame)
            
        except Exception as e:
            messagebox.showerror("Arayüz Hatası", f"Arayüz oluşturulamadı: {e}")
    
    def create_level_panel(self, parent):
        """
        Seviye ve XP gösterim paneli oluşturur
        Args: parent - ana frame
        """
        # Seviye paneli - en üstte şık bir panel
        self.level_panel = ctk.CTkFrame(parent, height=120)
        self.level_panel.pack(fill="x", pady=(0, 20))
        self.level_panel.pack_propagate(False)  # Sabit yükseklik
        
        # Panel içeriği
        panel_content = ctk.CTkFrame(self.level_panel)
        panel_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Sol taraf - Seviye bilgisi
        left_frame = ctk.CTkFrame(panel_content)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Seviye başlığı
        self.level_title_label = ctk.CTkLabel(
            left_frame,
            text="Yeni Başlayan",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#95A5A6"
        )
        self.level_title_label.pack(pady=(10, 5))
        
        # Seviye numarası
        self.level_number_label = ctk.CTkLabel(
            left_frame,
            text="Seviye 1",
            font=ctk.CTkFont(size=18, weight="normal")
        )
        self.level_number_label.pack()
        
        # Orta taraf - Progress bar
        middle_frame = ctk.CTkFrame(panel_content)
        middle_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        # XP etiketi
        self.xp_label = ctk.CTkLabel(
            middle_frame,
            text="0 XP • Sonraki seviye için 100 XP",
            font=ctk.CTkFont(size=14)
        )
        self.xp_label.pack(pady=(10, 5))
        
        # Progress bar - şık ve modern
        self.level_progress_bar = ctk.CTkProgressBar(
            middle_frame,
            width=300,
            height=25,
            progress_color="#3498DB",
            border_color="#2C3E50",
            border_width=2
        )
        self.level_progress_bar.pack(pady=5)
        
        # Progress yüzde
        self.progress_percentage_label = ctk.CTkLabel(
            middle_frame,
            text="0%",
            font=ctk.CTkFont(size=12)
        )
        self.progress_percentage_label.pack()
        
        # Sağ taraf - Rozetler
        right_frame = ctk.CTkFrame(panel_content)
        right_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        # Rozetler başlığı
        badges_title = ctk.CTkLabel(
            right_frame,
            text="🏆 Rozetler",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        badges_title.pack(pady=(10, 5))
        
        # Rozetler frame'i
        self.badges_frame = ctk.CTkFrame(right_frame)
        self.badges_frame.pack(fill="both", expand=True, padx=5)
    
    def create_tabview(self, parent):
        """
        Sekmeli arayüz oluşturur
        Args: parent - ana frame
        """
        self.tabview = ctk.CTkTabview(parent, width=1300, height=650)
        self.tabview.pack(fill="both", expand=True)
        
        # Sekmeleri ekle
        self.tabview.add("🎯 Alışkanlıklar")
        self.tabview.add("📊 İstatistikler")
        self.tabview.add("🏆 Liderlik Tablosu")
        self.tabview.add("⚙️ Ayarlar")
        
        # Sekme içeriklerini oluştur
        self.create_habits_tab()
        self.create_statistics_tab()
        self.create_leaderboard_tab()
        self.create_settings_tab()
    
    def create_habits_tab(self):
        """
        Alışkanlıklar sekmesini oluşturur
        """
        tab_frame = self.tabview.tab("🎯 Alışkanlıklar")
        
        # Butonlar
        buttons_frame = ctk.CTkFrame(tab_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Modern butonlar
        buttons = [
            ("➕ Yeni Alışkanlık", self.show_add_habit_dialog, "#4CAF50"),
            ("✏️ Düzenle", self.show_edit_habit_dialog, "#2196F3"),
            ("🗑️ Sil", self.delete_habit, "#F44336"),
            ("✅ Tamamla", self.complete_habit, "#FF9800"),
            ("🎁 Bonus Al", self.claim_streak_bonus, "#9B59B6")
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
        self.create_habits_list(tab_frame)
    
    def create_habits_list(self, parent):
        """
        Alışkanlıklar listesini oluşturur
        Args: parent - ana frame
        """
        # Scroll frame
        list_frame = ctk.CTkScrollableFrame(parent, height=450)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Başlıklar
        headers_frame = ctk.CTkFrame(list_frame)
        headers_frame.pack(fill="x", padx=5, pady=5)
        
        headers = ["ID", "Alışkanlık Adı", "Açıklama", "Zorluk", "XP", "Durum", "Tarih"]
        header_widths = [40, 200, 250, 80, 60, 100, 120]
        
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
        self.habits_frame = ctk.CTkFrame(list_frame)
        self.habits_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Listeyi güncelle
        self.refresh_habits_list()
    
    def create_statistics_tab(self):
        """
        İstatistikler sekmesini oluşturur
        """
        tab_frame = self.tabview.tab("📊 İstatistikler")
        
        # Başlık
        title_label = ctk.CTkLabel(
            tab_frame,
            text="📊 Oyunlaştırılmış İstatistikler",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # İstatistikler için scrollable frame
        self.stats_frame = ctk.CTkScrollableFrame(tab_frame, height=500)
        self.stats_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # İstatistikleri göster
        self.update_statistics_display()
    
    def create_leaderboard_tab(self):
        """
        Liderlik tablosu sekmesini oluşturur
        """
        tab_frame = self.tabview.tab("🏆 Liderlik Tablosu")
        
        # Başlık
        title_label = ctk.CTkLabel(
            tab_frame,
            text="🏆 En İyi Oyuncular",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Liderlik tablosu frame'i
        self.leaderboard_frame = ctk.CTkScrollableFrame(tab_frame, height=500)
        self.leaderboard_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Liderlik tablosunu güncelle
        self.update_leaderboard_display()
    
    def create_settings_tab(self):
        """
        Ayarlar sekmesini oluşturur
        """
        tab_frame = self.tabview.tab("⚙️ Ayarlar")
        
        # Başlık
        title_label = ctk.CTkLabel(
            tab_frame,
            text="⚙️ Oyun Ayarları",
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
        
        # Kullanıcı bilgileri
        user_info_frame = ctk.CTkFrame(tab_frame)
        user_info_frame.pack(fill="x", padx=20, pady=10)
        
        user_info_label = ctk.CTkLabel(
            user_info_frame,
            text="👤 Kullanıcı Bilgileri:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        user_info_label.pack(pady=10)
        
        # Kullanıcı bilgilerini göster
        self.show_user_info(user_info_frame)
    
    def show_user_info(self, parent):
        """
        Kullanıcı bilgilerini gösterir
        Args: parent - ana frame
        """
        try:
            if not self.current_user:
                return
            
            info_frame = ctk.CTkFrame(parent)
            info_frame.pack(pady=10)
            
            info_text = f"""
👤 Kullanıcı Adı: {self.current_user['username']}
📧 E-posta: {self.current_user['email']}
📅 Kayıt Tarihi: {self.current_user['created_date']}
🎮 Hesap Türü: Test Kullanıcısı
            """
            
            info_label = ctk.CTkLabel(
                info_frame,
                text=info_text.strip(),
                font=ctk.CTkFont(size=12),
                justify="left"
            )
            info_label.pack(padx=20, pady=10)
            
        except Exception as e:
            print(f"Kullanıcı bilgileri gösterme hatası: {e}")
    
    def load_user_data(self):
        """
        Kullanıcı verilerini yükler
        """
        try:
            if self.current_user:
                # Kullanıcı istatistiklerini yükle
                self.user_stats = self.data_manager.get_user_statistics_with_gamification(
                    self.current_user['user_id']
                )
                
                print(f"Kullanıcı verileri yüklendi: {self.current_user['username']}")
            else:
                self.user_stats = {}
                
        except Exception as e:
            print(f"Kullanıcı verileri yükleme hatası: {e}")
            self.user_stats = {}
    
    def update_level_panel(self):
        """
        Seviye panelini günceller
        """
        try:
            if not self.user_stats:
                return
            
            # Seviye bilgilerini al
            level = self.user_stats.get('current_level', 1)
            total_xp = self.user_stats.get('total_xp', 0)
            xp_for_next = self.user_stats.get('xp_for_next_level', 100)
            progress = self.user_stats.get('progress_percentage', 0.0)
            title = self.user_stats.get('title', 'Yeni Başlayan')
            color = self.user_stats.get('color', '#95A5A6')
            
            # Seviye başlığını güncelle
            self.level_title_label.configure(
                text=title,
                text_color=color
            )
            
            # Seviye numarasını güncelle
            self.level_number_label.configure(
                text=f"Seviye {level}"
            )
            
            # XP etiketini güncelle
            self.xp_label.configure(
                text=f"{total_xp} XP • Sonraki seviye için {xp_for_next} XP"
            )
            
            # Progress bar'ı güncelle
            self.level_progress_bar.set(progress)
            
            # Progress yüzdesini güncelle
            self.progress_percentage_label.configure(
                text=f"{int(progress * 100)}%"
            )
            
            # Rozetleri güncelle
            self.update_badges_display()
            
        except Exception as e:
            print(f"Seviye paneli güncelleme hatası: {e}")
    
    def update_badges_display(self):
        """
        Rozet gösterimini günceller
        """
        try:
            # Mevcut rozetleri temizle
            for widget in self.badges_frame.winfo_children():
                widget.destroy()
            
            if not self.user_stats:
                return
            
            achievements = self.user_stats.get('achievements', [])
            
            if not achievements:
                no_badges_label = ctk.CTkLabel(
                    self.badges_frame,
                    text="Henüz rozet yok",
                    font=ctk.CTkFont(size=12)
                )
                no_badges_label.pack()
                return
            
            # Rozetleri göster
            badges_row = ctk.CTkFrame(self.badges_frame)
            badges_row.pack()
            
            for i, achievement in enumerate(achievements[:5]):  # İlk 5 rozet
                badge_btn = ctk.CTkButton(
                    badges_row,
                    text=f"{achievement['icon']}",
                    width=40,
                    height=40,
                    fg_color="#F39C12",
                    hover_color="#E67E22",
                    text_color="white",
                    corner_radius=20,
                    font=ctk.CTkFont(size=16)
                )
                badge_btn.pack(side="left", padx=2)
                
                # Tooltip için (basit implementasyon)
                badge_btn.bind("<Enter>", lambda e, a=achievement: self.show_badge_tooltip(a))
                badge_btn.bind("<Leave>", self.hide_badge_tooltip)
            
        except Exception as e:
            print(f"Rozet güncelleme hatası: {e}")
    
    def show_badge_tooltip(self, achievement):
        """
        Rozet tooltip'ini gösterir
        Args: achievement - rozet bilgileri
        """
        # Basit tooltip implementasyonu
        try:
            tooltip_text = f"{achievement['name']}\n{achievement['description']}"
            print(f"Rozet: {tooltip_text}")
        except:
            pass
    
    def hide_badge_tooltip(self, event):
        """
        Rozet tooltip'ini gizler
        """
        pass
    
    def refresh_habits_list(self):
        """
        Alışkanlıklar listesini günceller
        """
        try:
            # Mevcut kartları temizle
            for widget in self.habits_frame.winfo_children():
                widget.destroy()
            
            if not self.current_user:
                no_user_label = ctk.CTkLabel(
                    self.habits_frame,
                    text="⚠️ Kullanıcı bulunamadı!",
                    font=ctk.CTkFont(size=14)
                )
                no_user_label.pack(pady=20)
                return
            
            # Kullanıcının alışkanlıklarını al
            habits = self.data_manager.get_user_habits_with_difficulty(
                self.current_user['user_id'], True
            )
            
            if not habits:
                no_habits_label = ctk.CTkLabel(
                    self.habits_frame,
                    text="📝 Henüz alışkanlık eklenmemiş!",
                    font=ctk.CTkFont(size=14)
                )
                no_habits_label.pack(pady=20)
                return
            
            # Her alışkanlık için kart
            for habit in habits:
                habit_card = ctk.CTkFrame(self.habits_frame)
                habit_card.pack(fill="x", padx=5, pady=5)
                
                # Kart içeriği
                card_content = ctk.CTkFrame(habit_card)
                card_content.pack(fill="x", padx=10, pady=8)
                
                # Alışkanlık bilgileri
                info_text = f"🎯 {habit['name']} | 📝 {habit['description']} | 🎯 {habit['target_frequency']}/gün"
                info_label = ctk.CTkLabel(
                    card_content,
                    text=info_text,
                    font=ctk.CTkFont(size=12),
                    anchor="w"
                )
                info_label.pack(fill="x")
                
                # Zorluk ve XP bilgisi
                difficulty_text = f"⚡ {habit['difficulty']} | 💎 {habit['xp_value']} XP"
                difficulty_label = ctk.CTkLabel(
                    card_content,
                    text=difficulty_text,
                    font=ctk.CTkFont(size=10),
                    text_color=habit['difficulty_color']
                )
                difficulty_label.pack(fill="x", pady=(5, 0))
                
                # Durum ve tarih
                status_text = f"✅ Aktif | 📅 {habit['created_date'].split()[0]}"
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
            for widget in self.stats_frame.winfo_children():
                widget.destroy()
            
            if not self.user_stats:
                no_stats_label = ctk.CTkLabel(
                    self.stats_frame,
                    text="⚠️ İstatistikler için kullanıcı gerekli!",
                    font=ctk.CTkFont(size=16)
                )
                no_stats_label.pack(pady=20)
                return
            
            # Ana istatistik kartı
            main_stats_card = ctk.CTkFrame(self.stats_frame)
            main_stats_card.pack(fill="x", padx=10, pady=10)
            
            # Başlık
            title_label = ctk.CTkLabel(
                main_stats_card,
                text=f"🎮 {self.current_user['username']} - Oyun İstatistikleri",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title_label.pack(pady=15)
            
            # İstatistik grid
            stats_grid = ctk.CTkFrame(main_stats_card)
            stats_grid.pack(fill="x", padx=20, pady=(0, 15))
            
            # Sol kolon - Seviye ve XP
            left_col = ctk.CTkFrame(stats_grid)
            left_col.pack(side="left", fill="both", expand=True, padx=10)
            
            ctk.CTkLabel(left_col, text="🎯 Mevcut Seviye", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
            ctk.CTkLabel(left_col, text=f"Seviye {self.user_stats.get('current_level', 1)}", 
                         font=ctk.CTkFont(size=16, weight="bold"), text_color="#3498DB").pack()
            
            ctk.CTkLabel(left_col, text="💎 Toplam XP", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
            ctk.CTkLabel(left_col, text=f"{self.user_stats.get('total_xp', 0)} XP", 
                         font=ctk.CTkFont(size=16, weight="bold"), text_color="#F39C12").pack()
            
            # Orta kolon - Alışkanlıklar
            middle_col = ctk.CTkFrame(stats_grid)
            middle_col.pack(side="left", fill="both", expand=True, padx=10)
            
            ctk.CTkLabel(middle_col, text="📝 Toplam Alışkanlık", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
            ctk.CTkLabel(middle_col, text=f"{self.user_stats.get('total_habits', 0)} adet", 
                         font=ctk.CTkFont(size=16, weight="bold"), text_color="#2ECC71").pack()
            
            ctk.CTkLabel(middle_col, text="✅ Tamamlanan", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
            ctk.CTkLabel(middle_col, text=f"{self.user_stats.get('total_habits_completed', 0)} kez", 
                         font=ctk.CTkFont(size=16, weight="bold"), text_color="#27AE60").pack()
            
            # Sağ kolon - Seri ve Sıralama
            right_col = ctk.CTkFrame(stats_grid)
            right_col.pack(side="left", fill="both", expand=True, padx=10)
            
            ctk.CTkLabel(right_col, text="🔥 En Uzun Seri", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
            ctk.CTkLabel(right_col, text=f"{self.user_stats.get('longest_streak', 0)} gün", 
                         font=ctk.CTkFont(size=16, weight="bold"), text_color="#E74C3C").pack()
            
            ctk.CTkLabel(right_col, text="🏆 Sıralama", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
            ctk.CTkLabel(right_col, text=f"#{self.user_stats.get('user_rank', 0)}", 
                         font=ctk.CTkFont(size=16, weight="bold"), text_color="#9B59B6").pack()
            
            # Zorluk dağılımı
            difficulty_frame = ctk.CTkFrame(self.stats_frame)
            difficulty_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(difficulty_frame, text="⚡ Zorluk Dağılımı", 
                         font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
            
            diff_dist = self.user_stats.get('difficulty_distribution', {})
            for difficulty, count in diff_dist.items():
                diff_item = ctk.CTkFrame(difficulty_frame)
                diff_item.pack(fill="x", padx=20, pady=5)
                
                color = self.gamification.get_difficulty_color(difficulty)
                ctk.CTkLabel(diff_item, text=f"{difficulty}:", 
                             font=ctk.CTkFont(size=12), text_color=color, width=100, anchor="w").pack(side="left")
                ctk.CTkLabel(diff_item, text=f"{count} alışkanlık", 
                             font=ctk.CTkFont(size=12), anchor="w").pack(side="left")
            
        except Exception as e:
            messagebox.showerror("Hata", f"İstatistikler güncellenemedi: {e}")
    
    def update_leaderboard_display(self):
        """
        Liderlik tablosunu günceller
        """
        try:
            # Mevcut widget'ları temizle
            for widget in self.leaderboard_frame.winfo_children():
                widget.destroy()
            
            # Liderlik tablosunu al
            leaderboard = self.data_manager.get_leaderboard_with_gamification(10)
            
            if not leaderboard:
                no_leaderboard_label = ctk.CTkLabel(
                    self.leaderboard_frame,
                    text="📊 Liderlik tablosu boş!",
                    font=ctk.CTkFont(size=16)
                )
                no_leaderboard_label.pack(pady=20)
                return
            
            # Başlık
            title_label = ctk.CTkLabel(
                self.leaderboard_frame,
                text="🏆 En İyi 10 Oyuncu",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title_label.pack(pady=15)
            
            # Liderlik tablosu başlıkları
            headers_frame = ctk.CTkFrame(self.leaderboard_frame)
            headers_frame.pack(fill="x", padx=20, pady=10)
            
            headers = ["Sıra", "Kullanıcı", "Seviye", "XP", "Alışkanlık", "Rozet"]
            header_widths = [60, 200, 80, 100, 100, 80]
            
            for i, (header, width) in enumerate(zip(headers, header_widths)):
                header_label = ctk.CTkLabel(
                    headers_frame,
                    text=header,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    width=width,
                    anchor="w"
                )
                header_label.pack(side="left", padx=5)
            
            # Liderlik tablosu içeriği
            for user in leaderboard:
                user_card = ctk.CTkFrame(self.leaderboard_frame)
                user_card.pack(fill="x", padx=20, pady=5)
                
                # Kullanıcı bilgileri
                user_info = f"#{user['rank']} • {user['username']} • Seviye {user['level']} • {user['total_xp']} XP"
                user_label = ctk.CTkLabel(
                    user_card,
                    text=user_info,
                    font=ctk.CTkFont(size=12),
                    anchor="w"
                )
                user_label.pack(fill="x", padx=10, pady=8)
                
        except Exception as e:
            messagebox.showerror("Hata", f"Liderlik tablosu güncellenemedi: {e}")
    
    def show_add_habit_dialog(self):
        """
        Yeni alışkanlık ekleme dialogu
        """
        if not self.current_user:
            messagebox.showwarning("Uyarı", "Kullanıcı bulunamadı!")
            return
        
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("🎯 Yeni Alışkanlık Ekle")
        dialog.geometry("420x380")  # Daha küçük pencere
        dialog.resizable(False, False)
        
        # Form frame - daha az padding
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=15, pady=15)  # Azaltılmış padding
        
        # Form alanları - daha az boşluk
        ctk.CTkLabel(form_frame, text="🎯 Alışkanlık Adı:", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(0, 3))
        name_entry = ctk.CTkEntry(form_frame, width=380, height=32)  # Daha küçük yükseklik
        name_entry.pack(pady=(0, 10))  # Azaltılmış boşluk
        
        ctk.CTkLabel(form_frame, text="📝 Açıklama:", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(0, 3))
        desc_entry = ctk.CTkEntry(form_frame, width=380, height=32)
        desc_entry.pack(pady=(0, 10))
        
        # Hedef ve zorluk yan yana
        fields_frame = ctk.CTkFrame(form_frame)
        fields_frame.pack(fill="x", pady=(0, 10))
        
        # Sol taraf - Hedef
        left_field = ctk.CTkFrame(fields_frame)
        left_field.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(left_field, text="🎯 Hedef:", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(0, 3))
        freq_entry = ctk.CTkEntry(left_field, width=180, height=32)
        freq_entry.pack()
        freq_entry.insert(0, "1")
        
        # Sağ taraf - Zorluk
        right_field = ctk.CTkFrame(fields_frame)
        right_field.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
        ctk.CTkLabel(right_field, text="⚡ Zorluk:", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(0, 3))
        difficulty_combo = ctk.CTkComboBox(right_field, values=["Düşük", "Orta", "Yüksek"], width=180, height=32)
        difficulty_combo.pack()
        difficulty_combo.set("Düşük")
        
        # Daha kompakt zorluk bilgileri
        difficulty_info_frame = ctk.CTkFrame(form_frame)
        difficulty_info_frame.pack(fill="x", pady=(0, 10))
        
        # Yan yana zorluk bilgileri
        diff_info_row = ctk.CTkFrame(difficulty_info_frame)
        diff_info_row.pack(pady=5)
        
        # Düşük
        diff_low = ctk.CTkFrame(diff_info_row)
        diff_low.pack(side="left", padx=5)
        ctk.CTkLabel(diff_low, text="🟢 Düşük", font=ctk.CTkFont(size=10, weight="bold"), text_color="#27AE60").pack()
        ctk.CTkLabel(diff_low, text="5 XP", font=ctk.CTkFont(size=9)).pack()
        
        # Orta
        diff_medium = ctk.CTkFrame(diff_info_row)
        diff_medium.pack(side="left", padx=5)
        ctk.CTkLabel(diff_medium, text="🟠 Orta", font=ctk.CTkFont(size=10, weight="bold"), text_color="#F39C12").pack()
        ctk.CTkLabel(diff_medium, text="15 XP", font=ctk.CTkFont(size=9)).pack()
        
        # Yüksek
        diff_high = ctk.CTkFrame(diff_info_row)
        diff_high.pack(side="left", padx=5)
        ctk.CTkLabel(diff_high, text="🔴 Yüksek", font=ctk.CTkFont(size=10, weight="bold"), text_color="#E74C3C").pack()
        ctk.CTkLabel(diff_high, text="30 XP", font=ctk.CTkFont(size=9)).pack()
        
        def add_habit():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()
            difficulty = difficulty_combo.get()
            
            # Validasyon
            if not name:
                messagebox.showwarning("Uyarı", "⚠️ Alışkanlık adı boş olamaz!")
                name_entry.focus()
                return
            
            if len(name) < 2:
                messagebox.showwarning("Uyarı", "⚠️ Alışkanlık adı çok kısa!")
                name_entry.focus()
                return
            
            try:
                frequency = int(freq_entry.get())
                if frequency < 1:
                    messagebox.showwarning("Uyarı", "⚠️ Hedef frekans 1'den küçük olamaz!")
                    freq_entry.focus()
                    return
            except ValueError:
                messagebox.showwarning("Uyarı", "⚠️ Hedef bir tam sayı olmalıdır!")
                freq_entry.focus()
                return
            
            # Alışkanlığı oluştur
            if self.data_manager.create_habit_with_difficulty(
                self.current_user['user_id'], name, description, difficulty, frequency
            ):
                # Verileri yenile
                self.load_user_data()
                self.refresh_habits_list()
                self.update_level_panel()
                
                dialog.destroy()
                messagebox.showinfo("Başarı", f"✅ {name} alışkanlığı eklendi!\n⚡ Zorluk: {difficulty}\n💎 XP: {self.gamification.calculate_habit_completion_xp(difficulty)}")
            else:
                messagebox.showerror("Hata", "Alışkanlık eklenemedi!")
        
        # Ekle butonu - daha küçük
        add_btn = ctk.CTkButton(
            form_frame,
            text="➕ Ekle",
            command=add_habit,
            width=180,  # Daha küçük genişlik
            height=35,  # Daha küçük yükseklik
            fg_color="#4CAF50",
            hover_color="#45A049",
            text_color="white",
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        add_btn.pack(pady=8)  # Azaltılmış boşluk
    
    def show_edit_habit_dialog(self):
        """
        Alışkanlık düzenleme dialogu
        """
        messagebox.showinfo("Bilgi", "Düzenleme özelliği yakında eklenecek!")
    
    def delete_habit(self):
        """
        Alışkanlığı siler
        """
        messagebox.showinfo("Bilgi", "Silme özelliği seçilen alışkanlık için çalışacak!")
    
    def complete_habit(self):
        """
        Alışkanlığı tamamlar ve XP verir
        """
        if not self.current_user:
            messagebox.showwarning("Uyarı", "Kullanıcı bulunamadı!")
            return
        
        # Basit implementasyon - ilk alışkanlığı tamamlar
        habits = self.data_manager.get_user_habits_with_difficulty(
            self.current_user['user_id'], True
        )
        
        if not habits:
            messagebox.showwarning("Uyarı", "Tamamlanacak alışkanlık yok!")
            return
        
        # İlk alışkanlığı tamamlar
        habit = habits[0]
        
        # Alışkanlığı tamamlama işlemi
        success, result = self.data_manager.complete_habit_with_xp(
            habit['habit_id'], 
            self.current_user['user_id']
        )
        
        if success:
            # Verileri yenile
            self.load_user_data()
            self.refresh_habits_list()
            self.update_level_panel()
            self.update_statistics_display()
            
            # Sonuç mesajı
            message = f"✅ {result['habit_name']} tamamlandı!\n"
            message += f"💎 {result['xp_gained']} XP kazanıldı!\n"
            message += f"⚡ Zorluk: {result['habit_difficulty']}"
            
            if result['level_up']:
                message += f"\n\n🎉 SEVİYE ATLADINIZ!\n"
                message += f"📈 Seviye {result['old_level']} → Seviye {result['new_level']}"
            
            if result['streak_bonus_given']:
                message += f"\n\n🎁 SERİ BONUSU!\n"
                message += f"💎 {result['streak_bonus_xp']} XP bonus kazanıldı!"
            
            messagebox.showinfo("Başarı!", message)
        else:
            messagebox.showerror("Hata", result.get('error', 'Alışkanlık tamamlanamadı!'))
    
    def claim_streak_bonus(self):
        """
        Seri bonusunu talep eder
        """
        if not self.current_user:
            messagebox.showwarning("Uyarı", "Kullanıcı bulunamadı!")
            return
        
        # Seri bonus bilgilerini al
        streak_info = self.data_manager.user_stats_manager.get_streak_bonus_info(
            self.current_user['user_id']
        )
        
        if streak_info['can_get_bonus']:
            # Bonusu talep et
            success, level_up, old_level, new_level = self.data_manager.user_stats_manager.award_streak_bonus(
                self.current_user['user_id']
            )
            
            if success:
                # Verileri yenile
                self.load_user_data()
                self.update_level_panel()
                self.update_statistics_display()
                
                message = f"🎁 SERİ BONUSU KAZANILDI!\n"
                message += f"💎 {streak_info['bonus_xp']} XP kazanıldı!\n"
                message += f"🔥 {streak_info['current_streak']} gün seri!"
                
                if level_up:
                    message += f"\n\n🎉 SEVİYE ATLADINIZ!\n"
                    message += f"📈 Seviye {old_level} → Seviye {new_level}"
                
                messagebox.showinfo("Bonus Kazanıldı!", message)
            else:
                messagebox.showerror("Hata", "Bonus alınamadı!")
        else:
            days_until = streak_info['days_until_bonus']
            current_streak = streak_info['current_streak']
            
            message = f"🎁 Seri bonusu için:\n"
            message += f"🔥 Mevcut seri: {current_streak} gün\n"
            message += f"📅 Gerekli seri: 7 gün\n"
            
            if current_streak < 7:
                message += f"⏳ Eksik gün: {7 - current_streak} gün"
            else:
                message += f"⏳ Bonus için bekleme: {days_until} gün"
            
            messagebox.showinfo("Bonus Bilgisi", message)
    
    def change_theme(self, mode):
        """
        Tema değiştirir
        Args: mode - tema modu ("dark" veya "light")
        """
        ctk.set_appearance_mode(mode)
        messagebox.showinfo("Tema Değiştirildi", f"Tema {mode} moduna değiştirildi!")
    
    def darken_color(self, color):
        """
        Renk tonunu koyulaştırır
        Args: color - renk kodu
        Returns: Koyulaştırılmış renk
        """
        if color.startswith("#"):
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            darker = tuple(int(c * 0.8) for c in rgb)
            return f'#{darker[0]:02x}{darker[1]:02x}{darker[2]:02x}'
        return color
    
    def show_main_interface(self):
        """
        Ana arayüzü gösterir
        """
        try:
            # Seviye panelini güncelle
            self.update_level_panel()
            
            # İstatistikleri güncelle
            self.update_statistics_display()
            
            # Liderlik tablosunu güncelle
            self.update_leaderboard_display()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Ana arayüz gösterilemedi: {e}")
    
    def run(self):
        """
        Uygulamayı başlatır
        """
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Uygulama Hatası", f"Uygulama çalıştırılamadı: {e}")
    
    def __del__(self):
        """
        Destructor - veritabanı bağlantısını kapatır
        """
        try:
            self.data_manager.close()
        except:
            pass


if __name__ == "__main__":
    app = GamifiedMainWindow()
    app.run()
