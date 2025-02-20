import os
import subprocess

def download_video(url, output_path='/Users/sahillulla/youtube-downloader/output'):
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
            print("Download completed successfully!")
            return True
        else:
            print(f"Error downloading video: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"\nAn error occurred while downloading {url}:\n{str(e)}\n")
        return False

def download_videos(urls, output_path='/Users/sahillulla/youtube-downloader/output'):
    # Ensure the output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created output directory at: {output_path}\n")
    
    successful_downloads = 0
    failed_downloads = []
    
    total_videos = len(urls)
    for index, url in enumerate(urls, 1):
        print(f"\nProcessing video {index}/{total_videos}")
        print(f"URL: {url}")
        
        if download_video(url, output_path):
            successful_downloads += 1
        else:
            failed_downloads.append(url)
    
    # Print summary
    print("\nDownload Summary:")
    print(f"Successfully downloaded: {successful_downloads}/{total_videos} videos")
    if failed_downloads:
        print("\nFailed downloads:")
        for url in failed_downloads:
            print(f"- {url}")

if __name__ == "__main__":
    print("YouTube Video Downloader (using yt-dlp)")
    print("------------------------------------\n")
    
    # Input multiple YouTube URLs separated by commas
    input_urls = input("Enter YouTube video URLs separated by commas: ").strip()
    url_list = [url.strip() for url in input_urls.split(',') if url.strip()]
    
    if not url_list:
        print("No valid URLs provided. Exiting.")
    else:
        # Use the specified output directory
        output_dir = '/Users/sahillulla/youtube-downloader/output'
        download_videos(url_list, output_dir)
