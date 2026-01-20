"""
Hatırlatıcı Düzenleme Penceresi
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime

class EditReminderDialog:
    """Hatırlatıcı düzenleme dialog penceresi"""
    
    def __init__(self, parent, database, reminder_id):
        """Dialog penceresini başlat"""
        self.db = database
        self.reminder_id = reminder_id
        
        # Dialog penceresi
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Hatırlatıcıyı Düzenle")
        self.dialog.geometry("600x750")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Mevcut verileri yükle
        self.load_reminder_data()
        self.create_widgets()
    
    def load_reminder_data(self):
        """Mevcut hatırlatıcı verilerini yükle"""
        reminder = self.db.get_reminder(self.reminder_id)
        if reminder:
            self.current_data = {
                'title': reminder[1],
                'description': reminder[2],
                'datetime': reminder[3],
                'category': reminder[4],
                'tags': reminder[5],
                'repeat': reminder[6],
                'priority': reminder[7],
                'active': reminder[8]
            }
        else:
            messagebox.showerror("Hata", "Hatırlatıcı bulunamadı!")
            self.dialog.destroy()
    
    def create_widgets(self):
        """Widget'ları oluştur"""
        # Ana frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        ttk.Label(main_frame, text="Başlık:", font=("", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_var = tk.StringVar(value=self.current_data['title'])
        ttk.Entry(main_frame, textvariable=self.title_var, width=50).grid(row=0, column=1, pady=5, sticky=tk.W+tk.E)
        
        # Açıklama
        ttk.Label(main_frame, text="Açıklama:", font=("", 10, "bold")).grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.desc_text = tk.Text(main_frame, width=50, height=5)
        self.desc_text.grid(row=1, column=1, pady=5, sticky=tk.W+tk.E)
        self.desc_text.insert("1.0", self.current_data['description'])
        
        # Tarih
        ttk.Label(main_frame, text="Tarih:", font=("", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Mevcut tarihi parse et
        try:
            dt = datetime.fromisoformat(self.current_data['datetime'])
            init_date = dt
        except:
            init_date = datetime.now()
        
        self.calendar = Calendar(main_frame, selectmode='day', date_pattern='dd.mm.yyyy',
                                year=init_date.year, month=init_date.month, day=init_date.day)
        self.calendar.grid(row=2, column=1, pady=5)
        
        # Saat
        time_frame = ttk.Frame(main_frame)
        time_frame.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Saat:", font=("", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.hour_var = tk.StringVar(value=f"{init_date.hour:02d}")
        self.minute_var = tk.StringVar(value=f"{init_date.minute:02d}")
        
        ttk.Spinbox(time_frame, from_=0, to=23, textvariable=self.hour_var, width=5, format="%02.0f").pack(side=tk.LEFT)
        ttk.Label(time_frame, text=":").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(time_frame, from_=0, to=59, textvariable=self.minute_var, width=5, format="%02.0f").pack(side=tk.LEFT)
        
        # Kategori
        ttk.Label(main_frame, text="Kategori:", font=("", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar(value=self.current_data['category'])
        categories = [cat[1] for cat in self.db.get_categories()]
        ttk.Combobox(main_frame, textvariable=self.category_var, 
                    values=categories, state="readonly", width=20).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Etiketler
        ttk.Label(main_frame, text="Etiketler:", font=("", 10, "bold")).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.tags_var = tk.StringVar(value=self.current_data['tags'] or "")
        ttk.Entry(main_frame, textvariable=self.tags_var, width=50).grid(row=5, column=1, pady=5, sticky=tk.W+tk.E)
        ttk.Label(main_frame, text="(Virgülle ayırın)", font=("", 8)).grid(row=6, column=1, sticky=tk.W)
        
        # Öncelik
        ttk.Label(main_frame, text="Öncelik:", font=("", 10, "bold")).grid(row=7, column=0, sticky=tk.W, pady=5)
        priority_frame = ttk.Frame(main_frame)
        priority_frame.grid(row=7, column=1, sticky=tk.W, pady=5)
        
        self.priority_var = tk.StringVar(value=self.current_data['priority'])
        ttk.Radiobutton(priority_frame, text="Düşük", variable=self.priority_var, value="Düşük").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(priority_frame, text="Orta", variable=self.priority_var, value="Orta").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(priority_frame, text="Yüksek", variable=self.priority_var, value="Yüksek").pack(side=tk.LEFT, padx=5)
        
        # Tekrar
        ttk.Label(main_frame, text="Tekrar:", font=("", 10, "bold")).grid(row=8, column=0, sticky=tk.W, pady=5)
        repeat_val = self.current_data['repeat'] if self.current_data['repeat'] else "Yok"
        self.repeat_var = tk.StringVar(value=repeat_val)
        repeat_options = ["Yok", "Günlük", "Haftalık", "Aylık", "Yıllık"]
        ttk.Combobox(main_frame, textvariable=self.repeat_var, values=repeat_options, 
                    state="readonly", width=20).grid(row=8, column=1, sticky=tk.W, pady=5)
        
        # Aktif/Pasif
        ttk.Label(main_frame, text="Durum:", font=("", 10, "bold")).grid(row=9, column=0, sticky=tk.W, pady=5)
        self.active_var = tk.BooleanVar(value=self.current_data['active'])
        ttk.Checkbutton(main_frame, text="Aktif", variable=self.active_var).grid(row=9, column=1, sticky=tk.W, pady=5)
        
        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="💾 Güncelle", command=self.update_reminder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ İptal", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Grid weight
        main_frame.columnconfigure(1, weight=1)
    
    def update_reminder(self):
        """Hatırlatıcıyı güncelle"""
        # Verileri al
        title = self.title_var.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        category = self.category_var.get()
        tags = self.tags_var.get().strip()
        priority = self.priority_var.get()
        repeat = self.repeat_var.get() if self.repeat_var.get() != "Yok" else None
        active = self.active_var.get()
        
        # Tarih ve saat
        date_str = self.calendar.get_date()
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())
        
        try:
            # Tarihi parse et
            dt = datetime.strptime(date_str, "%d.%m.%Y")
            dt = dt.replace(hour=hour, minute=minute)
        except Exception as e:
            messagebox.showerror("Hata", f"Tarih formatı hatalı: {e}")
            return
        
        # Validasyon
        if not title:
            messagebox.showwarning("Uyarı", "Lütfen bir başlık girin!")
            return
        
        if not category:
            messagebox.showwarning("Uyarı", "Lütfen bir kategori seçin!")
            return
        
        # Veritabanında güncelle
        try:
            self.db.update_reminder(
                reminder_id=self.reminder_id,
                title=title,
                description=description,
                datetime_str=dt.isoformat(),
                category=category,
                tags=tags,
                repeat_type=repeat,
                priority=priority,
                active=active
            )
            
            messagebox.showinfo("Başarılı", "Hatırlatıcı güncellendi!")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Hatırlatıcı güncellenirken hata oluştu: {e}")
