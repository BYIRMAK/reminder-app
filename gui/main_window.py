"""
Ana Pencere - Hatırlatıcı Listesi ve Ana İşlemler
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from gui.add_reminder import AddReminderDialog
from gui.edit_reminder import EditReminderDialog
from core.scheduler import ReminderScheduler

class MainWindow:
    """Ana pencere sınıfı"""
    
    def __init__(self, root, database):
        """Ana pencereyi başlat"""
        self.root = root
        self.db = database
        self.scheduler = ReminderScheduler(database)
        
        # Pencere ayarları
        self.root.title("Hatırlatıcı Uygulaması")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # UI oluştur
        self.create_menu()
        self.create_toolbar()
        self.create_treeview()
        self.create_statusbar()
        
        # Hatırlatıcıları yükle
        self.load_reminders()
        
        # Scheduler'ı başlat
        self.scheduler.start()
        
        # Pencere kapanırken scheduler'ı durdur
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_menu(self):
        """Menü çubuğunu oluştur"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Dosya menüsü
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        file_menu.add_command(label="Yeni Hatırlatıcı", command=self.add_reminder)
        file_menu.add_separator()
        file_menu.add_command(label="Dışa Aktar", command=self.export_data)
        file_menu.add_command(label="İçe Aktar", command=self.import_data)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.on_closing)
        
        # Düzenle menüsü
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Düzenle", menu=edit_menu)
        edit_menu.add_command(label="Düzenle", command=self.edit_reminder)
        edit_menu.add_command(label="Sil", command=self.delete_reminder)
        
        # Görünüm menüsü
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Görünüm", menu=view_menu)
        view_menu.add_command(label="Yenile", command=self.load_reminders)
        
        # Yardım menüsü
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        help_menu.add_command(label="Hakkında", command=self.show_about)
    
    def create_toolbar(self):
        """Araç çubuğunu oluştur"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Butonlar
        ttk.Button(toolbar, text="➕ Yeni", command=self.add_reminder).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="✏️ Düzenle", command=self.edit_reminder).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🗑️ Sil", command=self.delete_reminder).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔄 Yenile", command=self.load_reminders).pack(side=tk.LEFT, padx=2)
        
        # Ayırıcı
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Kategori filtresi
        ttk.Label(toolbar, text="Kategori:").pack(side=tk.LEFT, padx=5)
        self.category_var = tk.StringVar(value="Tümü")
        categories = ["Tümü"] + [cat[1] for cat in self.db.get_categories()]
        self.category_combo = ttk.Combobox(toolbar, textvariable=self.category_var, 
                                          values=categories, state="readonly", width=15)
        self.category_combo.pack(side=tk.LEFT, padx=5)
        self.category_combo.bind("<<ComboboxSelected>>", lambda e: self.load_reminders())
        
        # Arama
        ttk.Label(toolbar, text="Ara:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.load_reminders())
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
    
    def create_treeview(self):
        """Hatırlatıcı listesini oluştur"""
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("Başlık", "Tarih/Saat", "Kategori", "Öncelik", "Tekrar", "Durum")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings",
                                yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("#0", text="ID")
        self.tree.column("#0", width=50)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Başlık":
                self.tree.column(col, width=200)
            elif col == "Tarih/Saat":
                self.tree.column(col, width=150)
            else:
                self.tree.column(col, width=100)
        
        self.tree.bind("<Double-1>", lambda e: self.edit_reminder())
    
    def create_statusbar(self):
        """Durum çubuğunu oluştur"""
        self.statusbar = ttk.Label(self.root, text="Hazır", relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_reminders(self):
        """Hatırlatıcıları yükle"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        category = self.category_var.get()
        search = self.search_var.get()
        
        reminders = self.db.get_reminders()
        
        if category != "Tümü":
            reminders = [r for r in reminders if r[4] == category]
        
        if search:
            search_lower = search.lower()
            reminders = [r for r in reminders if 
                        search_lower in r[1].lower() or
                        search_lower in r[2].lower()]
        
        count = 0
        for reminder in reminders:
            rid, title, desc, dt, category, tags, repeat, priority, active, created = reminder
            
            try:
                dt_obj = datetime.fromisoformat(dt)
                date_str = dt_obj.strftime("%d.%m.%Y %H:%M")
            except:
                date_str = dt
            
            repeat_text = repeat if repeat else "Tek seferlik"
            status = "Aktif" if active else "Pasif"
            tag = f"priority_{priority}"
            
            self.tree.insert("", tk.END, text=str(rid),
                           values=(title, date_str, category, priority, repeat_text, status),
                           tags=(tag,))
            count += 1
        
        self.tree.tag_configure("priority_Yüksek", background="#ffcccc")
        self.tree.tag_configure("priority_Orta", background="#ffffcc")
        self.tree.tag_configure("priority_Düşük", background="#ccffcc")
        
        self.statusbar.config(text=f"Toplam {count} hatırlatıcı")
    
    def add_reminder(self):
        """Yeni hatırlatıcı ekle"""
        dialog = AddReminderDialog(self.root, self.db)
        self.root.wait_window(dialog.dialog)
        self.load_reminders()
    
    def edit_reminder(self):
        """Seçili hatırlatıcıyı düzenle"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen düzenlemek için bir hatırlatıcı seçin!")
            return
        
        item = self.tree.item(selection[0])
        reminder_id = int(item["text"])
        
        dialog = EditReminderDialog(self.root, self.db, reminder_id)
        self.root.wait_window(dialog.dialog)
        self.load_reminders()
    
    def delete_reminder(self):
        """Seçili hatırlatıcıyı sil"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir hatırlatıcı seçin!")
            return
        
        if not messagebox.askyesno("Onay", "Seçili hatırlatıcıyı silmek istediğinizden emin misiniz?"):
            return
        
        item = self.tree.item(selection[0])
        reminder_id = int(item["text"])
        
        self.db.delete_reminder(reminder_id)
        self.load_reminders()
        messagebox.showinfo("Başarılı", "Hatırlatıcı silindi!")
    
    def export_data(self):
        """Verileri dışa aktar"""
        from tkinter import filedialog
        import json
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            data = {
                "reminders": self.db.get_reminders(),
                "categories": self.db.get_categories()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Başarılı", "Veriler dışa aktarıldı!")
    
    def import_data(self):
        """Verileri içe aktar"""
        from tkinter import filedialog
        import json
        
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                messagebox.showinfo("Başarılı", "Veriler içe aktarıldı!")
                self.load_reminders()
            except Exception as e:
                messagebox.showerror("Hata", f"İçe aktarma başarısız: {e}")
    
    def show_about(self):
        """Hakkında bilgisi göster"""
        messagebox.showinfo("Hakkında", 
                          "Hatırlatıcı Uygulaması v1.0\n\n"
                          "Python + Tkinter ile geliştirilmiştir.\n"
                          "© 2026")
    
    def on_closing(self):
        """Pencere kapatılırken"""
        if messagebox.askokcancel("Çıkış", "Uygulamadan çıkmak istediğinizden emin misiniz?"):
            self.scheduler.stop()
            self.root.destroy()