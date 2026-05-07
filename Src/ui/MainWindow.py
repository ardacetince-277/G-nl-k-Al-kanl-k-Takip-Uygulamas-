"""
MainWindow GUI Class
Ana uygulama arayüzünü yöneten sınıf
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font
import datetime
import sys
import os
from tkinter import Canvas, Frame, Label, Button

# Modelleri import et
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.User import User
from models.Habit import Habit
from models.HabitRecord import HabitRecord
from services.Statistics import Statistics
from services.DataManager import DataManager


class MainWindow:
    """
    Ana pencere sınıfı
    Uygulamanın ana arayüzünü ve işlevselliğini yönetir
    """
    
    def __init__(self):
        """
        MainWindow constructor
        """
        self.root = tk.Tk()
        self.root.title("✨ Günlük Alışkanlık Takip Uygulaması")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Modern renk paleti
        self.colors = {
            'primary': '#2E86AB',      # Ana mavi
            'secondary': '#A23B72',    # Pembe
            'accent': '#F18F01',       # Turuncu
            'success': '#C73E1D',      # Kırmızı
            'bg_light': '#F5F5F5',     # Açık gri
            'bg_dark': '#2C3E50',      # Koyu lacivert
            'text_dark': '#2C3E50',    # Metin rengi
            'text_light': '#FFFFFF',    # Beyaz metin
            'card_bg': '#FFFFFF',      # Kart arka planı
            'border': '#E0E0E0'        # Kenarlık
        }
        
        # Modern fontlar
        self.fonts = {
            'title': font.Font(family='Segoe UI', size=16, weight='bold'),
            'subtitle': font.Font(family='Segoe UI', size=12, weight='bold'),
            'normal': font.Font(family='Segoe UI', size=10),
            'button': font.Font(family='Segoe UI', size=10, weight='bold'),
            'small': font.Font(family='Segoe UI', size=9)
        }
        
        # Ana arka plan rengi
        self.root.configure(bg=self.colors['bg_light'])
        
        # Veri yönetimi
        self.data_manager = DataManager()
        
        # Veri listeleri
        self.users = []
        self.habits = []
        self.records = []
        
        # Mevcut kullanıcı
        self.current_user = None
        
        # Arayüz bileşenleri
        self.notebook = None
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
        Ana arayüz bileşenlerini oluşturur
        """
        try:
            # Menü çubuğu
            self.create_menu()
            
            # Ana frame - modern stil
            main_frame = Frame(self.root, bg=self.colors['bg_light'], padx=20, pady=20)
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Kullanıcı bilgisi
            self.create_user_info(main_frame)
            
            # Modern sekmeli arayüz
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TNotebook', background=self.colors['bg_light'], borderwidth=0)
            style.configure('TNotebook.Tab', padding=[20, 10], font=self.fonts['subtitle'])
            style.map('TNotebook.Tab', background=[('selected', self.colors['primary']), ('active', self.colors['secondary'])])
            style.map('TNotebook.Tab', foreground=[('selected', self.colors['text_light']), ('active', self.colors['text_light'])])
            
            self.notebook = ttk.Notebook(main_frame)
            self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=15)
            
            # Alışkanlıklar sekmesi
            self.create_habits_tab()
            
            # İstatistikler sekmesi
            self.create_statistics_tab()
            
            # Grid ağırlıkları
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(0, weight=1)
            main_frame.rowconfigure(1, weight=1)
            
        except Exception as e:
            messagebox.showerror("Arayüz Hatası", f"Arayüz oluşturulamadı: {e}")
    
    def create_menu(self):
        """
        Menü çubuğunu oluşturur
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Dosya menüsü
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        file_menu.add_command(label="Veri Kaydet", command=self.save_data)
        file_menu.add_command(label="Veri Yükle", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Yedekle", command=self.create_backup)
        file_menu.add_command(label="Çıkış", command=self.root.quit)
        
        # Kullanıcı menüsü
        user_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Kullanıcı", menu=user_menu)
        user_menu.add_command(label="Profil Güncelle", command=self.show_profile_dialog)
        user_menu.add_command(label="Yeni Kullanıcı", command=self.show_registration_dialog)
        
        # Yardım menüsü
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        help_menu.add_command(label="Hakkında", command=self.show_about_dialog)
    
    def create_user_info(self, parent):
        """
        Kullanıcı bilgi bölümünü oluşturur - modern tasarım
        """
        # Modern kart tasarımı
        info_frame = Frame(parent, bg=self.colors['card_bg'], relief='flat', bd=1, highlightbackground=self.colors['border'], highlightthickness=1)
        info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Kart içeriği
        card_content = Frame(info_frame, bg=self.colors['card_bg'], padx=15, pady=12)
        card_content.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = Label(card_content, text="👤 Kullanıcı Bilgisi", 
                        font=self.fonts['subtitle'], 
                        bg=self.colors['card_bg'], fg=self.colors['primary'])
        title_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Kullanıcı bilgisi
        if self.current_user:
            user_text = f"📧 {self.current_user.username} | {self.current_user.email}"
            status_color = self.colors['success']
        else:
            user_text = "⚠️ Kullanıcı giriş yapmamış"
            status_color = self.colors['accent']
        
        self.user_label = Label(card_content, text=user_text, 
                             font=self.fonts['normal'],
                             bg=self.colors['card_bg'], fg=status_color)
        self.user_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Modern buton
        user_button = Button(card_content, text="🔄 Kullanıcı Değiştir", 
                          command=self.show_user_selection,
                          bg=self.colors['primary'], fg=self.colors['text_light'],
                          font=self.fonts['button'], relief='flat',
                          padx=20, pady=8, cursor='hand2')
        user_button.pack(anchor=tk.W)
        
        # Hover efekti
        user_button.bind('<Enter>', lambda e: user_button.config(bg=self.colors['secondary']))
        user_button.bind('<Leave>', lambda e: user_button.config(bg=self.colors['primary']))
    
    def darken_color(self, color):
        """
        Renk tonunu koyulaştırır
        """
        # Basit renk koyulaştırma
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darker = tuple(int(c * 0.8) for c in rgb)
        return f'#{darker[0]:02x}{darker[1]:02x}{darker[2]:02x}'
    
    def create_habits_tab(self):
        """
        Alışkanlıklar sekmesini oluşturur
        """
        habits_frame = ttk.Frame(self.notebook)
        self.notebook.add(habits_frame, text="Alışkanlıklar")
        
        # Modern buton çerçevesi
        buttons_frame = Frame(habits_frame, bg=self.colors['bg_light'], pady=15)
        buttons_frame.pack(fill=tk.X)
        
        # Butonlar için container
        button_container = Frame(buttons_frame, bg=self.colors['bg_light'])
        button_container.pack()
        
        # Modern butonlar
        buttons = [
            ("➕ Yeni Alışkanlık Ekle", self.show_add_habit_dialog, self.colors['primary']),
            ("✏️ Alışkanlık Düzenle", self.show_edit_habit_dialog, self.colors['secondary']),
            ("🗑️ Alışkanlık Sil", self.delete_habit, self.colors['accent']),
            ("✅ Tamamla", self.mark_habit_completed, self.colors['success'])
        ]
        
        for text, command, color in buttons:
            btn = Button(button_container, text=text, command=command,
                       bg=color, fg=self.colors['text_light'],
                       font=self.fonts['button'], relief='flat',
                       padx=15, pady=10, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=8)
            
            # Hover efekti
            btn.bind('<Enter>', lambda e, b=btn, c=color: b.config(bg=self.darken_color(c)))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.config(bg=c))
        
        # Modern alışkanlıklar listesi
        self.create_habits_list(habits_frame)
    
    def create_habits_list(self, parent):
        """
        Alışkanlıklar listesini oluşturur
        """
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Modern Treeview
        style = ttk.Style()
        style.configure('Treeview', background=self.colors['card_bg'], foreground=self.colors['text_dark'],
                     fieldbackground=self.colors['card_bg'], font=self.fonts['normal'])
        style.configure('Treeview.Heading', background=self.colors['primary'], foreground=self.colors['text_light'],
                     font=self.fonts['subtitle'])
        
        columns = ("ID", "Ad", "Açıklama", "Hedef", "Durum", "Oluşturulma")
        self.habits_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Sütun başlıkları
        self.habits_tree.heading("ID", text="ID")
        self.habits_tree.heading("Ad", text="Alışkanlık Adı")
        self.habits_tree.heading("Açıklama", text="Açıklama")
        self.habits_tree.heading("Hedef", text="Hedef (gün)")
        self.habits_tree.heading("Durum", text="Durum")
        self.habits_tree.heading("Oluşturulma", text="Oluşturulma Tarihi")
        
        # Sütun genişlikleri
        self.habits_tree.column("ID", width=50)
        self.habits_tree.column("Ad", width=150)
        self.habits_tree.column("Açıklama", width=200)
        self.habits_tree.column("Hedef", width=80)
        self.habits_tree.column("Durum", width=80)
        self.habits_tree.column("Oluşturulma", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.habits_tree.yview)
        self.habits_tree.configure(yscrollcommand=scrollbar.set)
        
        # Yerleşim
        self.habits_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listeyi güncelle
        self.refresh_habits_list()
    
    def create_statistics_tab(self):
        """
        İstatistikler sekmesini oluşturur - modern tasarım
        """
        self.stats_frame = Frame(self.notebook, bg=self.colors['bg_light'])
        self.notebook.add(self.stats_frame, text="📊 İstatistikler")
        
        # Modern istatistikler göster
        self.update_statistics_display()
    
    def show_registration_dialog(self):
        """
        Kullanıcı kayıt dialogunu gösterir
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("Yeni Kullanıcı Kaydı")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # Form alanları
        ttk.Label(dialog, text="Kullanıcı Adı:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        username_entry = ttk.Entry(dialog, width=30)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="E-posta:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        email_entry = ttk.Entry(dialog, width=30)
        email_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Şifre:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        password_entry = ttk.Entry(dialog, width=30, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=5)
        
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
                self.update_user_info()
                dialog.destroy()
                messagebox.showinfo("Başarı", "Kullanıcı başarıyla oluşturuldu!")
            else:
                messagebox.showerror("Hata", "Kullanıcı oluşturulamadı!")
        
        # Butonlar
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Kayıt Ol", command=register_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="İptal", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_add_habit_dialog(self):
        """
        Alışkanlık ekleme dialogunu gösterir
        """
        if not self.current_user:
            messagebox.showwarning("Uyarı", "Önce kullanıcı girişi yapın!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Yeni Alışkanlık Ekle")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        
        # Form alanları
        ttk.Label(dialog, text="Alışkanlık Adı:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Açıklama:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        desc_entry = ttk.Entry(dialog, width=30)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Hedef (gün):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        freq_entry = ttk.Entry(dialog, width=30)
        freq_entry.grid(row=2, column=1, padx=10, pady=5)
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
        
        # Butonlar
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Ekle", command=add_habit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="İptal", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def refresh_habits_list(self):
        """
        Alışkanlıklar listesini günceller
        """
        try:
            # Mevcut listeyi temizle
            for item in self.habits_tree.get_children():
                self.habits_tree.delete(item)
            
            # Kullanıcının alışkanlıklarını ekle
            user_habits = [h for h in self.habits if h.user_id == self.current_user.user_id and h.is_active]
            
            for habit in user_habits:
                status = "Aktif" if habit.is_active else "Pasif"
                self.habits_tree.insert("", tk.END, values=(
                    habit.habit_id,
                    habit.name,
                    habit.description,
                    habit.target_frequency,
                    status,
                    habit.created_date.strftime('%d.%m.%Y')
                ))
                
        except Exception as e:
            messagebox.showerror("Hata", f"Liste güncellenemedi: {e}")
    
    def mark_habit_completed(self):
        """
        Seçili alışkanlığı tamamlandı olarak işaretler
        """
        try:
            selection = self.habits_tree.selection()
            if not selection:
                messagebox.showwarning("Uyarı", "Lütfen bir alışkanlık seçin!")
                return
            
            item = self.habits_tree.item(selection[0])
            habit_id = item['values'][0]
            
            # Bugün için kayıt var mı kontrol et
            today = datetime.datetime.now().date()
            existing_record = None
            
            for record in self.records:
                if (record.habit_id == habit_id and 
                    record.completion_date.date() == today):
                    existing_record = record
                    break
            
            if existing_record and existing_record.is_completed:
                messagebox.showinfo("Bilgi", "Bu alışkanlık bugün zaten tamamlanmış!")
                return
            
            # Yeni kayıt oluştur
            if existing_record:
                existing_record.mark_completed()
            else:
                record = HabitRecord(habit_id, datetime.datetime.now())
                record.mark_completed()
                self.records.append(record)
            
            self.save_data()
            messagebox.showinfo("Başarı", "Alışkanlık tamamlandı olarak işaretlendi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"İşlem başarısız: {e}")
    
    def delete_habit(self):
        """
        Seçili alışkanlığı siler
        """
        try:
            selection = self.habits_tree.selection()
            if not selection:
                messagebox.showwarning("Uyarı", "Lütfen bir alışkanlık seçin!")
                return
            
            if messagebox.askyesno("Onay", "Seçili alışkanlığı silmek istediğinizden emin misiniz?"):
                item = self.habits_tree.item(selection[0])
                habit_id = item['values'][0]
                
                # Alışkanlığı bul ve sil
                for habit in self.habits:
                    if habit.habit_id == habit_id:
                        habit.delete_habit()
                        break
                
                self.save_data()
                self.refresh_habits_list()
                messagebox.showinfo("Başarı", "Alışkanlık silindi!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Silme işlemi başarısız: {e}")
    
    def update_statistics_display(self):
        """
        İstatistikler ekranını günceller - modern tasarım
        """
        try:
            # Mevcut widget'ları temizle
            for widget in self.stats_frame.winfo_children():
                widget.destroy()
            
            if not self.current_user:
                # Modern mesaj kartı
                msg_frame = Frame(self.stats_frame, bg=self.colors['card_bg'], relief='flat', bd=1, 
                               highlightbackground=self.colors['border'], highlightthickness=1)
                msg_frame.pack(pady=20, padx=20, fill=tk.X)
                
                Label(msg_frame, text="⚠️ İstatistikler için kullanıcı girişi yapın!", 
                      font=self.fonts['subtitle'], bg=self.colors['card_bg'], 
                      fg=self.colors['accent']).pack(padx=20, pady=15)
                return
            
            # Modern başlık
            title_frame = Frame(self.stats_frame, bg=self.colors['bg_light'])
            title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
            
            Label(title_frame, text="📊 Alışkanlık İstatistikleri", 
                  font=self.fonts['title'], bg=self.colors['bg_light'], 
                  fg=self.colors['primary']).pack()
            
            # Kullanıcının alışkanlıkları
            user_habits = [h for h in self.habits if h.user_id == self.current_user.user_id and h.is_active]
            
            if not user_habits:
                # Modern boş durum mesajı
                empty_frame = Frame(self.stats_frame, bg=self.colors['card_bg'], relief='flat', bd=1,
                                highlightbackground=self.colors['border'], highlightthickness=1)
                empty_frame.pack(pady=20, padx=20, fill=tk.X)
                
                Label(empty_frame, text="📝 Henüz alışkanlık eklenmemiş!", 
                      font=self.fonts['subtitle'], bg=self.colors['card_bg'], 
                      fg=self.colors['text_dark']).pack(padx=20, pady=15)
                return
            
            # İstatistik kartları için scrollable frame
            canvas = Canvas(self.stats_frame, bg=self.colors['bg_light'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(self.stats_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg=self.colors['bg_light'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Her alışkanlık için modern istatistik kartı
            for i, habit in enumerate(user_habits):
                # Modern kart tasarımı
                habit_card = Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=1,
                              highlightbackground=self.colors['border'], highlightthickness=1)
                habit_card.pack(padx=20, pady=10, fill=tk.X)
                
                # Kart içeriği
                card_content = Frame(habit_card, bg=self.colors['card_bg'], padx=20, pady=15)
                card_content.pack(fill=tk.BOTH, expand=True)
                
                # Alışkanlık adı ve icon
                header_frame = Frame(card_content, bg=self.colors['card_bg'])
                header_frame.pack(fill=tk.X, pady=(0, 10))
                
                Label(header_frame, text=f"🎯 {habit.name}", 
                      font=self.fonts['subtitle'], bg=self.colors['card_bg'], 
                      fg=self.colors['primary']).pack(side=tk.LEFT)
                
                # İstatistikler
                stats = Statistics(habit.user_id, habit.habit_id)
                all_stats = stats.get_all_stats(self.records)
                
                # İstatistik grid
                stats_grid = Frame(card_content, bg=self.colors['card_bg'])
                stats_grid.pack(fill=tk.X)
                
                # Sol kolon - başarı oranı
                left_col = Frame(stats_grid, bg=self.colors['card_bg'])
                left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
                
                Label(left_col, text="📈 Başarı Oranı", 
                      font=self.fonts['small'], bg=self.colors['card_bg'], 
                      fg=self.colors['text_dark']).pack(anchor=tk.W)
                Label(left_col, text=f"%{all_stats.get('completion_rate', 0)}", 
                      font=self.fonts['subtitle'], bg=self.colors['card_bg'], 
                      fg=self.colors['success']).pack(anchor=tk.W)
                
                # Orta kolon - streak
                middle_col = Frame(stats_grid, bg=self.colors['card_bg'])
                middle_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                Label(middle_col, text="🔥 Mevcut Streak", 
                      font=self.fonts['small'], bg=self.colors['card_bg'], 
                      fg=self.colors['text_dark']).pack(anchor=tk.W)
                Label(middle_col, text=f"{all_stats.get('current_streak', 0)} gün", 
                      font=self.fonts['subtitle'], bg=self.colors['card_bg'], 
                      fg=self.colors['accent']).pack(anchor=tk.W)
                
                # Sağ kolon - toplam
                right_col = Frame(stats_grid, bg=self.colors['card_bg'])
                right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                Label(right_col, text="✅ Toplam Tamamlama", 
                      font=self.fonts['small'], bg=self.colors['card_bg'], 
                      fg=self.colors['text_dark']).pack(anchor=tk.W)
                Label(right_col, text=f"{all_stats.get('total_completions', 0)}", 
                      font=self.fonts['subtitle'], bg=self.colors['card_bg'], 
                      fg=self.colors['primary']).pack(anchor=tk.W)
                
            # Canvas ve scrollbar'ı yerleştir
            canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
            scrollbar.pack(side="right", fill="y", pady=20, padx=(0, 20))
                
        except Exception as e:
            messagebox.showerror("Hata", f"İstatistikler güncellenemedi: {e}")
    
    def update_user_info(self):
        """
        Kullanıcı bilgisini günceller
        """
        if self.current_user:
            user_text = f"Kullanıcı: {self.current_user.username} | E-posta: {self.current_user.email}"
        else:
            user_text = "Kullanıcı giriş yapmamış"
        
        self.user_label.config(text=user_text)
    
    def save_data(self):
        """
        Verileri kaydeder
        """
        try:
            self.data_manager.save_data(self.users, self.habits, self.records)
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
    
    def show_user_selection(self):
        """
        Kullanıcı seçim dialogunu gösterir
        """
        if not self.users:
            messagebox.showinfo("Bilgi", "Henüz kullanıcı bulunmuyor!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Kullanıcı Seç")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Kullanıcı Seçin:").pack(pady=10)
        
        user_var = tk.StringVar()
        user_names = [user.username for user in self.users]
        
        user_combo = ttk.Combobox(dialog, textvariable=user_var, values=user_names, state="readonly")
        user_combo.pack(pady=10)
        if user_names:
            user_combo.current(0)
        
        def select_user():
            username = user_var.get()
            for user in self.users:
                if user.username == username:
                    self.current_user = user
                    self.update_user_info()
                    self.refresh_habits_list()
                    self.update_statistics_display()
                    dialog.destroy()
                    messagebox.showinfo("Başarı", f"{username} kullanıcısı seçildi!")
                    break
        
        ttk.Button(dialog, text="Seç", command=select_user).pack(pady=10)
    
    def show_profile_dialog(self):
        """
        Profil güncelleme dialogunu gösterir
        """
        if not self.current_user:
            messagebox.showwarning("Uyarı", "Önce kullanıcı girişi yapın!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Profil Güncelle")
        dialog.geometry("400x200")
        
        ttk.Label(dialog, text="Yeni Kullanıcı Adı:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        username_entry = ttk.Entry(dialog, width=30)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        username_entry.insert(0, self.current_user.username)
        
        ttk.Label(dialog, text="Yeni E-posta:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        email_entry = ttk.Entry(dialog, width=30)
        email_entry.grid(row=1, column=1, padx=10, pady=5)
        email_entry.insert(0, self.current_user.email)
        
        def update_profile():
            new_username = username_entry.get().strip()
            new_email = email_entry.get().strip()
            
            if self.current_user.update_profile(new_username, new_email):
                self.save_data()
                self.update_user_info()
                dialog.destroy()
                messagebox.showinfo("Başarı", "Profil başarıyla güncellendi!")
            else:
                messagebox.showerror("Hata", "Profil güncellenemedi!")
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Güncelle", command=update_profile).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="İptal", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_edit_habit_dialog(self):
        """
        Alışkanlık düzenleme dialogunu gösterir
        """
        selection = self.habits_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir alışkanlık seçin!")
            return
        
        item = self.habits_tree.item(selection[0])
        habit_id = item['values'][0]
        
        # Alışkanlığı bul
        habit = None
        for h in self.habits:
            if h.habit_id == habit_id:
                habit = h
                break
        
        if not habit:
            messagebox.showerror("Hata", "Alışkanlık bulunamadı!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Alışkanlık Düzenle")
        dialog.geometry("400x250")
        
        ttk.Label(dialog, text="Alışkanlık Adı:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        name_entry.insert(0, habit.name)
        
        ttk.Label(dialog, text="Açıklama:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        desc_entry = ttk.Entry(dialog, width=30)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        desc_entry.insert(0, habit.description)
        
        ttk.Label(dialog, text="Hedef (gün):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        freq_entry = ttk.Entry(dialog, width=30)
        freq_entry.grid(row=2, column=1, padx=10, pady=5)
        freq_entry.insert(0, str(habit.target_frequency))
        
        def update_habit():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()
            
            try:
                frequency = int(freq_entry.get())
            except ValueError:
                messagebox.showerror("Hata", "Hedef bir tam sayı olmalıdır!")
                return
            
            if habit.update_habit(name, description, frequency):
                self.save_data()
                self.refresh_habits_list()
                dialog.destroy()
                messagebox.showinfo("Başarı", "Alışkanlık başarıyla güncellendi!")
            else:
                messagebox.showerror("Hata", "Alışkanlık güncellenemedi!")
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Güncelle", command=update_habit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="İptal", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_about_dialog(self):
        """
        Hakkında dialogunu gösterir
        """
        about_text = """Günlük Alışkanlık Takip Uygulaması
        
Sürüm: 1.0
Geliştirici: 1. Sınıf Bilgisayar Programcılığı Öğrencisi

Bu uygulama kullanıcıların günlük alışkanlıklarını
takip etmelerini sağlayan basit bir araçtır.

Özellikler:
- Alışkanlık ekleme/düzenleme/silme
- Günlük tamamlama takibi
- İstatistikler ve streak takibi
- Veri yedekleme
"""
        messagebox.showinfo("Hakkında", about_text)
    
    def run(self):
        """
        Uygulamayı başlatır
        """
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Uygulama Hatası", f"Uygulama çalıştırılamadı: {e}")


if __name__ == "__main__":
    app = MainWindow()
    app.run()
