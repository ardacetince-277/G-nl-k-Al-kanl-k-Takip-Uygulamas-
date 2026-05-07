import customtkinter as ctk

class AddHabitWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Pencere Ayarları (Tam istediğin ölçüler)
        self.title("Yeni Alışkanlık")
        self.geometry("340x380")  # Genişlik x Yükseklik (400'den küçük)
        self.resizable(False, False)
        self.attributes("-topmost", True)  # Ana pencerenin arkasında kalmasın
        
        # İç Boşluklar
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)

        # Başlık
        self.label_title = ctk.CTkLabel(self, text="Yeni Alışkanlık Ekle", font=ctk.CTkFont(size=18, weight="bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=(15, 10))

        # Giriş Alanları (Kompakt 13px font)
        self.entry_name = ctk.CTkEntry(self, placeholder_text="Alışkanlık adı...", width=220, font=("Segoe UI", 13))
        self.entry_name.grid(row=1, column=0, padx=20, pady=5)

        # Zorluk Seçimi
        self.label_diff = ctk.CTkLabel(self, text="Zorluk Seviyesi:", font=("Segoe UI", 12))
        self.label_diff.grid(row=2, column=0, padx=20, pady=(5, 0))
        
        self.combo_difficulty = ctk.CTkComboBox(self, values=["Düşük (5 XP)", "Orta (15 XP)", "Yüksek (30 XP)"], 
                                               width=220, font=("Segoe UI", 13))
        self.combo_difficulty.grid(row=3, column=0, padx=20, pady=5)

        # Hedef Süre
        self.entry_goal = ctk.CTkEntry(self, placeholder_text="Günlük hedef (dakika)...", width=220, font=("Segoe UI", 13))
        self.entry_goal.grid(row=4, column=0, padx=20, pady=5)

        # Çile: Ömür 180x35 Buton
        self.btn_save = ctk.CTkButton(self, text="Alışkanlığı Kaydet", 
                                      width=180, height=35, corner_radius=8,
                                      font=ctk.CTkFont(size=13, weight="bold"),
                                      command=self.save_habit)
        self.btn_save.grid(row=5, column=0, padx=20, pady=20)

    def save_habit(self):
        # Burası ekleme mantığının çalışacağı yer
        name = self.entry_name.get()
        if name:
            print(f"Yeni alışkanlık eklendi: {name}")
            self.destroy()  # Kaydedince pencereyi kapat
        else:
            self.entry_name.configure(border_color="red")  # Boşsa uyarı
