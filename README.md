# YouTube Video Downloader

A Python script to download multiple YouTube videos simultaneously using yt-dlp.

## Features

- Download multiple YouTube videos by providing URLs
- Downloads highest quality available in MP4 format
- Shows download progress and summary
- Handles errors gracefully
- Creates output directory automatically

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

1. Run the script:
```bash
python youtube_downloader.py
```

2. Enter YouTube video URLs separated by commas when prompted

3. Videos will be downloaded to the `output` directory

## Output

The downloaded videos will be saved in the `output` directory with their original titles.

## Error Handling

- The script will continue downloading other videos even if one fails
- A summary of successful and failed downloads is provided at the end
- Error messages are displayed for failed downloads

## License

MIT License 