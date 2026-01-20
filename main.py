"""
Hatırlatıcı Uygulaması - Ana Dosya
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Modülleri import et
from gui.main_window import MainWindow
from core.database import Database
from utils.config import Config

def main():
    """Ana uygulama fonksiyonu"""
    
    # Yapılandırmayı yükle
    config = Config()
    
    # Veritabanını başlat
    db = Database(config.get('database_path', 'reminders.db'))
    db.initialize()
    
    # Ana pencereyi oluştur
    root = tk.Tk()
    
    # Ana uygulama
    app = MainWindow(root, db)
    
    # Uygulamayı başlat
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nUygulama kapatılıyor...")
    finally:
        db.close()

if __name__ == '__main__':
    main()