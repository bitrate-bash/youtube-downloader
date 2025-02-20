import customtkinter as ctk
import os
from youtube_downloader import download_video
import threading
from typing import List
import json

class YouTubeDownloaderGUI:
    def __init__(self):
        # Configure appearance
        ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # Create main window
        self.window = ctk.CTk()
        self.window.title("YouTube Video Downloader")
        self.window.geometry("800x600")
        self.window.minsize(800, 600)

        # Configure grid layout
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        # Create sidebar frame
        self.sidebar = ctk.CTkFrame(self.window, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Add logo/title to sidebar
        self.logo_label = ctk.CTkLabel(self.sidebar, text="YouTube\nDownloader", 
                                     font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Add buttons to sidebar
        self.add_url_button = ctk.CTkButton(self.sidebar, text="Add URLs", 
                                          command=self.add_url)
        self.add_url_button.grid(row=1, column=0, padx=20, pady=10)

        self.clear_button = ctk.CTkButton(self.sidebar, text="Clear All", 
                                        command=self.clear_urls)
        self.clear_button.grid(row=2, column=0, padx=20, pady=10)

        # Add output directory selector
        self.output_dir_button = ctk.CTkButton(self.sidebar, text="Select Output Directory", 
                                             command=self.select_output_dir)
        self.output_dir_button.grid(row=3, column=0, padx=20, pady=10)

        # Add appearance mode selector
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"],
                                                    command=self.change_appearance_mode)
        self.appearance_mode_menu.grid(row=5, column=0, padx=20, pady=(10, 10))

        # Add download button
        self.download_button = ctk.CTkButton(self.sidebar, text="Start Download",
                                           command=self.start_download,
                                           font=ctk.CTkFont(size=15, weight="bold"))
        self.download_button.grid(row=6, column=0, padx=20, pady=(10, 20))

        # Create main area title
        self.title_label = ctk.CTkLabel(self.main_frame, text="YouTube URLs", 
                                      font=ctk.CTkFont(size=15, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=10, pady=(0, 10))

        # Create URL list
        self.url_textbox = ctk.CTkTextbox(self.main_frame, width=400)
        self.url_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Create status area
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.status_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(self.status_frame, text="Ready", 
                                       font=ctk.CTkFont(size=12))
        self.status_label.grid(row=0, column=0, padx=10, pady=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.status_frame)
        self.progress_bar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)

        # Initialize variables
        self.output_directory = os.path.join(os.path.dirname(__file__), 'output')
        self.urls: List[str] = []
        self.is_downloading = False

        # Load saved settings
        self.load_settings()

    def load_settings(self):
        """Load saved settings from file."""
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    self.output_directory = settings.get('output_directory', self.output_directory)
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save current settings to file."""
        try:
            settings = {
                'output_directory': self.output_directory
            }
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def add_url(self):
        """Add URLs from clipboard."""
        clipboard = self.window.clipboard_get()
        if clipboard:
            current_text = self.url_textbox.get("1.0", "end-1c")
            if current_text:
                self.url_textbox.insert("end", "\n")
            self.url_textbox.insert("end", clipboard)
        self.update_status("URL added from clipboard")

    def clear_urls(self):
        """Clear all URLs from the textbox."""
        self.url_textbox.delete("1.0", "end")
        self.update_status("URLs cleared")

    def select_output_dir(self):
        """Open directory selector dialog."""
        directory = ctk.filedialog.askdirectory(initialdir=self.output_directory)
        if directory:
            self.output_directory = directory
            self.save_settings()
            self.update_status(f"Output directory set to: {directory}")

    def change_appearance_mode(self, new_appearance_mode: str):
        """Change the app's appearance mode."""
        ctk.set_appearance_mode(new_appearance_mode.lower())

    def update_status(self, message: str):
        """Update the status label."""
        self.status_label.configure(text=message)

    def update_progress(self, value: float):
        """Update the progress bar."""
        self.progress_bar.set(value)

    def download_videos(self):
        """Download all videos in the list."""
        try:
            # Get URLs from textbox
            urls = [url.strip() for url in self.url_textbox.get("1.0", "end-1c").split('\n') if url.strip()]
            total_urls = len(urls)
            
            if not total_urls:
                self.update_status("No URLs to download")
                return

            # Create output directory if it doesn't exist
            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory)

            # Download each video
            for i, url in enumerate(urls, 1):
                if not self.is_downloading:
                    break
                
                self.update_status(f"Downloading video {i}/{total_urls}")
                self.update_progress(i / total_urls)
                
                success = download_video(url, self.output_directory)
                if not success:
                    self.update_status(f"Error downloading: {url}")

            if self.is_downloading:
                self.update_status("All downloads completed!")
            else:
                self.update_status("Downloads cancelled")
                
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
        finally:
            self.is_downloading = False
            self.download_button.configure(text="Start Download")
            self.update_progress(0)

    def start_download(self):
        """Start or stop the download process."""
        if not self.is_downloading:
            self.is_downloading = True
            self.download_button.configure(text="Stop Download")
            # Start download in a separate thread
            threading.Thread(target=self.download_videos, daemon=True).start()
        else:
            self.is_downloading = False
            self.download_button.configure(text="Start Download")

    def run(self):
        """Start the GUI application."""
        self.window.mainloop()

if __name__ == "__main__":
    app = YouTubeDownloaderGUI()
    app.run() 