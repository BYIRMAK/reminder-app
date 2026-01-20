"""
Hatırlatıcı Ekleme Penceresi
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta

class AddReminderDialog:
    """Hatırlatıcı ekleme dialog penceresi"""
    
    def __init__(self, parent, database):
        """Dialog penceresini başlat"""
        self.db = database
        
        # Dialog penceresi
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Yeni Hatırlatıcı")
        self.dialog.geometry("600x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Widget'ları oluştur"""
        # Ana frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        ttk.Label(main_frame, text="Başlık:", font=("", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.title_var, width=50).grid(row=0, column=1, pady=5, sticky=tk.W+tk.E)
        
        # Açıklama
        ttk.Label(main_frame, text="Açıklama:", font=("", 10, "bold")).grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.desc_text = tk.Text(main_frame, width=50, height=5)
        self.desc_text.grid(row=1, column=1, pady=5, sticky=tk.W+tk.E)
        
        # Tarih
        ttk.Label(main_frame, text="Tarih:", font=("", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.calendar = Calendar(main_frame, selectmode='day', date_pattern='dd.mm.yyyy')
        self.calendar.grid(row=2, column=1, pady=5)
        
        # Saat
        time_frame = ttk.Frame(main_frame)
        time_frame.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Saat:", font=("", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.hour_var = tk.StringVar(value="12")
        self.minute_var = tk.StringVar(value="00")
        
        ttk.Spinbox(time_frame, from_=0, to=23, textvariable=self.hour_var, width=5, format="%02.0f").pack(side=tk.LEFT)
        ttk.Label(time_frame, text=":").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(time_frame, from_=0, to=59, textvariable=self.minute_var, width=5, format="%02.0f").pack(side=tk.LEFT)
        
        # Kategori
        ttk.Label(main_frame, text="Kategori:", font=("", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        categories = [cat[1] for cat in self.db.get_categories()]
        category_combo = ttk.Combobox(main_frame, textvariable=self.category_var, 
                                     values=categories, state="readonly", width=20)
        category_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        if categories:
            category_combo.current(0)
        
        # Etiketler
        ttk.Label(main_frame, text="Etiketler:", font=("", 10, "bold")).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.tags_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.tags_var, width=50).grid(row=5, column=1, pady=5, sticky=tk.W+tk.E)
        ttk.Label(main_frame, text="(Virgülle ayırın)", font=("", 8)).grid(row=6, column=1, sticky=tk.W)
        
        # Öncelik
        ttk.Label(main_frame, text="Öncelik:", font=("", 10, "bold")).grid(row=7, column=0, sticky=tk.W, pady=5)
        priority_frame = ttk.Frame(main_frame)
        priority_frame.grid(row=7, column=1, sticky=tk.W, pady=5)
        
        self.priority_var = tk.StringVar(value="Orta")
        ttk.Radiobutton(priority_frame, text="Düşük", variable=self.priority_var, value="Düşük").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(priority_frame, text="Orta", variable=self.priority_var, value="Orta").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(priority_frame, text="Yüksek", variable=self.priority_var, value="Yüksek").pack(side=tk.LEFT, padx=5)
        
        # Tekrar
        ttk.Label(main_frame, text="Tekrar:", font=("", 10, "bold")).grid(row=8, column=0, sticky=tk.W, pady=5)
        self.repeat_var = tk.StringVar(value="Yok")
        repeat_options = ["Yok", "Günlük", "Haftalık", "Aylık", "Yıllık"]
        ttk.Combobox(main_frame, textvariable=self.repeat_var, values=repeat_options, 
                    state="readonly", width=20).grid(row=8, column=1, sticky=tk.W, pady=5)
        
        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="💾 Kaydet", command=self.save_reminder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ İptal", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Grid weight
        main_frame.columnconfigure(1, weight=1)
    
    def save_reminder(self):
        """Hatırlatıcıyı kaydet"""
        # Verileri al
        title = self.title_var.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        category = self.category_var.get()
        tags = self.tags_var.get().strip()
        priority = self.priority_var.get()
        repeat = self.repeat_var.get() if self.repeat_var.get() != "Yok" else None
        
        # Tarih ve saat
        date_str = self.calendar.get_date()
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())
        
        try:
            # Tarihi parse et
            dt = datetime.strptime(date_str, "%d.%m.%Y")
            dt = dt.replace(hour=hour, minute=minute)
            
            # Geçmiş tarih kontrolü
            if dt < datetime.now():
                if not messagebox.askyesno("Uyarı", "Seçilen tarih geçmişte! Devam etmek istiyor musunuz?"):
                    return
            
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
        
        # Veritabanına kaydet
        try:
            self.db.add_reminder(
                title=title,
                description=description,
                datetime_str=dt.isoformat(),
                category=category,
                tags=tags,
                repeat_type=repeat,
                priority=priority
            )
            
            messagebox.showinfo("Başarılı", "Hatırlatıcı eklendi!")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Hatırlatıcı eklenirken hata oluştu: {e}")
