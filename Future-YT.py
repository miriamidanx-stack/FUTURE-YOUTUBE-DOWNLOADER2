import os
import certifi
import customtkinter as ctk
import yt_dlp
from tkinter import messagebox

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk(fg_color="red")
root.title("YouTube Downloader")
root.geometry("500x300")

title_label = ctk.CTkLabel(root, text="YouTube Downloader", font=("Arial", 24, "bold"))
title_label.pack(pady=20)

url_entry = ctk.CTkEntry(root, width=350, placeholder_text="Paste YouTube URL here")
url_entry.pack(pady=10)

def download_video():
    url = url_entry.get().strip()

    if not url:
        messagebox.showwarning("Missing URL", "Please enter a YouTube URL.")
        return

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download completed.")
    except Exception as e:
        messagebox.showerror("Download failed", str(e))

download_button = ctk.CTkButton(root, text="Download", command=download_video)
download_button.pack(pady=20)
























root.mainloop()