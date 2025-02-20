import os
import subprocess
import glob
from typing import List, Tuple

def read_urls_from_file(file_path: str) -> List[str]:
    """Read URLs from a text file, ignoring comments and empty lines."""
    urls = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                # Remove whitespace and skip empty lines or comments
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)
        return urls
    except Exception as e:
        print(f"\nError reading {file_path}:\n{str(e)}\n")
        return []

def get_all_urls_from_input_dir() -> List[Tuple[str, List[str]]]:
    """Get URLs from all .txt files in the input directory."""
    input_dir = os.path.join(os.path.dirname(__file__), 'input')
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"Created input directory at: {input_dir}")
        print("Please add .txt files with YouTube URLs (one per line) to the input directory.")
        return []
    
    txt_files = glob.glob(os.path.join(input_dir, '*.txt'))
    if not txt_files:
        print("\nNo .txt files found in the input directory.")
        print(f"Please add .txt files with YouTube URLs to: {input_dir}")
        return []
    
    all_urls = []
    for file_path in txt_files:
        urls = read_urls_from_file(file_path)
        if urls:
            all_urls.append((os.path.basename(file_path), urls))
    
    return all_urls

def download_video(url: str, output_path: str = 'output') -> bool:
    """Download a single video using yt-dlp."""
    try:
        # Construct the yt-dlp command
        command = [
            'yt-dlp',
            '--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Prefer MP4
            '--output', os.path.join(output_path, '%(title)s.%(ext)s'),
            '--no-playlist',
            '--no-warnings',
            url
        ]
        
        print(f"\nDownloading video from: {url}")
        # Run the command and capture output
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Download completed successfully!")
            return True
        else:
            print(f"✗ Error downloading video: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"\n✗ An error occurred while downloading {url}:\n{str(e)}\n")
        return False

def download_videos(file_urls: List[Tuple[str, List[str]]], output_base: str = 'output') -> None:
    """Download videos from multiple files, organizing them in subdirectories."""
    if not file_urls:
        print("\nNo URLs to process. Please add some URLs to your input files.")
        return
    
    total_files = len(file_urls)
    total_successful = 0
    total_failed = 0
    failed_downloads = []
    
    for file_index, (file_name, urls) in enumerate(file_urls, 1):
        print(f"\n{'='*60}")
        print(f"Processing file {file_index}/{total_files}: {file_name}")
        print(f"{'='*60}")
        
        # Create output subdirectory based on input filename (without .txt)
        output_subdir = os.path.join(output_base, os.path.splitext(file_name)[0])
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)
        
        successful_downloads = 0
        total_videos = len(urls)
        
        for index, url in enumerate(urls, 1):
            print(f"\nVideo {index}/{total_videos}")
            if download_video(url, output_subdir):
                successful_downloads += 1
            else:
                failed_downloads.append((file_name, url))
        
        print(f"\nCompleted file {file_name}:")
        print(f"Successfully downloaded: {successful_downloads}/{total_videos} videos")
        
        total_successful += successful_downloads
        total_failed += (total_videos - successful_downloads)
    
    # Print final summary
    print(f"\n{'='*60}")
    print("Download Summary")
    print(f"{'='*60}")
    print(f"Total files processed: {total_files}")
    print(f"Total videos downloaded: {total_successful}")
    print(f"Total failed downloads: {total_failed}")
    
    if failed_downloads:
        print("\nFailed downloads:")
        for file_name, url in failed_downloads:
            print(f"- [{file_name}] {url}")

def main():
    """Main function to run the downloader."""
    print("YouTube Video Downloader")
    print("----------------------")
    print("\nReading URLs from input directory...")
    
    # Get all URLs from input directory
    file_urls = get_all_urls_from_input_dir()
    
    if file_urls:
        print(f"\nFound {len(file_urls)} file(s) with URLs to process.")
        # Create base output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Process all files
        download_videos(file_urls, output_dir)
    else:
        print("\nNo URLs to process. Please add .txt files with URLs to the input directory.")
        print("You can use 'sample_urls.txt' as a template.")

if __name__ == "__main__":
    main()
