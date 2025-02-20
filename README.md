# YouTube Video Downloader

A Python script to download multiple YouTube videos simultaneously using yt-dlp. Simply add your YouTube URLs to text files in the input directory, and run the script to download all videos.

## Features

- Download multiple YouTube videos by providing URLs in text files
- Downloads highest quality available in MP4 format
- Shows download progress and summary
- Handles errors gracefully
- Organizes downloads in subdirectories based on input files
- Creates output directory automatically
- Supports comments and ignores empty lines in input files

## Requirements

- Python 3.x
- yt-dlp

## Installation

1. Clone this repository:
```bash
git clone https://github.com/bitrate-bash/youtube-downloader.git
cd youtube-downloader
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Create a text file in the `input` directory (you can use `sample_urls.txt` as a template)

2. Add your YouTube URLs to the text file, one per line:
```
# Comments start with #
https://www.youtube.com/watch?v=example1
https://www.youtube.com/watch?v=example2
https://youtu.be/example3
```

3. You can create multiple text files - each file's downloads will be organized in its own subdirectory

4. Run the script:
```bash
python youtube_downloader.py
```

## Directory Structure

```
youtube-downloader/
├── input/                  # Put your URL files here
│   └── sample_urls.txt     # Example template
├── output/                 # Downloaded videos go here
│   └── sample_urls/       # Subdirectory for each input file
├── youtube_downloader.py   # Main script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Output Organization

- Videos are organized in subdirectories based on the input file names
- For example, URLs from `input/music.txt` will be downloaded to `output/music/`
- Each video is saved with its original title
- Failed downloads are logged in the summary

## Error Handling

- The script will continue downloading other videos even if one fails
- A summary of successful and failed downloads is provided at the end
- Error messages are displayed for failed downloads
- Comments and empty lines in input files are ignored

## License

MIT License 