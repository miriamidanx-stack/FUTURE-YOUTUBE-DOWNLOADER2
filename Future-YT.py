import tkinter as tk
from tkinter import ttk, messagebox
import threading
import yt_dlp
import os
import time


# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "DownloadStudio")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# ─────────────────────────────────────────────
# COLORS
# ─────────────────────────────────────────────

BG = "#080b14"
CARD = "#101522"
CARD_2 = "#151b2b"
TEXT = "#f5f7ff"
MUTED = "#8993aa"
ACCENT = "#7c5cff"
CYAN = "#00e5ff"
GREEN = "#35e39a"
RED = "#ff5577"


# ─────────────────────────────────────────────
# APP
# ─────────────────────────────────────────────

class DownloadStudio(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Download Studio")
        self.geometry("900x650")
        self.minsize(800, 600)
        self.configure(bg=BG)

        self.current_speed = "0 KB/s"
        self.current_eta = "--"
        self.current_percent = 0

        self.create_styles()
        self.build_ui()

    # ─────────────────────────────────────────

    def create_styles(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Modern.Horizontal.TProgressbar",
            troughcolor="#202638",
            background=ACCENT,
            bordercolor="#202638",
            lightcolor=ACCENT,
            darkcolor=ACCENT,
            thickness=14
        )

        style.configure(
            "Modern.TCombobox",
            fieldbackground=CARD_2,
            background=CARD_2,
            foreground=TEXT,
            arrowcolor=TEXT
        )

    # ─────────────────────────────────────────

    def build_ui(self):

        # Header
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=35, pady=(25, 10))

        title = tk.Label(
            header,
            text="DOWNLOAD",
            font=("Segoe UI", 28, "bold"),
            fg=TEXT,
            bg=BG
        )
        title.pack(side="left")

        studio = tk.Label(
            header,
            text="  STUDIO",
            font=("Segoe UI", 28, "bold"),
            fg=ACCENT,
            bg=BG
        )
        studio.pack(side="left")

        status = tk.Label(
            header,
            text="● READY",
            font=("Segoe UI", 10, "bold"),
            fg=GREEN,
            bg=BG
        )
        status.pack(side="right")

        # URL card
        url_card = tk.Frame(
            self,
            bg=CARD,
            highlightbackground="#20283c",
            highlightthickness=1
        )
        url_card.pack(fill="x", padx=35, pady=15)

        tk.Label(
            url_card,
            text="VIDEO URL",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(anchor="w", padx=20, pady=(15, 5))

        url_row = tk.Frame(url_card, bg=CARD)
        url_row.pack(fill="x", padx=20, pady=(0, 18))

        self.url_entry = tk.Entry(
            url_row,
            font=("Segoe UI", 13),
            bg=CARD_2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        )
        self.url_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12,
            padx=(0, 10)
        )

        paste_button = tk.Button(
            url_row,
            text="PASTE",
            command=self.paste_url,
            font=("Segoe UI", 9, "bold"),
            bg="#242c42",
            fg=TEXT,
            activebackground="#303a55",
            activeforeground=TEXT,
            relief="flat",
            padx=18
        )
        paste_button.pack(side="right")

        # Options
        options = tk.Frame(self, bg=BG)
        options.pack(fill="x", padx=35, pady=5)

        self.create_option(
            options,
            "FORMAT",
            ["MP4", "MP3", "WEBM"],
            0
        )

        self.create_option(
            options,
            "QUALITY",
            ["Best", "1080p", "720p", "480p", "360p"],
            1
        )

        # Download button
        self.download_button = tk.Button(
            options,
            text="⚡ START DOWNLOAD",
            command=self.start_download,
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT,
            fg="white",
            activebackground="#6847e8",
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2"
        )
        self.download_button.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=(20, 0),
            sticky="e"
        )

        options.columnconfigure(0, weight=1)
        options.columnconfigure(1, weight=1)
        options.columnconfigure(2, weight=0)

        # Progress card
        progress_card = tk.Frame(
            self,
            bg=CARD,
            highlightbackground="#20283c",
            highlightthickness=1
        )
        progress_card.pack(fill="x", padx=35, pady=25)

        tk.Label(
            progress_card,
            text="DOWNLOAD PROGRESS",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(anchor="w", padx=20, pady=(18, 10))

        self.progress = ttk.Progressbar(
            progress_card,
            style="Modern.Horizontal.TProgressbar",
            mode="determinate",
            maximum=100
        )
        self.progress.pack(fill="x", padx=20)

        stats = tk.Frame(progress_card, bg=CARD)
        stats.pack(fill="x", padx=20, pady=15)

        self.percent_label = tk.Label(
            stats,
            text="0%",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT,
            bg=CARD
        )
        self.percent_label.pack(side="left")

        self.speed_label = tk.Label(
            stats,
            text="0 KB/s",
            font=("Segoe UI", 10),
            fg=CYAN,
            bg=CARD
        )
        self.speed_label.pack(side="left", padx=20)

        self.eta_label = tk.Label(
            stats,
            text="ETA --",
            font=("Segoe UI", 10),
            fg=MUTED,
            bg=CARD
        )
        self.eta_label.pack(side="right")

        # History
        history_header = tk.Frame(self, bg=BG)
        history_header.pack(fill="x", padx=35)

        tk.Label(
            history_header,
            text="DOWNLOAD HISTORY",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=BG
        ).pack(side="left")

        self.history = tk.Listbox(
            self,
            bg=CARD,
            fg=TEXT,
            selectbackground=ACCENT,
            selectforeground="white",
            relief="flat",
            font=("Segoe UI", 10),
            height=8
        )
        self.history.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(8, 25)
        )

    # ─────────────────────────────────────────

    def create_option(self, parent, label, values, column):

        frame = tk.Frame(parent, bg=BG)
        frame.grid(
            row=0,
            column=column,
            padx=(0, 10),
            sticky="ew"
        )

        tk.Label(
            frame,
            text=label,
            font=("Segoe UI", 8, "bold"),
            fg=MUTED,
            bg=BG
        ).pack(anchor="w")

        combo = ttk.Combobox(
            frame,
            values=values,
            state="readonly",
            style="Modern.TCombobox",
            font=("Segoe UI", 10)
        )

        combo.current(0)
        combo.pack(fill="x", pady=(5, 0), ipady=5)

        if label == "FORMAT":
            self.format_combo = combo

        else:
            self.quality_combo = combo

    # ─────────────────────────────────────────

    def paste_url(self):

        try:
            text = self.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, text)
        except tk.TclError:
            pass

    # ─────────────────────────────────────────

    def start_download(self):

        url = self.url_entry.get().strip()

        if not url:
            messagebox.showwarning(
                "Missing URL",
                "Paste a video URL first."
            )
            return

        self.download_button.config(
            state="disabled",
            text="DOWNLOADING..."
        )

        self.progress["value"] = 0
        self.percent_label.config(text="0%")

        thread = threading.Thread(
            target=self.download_video,
            args=(url,),
            daemon=True
        )

        thread.start()

    # ─────────────────────────────────────────

    def download_video(self, url):

        selected_format = self.format_combo.get()
        quality = self.quality_combo.get()

        if selected_format == "MP3":

            postprocessors = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }]

            format_selector = "bestaudio/best"

        else:

            postprocessors = []

            if quality == "Best":
                format_selector = "bestvideo+bestaudio/best"

            elif quality == "1080p":
                format_selector = (
                    "bestvideo[height<=1080]+bestaudio/"
                    "best[height<=1080]"
                )

            elif quality == "720p":
                format_selector = (
                    "bestvideo[height<=720]+bestaudio/"
                    "best[height<=720]"
                )

            elif quality == "480p":
                format_selector = (
                    "bestvideo[height<=480]+bestaudio/"
                    "best[height<=480]"
                )

            else:
                format_selector = (
                    "bestvideo[height<=360]+bestaudio/"
                    "best[height<=360]"
                )

        options = {
            "format": format_selector,
            "outtmpl": os.path.join(
                DOWNLOAD_DIR,
                "%(title)s.%(ext)s"
            ),
            "progress_hooks": [self.progress_hook],
            "postprocessors": postprocessors,
            "merge_output_format": "mp4",
            "continuedl": True,
            "retries": 10,
            "fragment_retries": 10,
            "file_access_retries": 5,
            "http_chunk_size": 10 * 1024 * 1024,
            "socket_timeout": 30,
            "quiet": True,
            "noplaylist": True
        }

        try:

            with yt_dlp.YoutubeDL(options) as ydl:

                info = ydl.extract_info(url, download=True)

                title = info.get(
                    "title",
                    "Unknown video"
                )

                self.after(
                    0,
                    lambda: self.history.insert(
                        0,
                        "⬇ " + title[:85]
                    )
                )

            self.after(
                0,
                self.download_finished
            )

        except Exception as error:

            self.after(
                0,
                lambda: self.download_error(str(error))
            )

    # ─────────────────────────────────────────

    def progress_hook(self, data):

        if data["status"] == "downloading":

            downloaded = data.get("downloaded_bytes", 0)
            total = data.get("total_bytes") or data.get(
                "total_bytes_estimate",
                0
            )

            if total:

                percent = downloaded / total * 100

                self.after(
                    0,
                    lambda p=percent:
                    self.update_progress(p)
                )

            speed = data.get("speed")

            if speed:

                speed_text = self.format_bytes(speed) + "/s"

            else:
                speed_text = "0 KB/s"

            eta = data.get("eta")

            if eta is not None:

                eta_text = self.format_time(eta)

            else:
                eta_text = "--"

            self.after(
                0,
                lambda s=speed_text, e=eta_text:
                self.update_stats(s, e)
            )

    # ─────────────────────────────────────────

    def update_progress(self, value):

        self.progress["value"] = value
        self.percent_label.config(
            text=f"{value:.1f}%"
        )

    # ─────────────────────────────────────────

    def update_stats(self, speed, eta):

        self.speed_label.config(text=speed)
        self.eta_label.config(
            text=f"ETA {eta}"
        )

    # ─────────────────────────────────────────

    def download_finished(self):

        self.progress["value"] = 100
        self.percent_label.config(text="100%")
        self.speed_label.config(text="DONE")
        self.eta_label.config(text="Complete")

        self.download_button.config(
            state="normal",
            text="⚡ START DOWNLOAD"
        )

        messagebox.showinfo(
            "Download Complete",
            f"Your file was saved to:\n\n{DOWNLOAD_DIR}"
        )

    # ─────────────────────────────────────────

    def download_error(self, error):

        self.download_button.config(
            state="normal",
            text="⚡ START DOWNLOAD"
        )

        messagebox.showerror(
            "Download Error",
            error
        )

    # ─────────────────────────────────────────

    @staticmethod
    def format_bytes(size):

        units = [
            "B",
            "KB",
            "MB",
            "GB",
            "TB"
        ]

        for unit in units:

            if size < 1024:
                return f"{size:.1f} {unit}"

            size /= 1024

        return f"{size:.1f} PB"

    # ─────────────────────────────────────────

    @staticmethod
    def format_time(seconds):

        seconds = int(seconds)

        minutes, seconds = divmod(
            seconds,
            60
        )

        hours, minutes = divmod(
            minutes,
            60
        )

        if hours:
            return f"{hours}h {minutes}m"

        if minutes:
            return f"{minutes}m {seconds}s"

        return f"{seconds}s"


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = DownloadStudio()
    app.mainloop()
