"""
Hatırlatıcı Uygulaması - Ana Dosya
Masaüstü hatırlatıcı programı
"""

import tkinter as tk
from gui.main_window import MainWindow
from core.database import Database
import sys

def main():
    """Ana uygulama fonksiyonu"""
    try:
        # Veritabanını başlat
        db = Database()
        db.initialize()
        
        # Ana pencereyi oluştur
        root = tk.Tk()
        app = MainWindow(root, db)
        
        # Uygulamayı başlat
        root.mainloop()
        
    except Exception as e: 
        print(f"Hata: {e}")
        sys.exit(1)

if __name__ == "__main__": 
    main()