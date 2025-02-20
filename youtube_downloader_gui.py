import customtkinter as ctk
import os
from youtube_downloader import download_video
import threading
from typing import List
import json

class YouTubeDownloaderGUI:
    def __init__(self):
        # Configure appearance
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        # Create main window first
        self.window = ctk.CTk()
        self.window.title("YouTube Video Downloader")
        self.window.geometry("1000x700")
        self.window.minsize(900, 600)

        # Font configurations - after window creation
        self.FONT_FAMILY = "IBM Plex Mono"
        self.TITLE_FONT = ctk.CTkFont(family=self.FONT_FAMILY, size=24, weight="bold")
        self.HEADING_FONT = ctk.CTkFont(family=self.FONT_FAMILY, size=16, weight="bold")
        self.BUTTON_FONT = ctk.CTkFont(family=self.FONT_FAMILY, size=13)
        self.TEXT_FONT = ctk.CTkFont(family=self.FONT_FAMILY, size=12)
        self.STATUS_FONT = ctk.CTkFont(family=self.FONT_FAMILY, size=11)

        # Configure grid layout
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        # Create sidebar frame with gradient effect
        self.sidebar = ctk.CTkFrame(self.window, width=250, corner_radius=15)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.sidebar.grid_rowconfigure(7, weight=1)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window, corner_radius=15)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Add logo/title to sidebar with enhanced styling
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="YouTube\nDownloader", 
            font=self.TITLE_FONT,
            pady=20
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        # Separator after title
        self.separator1 = ctk.CTkFrame(self.sidebar, height=2)
        self.separator1.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        # Add buttons to sidebar with consistent styling
        self.add_url_button = ctk.CTkButton(
            self.sidebar,
            text="Paste URLs",
            command=self.add_url,
            font=self.BUTTON_FONT,
            height=40,
            corner_radius=8
        )
        self.add_url_button.grid(row=2, column=0, padx=20, pady=10)

        self.clear_button = ctk.CTkButton(
            self.sidebar,
            text="Clear All",
            command=self.clear_urls,
            font=self.BUTTON_FONT,
            height=40,
            corner_radius=8
        )
        self.clear_button.grid(row=3, column=0, padx=20, pady=10)

        self.output_dir_button = ctk.CTkButton(
            self.sidebar,
            text="Select Output Directory",
            command=self.select_output_dir,
            font=self.BUTTON_FONT,
            height=40,
            corner_radius=8
        )
        self.output_dir_button.grid(row=4, column=0, padx=20, pady=10)

        # Separator before theme selector
        self.separator2 = ctk.CTkFrame(self.sidebar, height=2)
        self.separator2.grid(row=5, column=0, sticky="ew", padx=20, pady=20)

        # Theme selector with label
        self.theme_label = ctk.CTkLabel(
            self.sidebar,
            text="Theme",
            font=self.HEADING_FONT
        )
        self.theme_label.grid(row=6, column=0, padx=20, pady=(0, 5))

        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode,
            font=self.BUTTON_FONT,
            height=35,
            corner_radius=8
        )
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=10)

        # Download button at bottom of sidebar
        self.download_button = ctk.CTkButton(
            self.sidebar,
            text="Start Download",
            command=self.start_download,
            font=self.HEADING_FONT,
            height=50,
            corner_radius=8
        )
        self.download_button.grid(row=8, column=0, padx=20, pady=(20, 30))

        # Main area components with enhanced styling
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="YouTube URLs",
            font=self.HEADING_FONT
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # URL textbox with custom styling
        self.url_textbox = ctk.CTkTextbox(
            self.main_frame,
            font=self.TEXT_FONT,
            corner_radius=8,
            border_spacing=10
        )
        self.url_textbox.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

        # Status area with enhanced visual feedback
        self.status_frame = ctk.CTkFrame(self.main_frame, corner_radius=8)
        self.status_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.status_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready to download",
            font=self.STATUS_FONT
        )
        self.status_label.grid(row=0, column=0, padx=20, pady=(15, 5))

        self.progress_bar = ctk.CTkProgressBar(self.status_frame)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="ew")
        self.progress_bar.set(0)

        # Initialize variables
        self.output_directory = os.path.join(os.path.dirname(__file__), 'output')
        self.urls: List[str] = []
        self.is_downloading = False

        # Load saved settings
        self.load_settings()

        # Set initial theme
        self.appearance_mode_menu.set("System")

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
        try:
            clipboard = self.window.clipboard_get()
            if clipboard:
                current_text = self.url_textbox.get("1.0", "end-1c")
                if current_text and not current_text.endswith('\n'):
                    self.url_textbox.insert("end", "\n")
                self.url_textbox.insert("end", clipboard)
                self.update_status("✓ URL added from clipboard")
        except Exception:
            self.update_status("⚠ No valid URL in clipboard")

    def clear_urls(self):
        """Clear all URLs from the textbox."""
        self.url_textbox.delete("1.0", "end")
        self.update_status("✓ URLs cleared")

    def select_output_dir(self):
        """Open directory selector dialog."""
        directory = ctk.filedialog.askdirectory(initialdir=self.output_directory)
        if directory:
            self.output_directory = directory
            self.save_settings()
            self.update_status(f"✓ Output directory set: {os.path.basename(directory)}")

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
            urls = [url.strip() for url in self.url_textbox.get("1.0", "end-1c").split('\n') if url.strip()]
            total_urls = len(urls)
            
            if not total_urls:
                self.update_status("⚠ No URLs to download")
                return

            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory)

            for i, url in enumerate(urls, 1):
                if not self.is_downloading:
                    break
                
                self.update_status(f"⏳ Downloading video {i}/{total_urls}")
                self.update_progress(i / total_urls)
                
                success = download_video(url, self.output_directory)
                if not success:
                    self.update_status(f"❌ Error downloading: {url}")

            if self.is_downloading:
                self.update_status("✅ All downloads completed!")
            else:
                self.update_status("⏹ Downloads cancelled")
                
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}")
        finally:
            self.is_downloading = False
            self.download_button.configure(text="Start Download")
            self.update_progress(0)

    def start_download(self):
        """Start or stop the download process."""
        if not self.is_downloading:
            self.is_downloading = True
            self.download_button.configure(text="Stop Download")
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