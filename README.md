# ASCII Image Converter

Convert images and videos to ASCII art with an easy-to-use GUI application!

## Features

✨ **Image Conversion**
- Convert images to ASCII text art
- Convert images to colored ASCII art (PNG output)
- Support for JPG, PNG, BMP, GIF formats
- Customizable width setting

🎬 **Video Conversion**
- Convert videos to ASCII art video
- Adjustable frames per second
- Support for MP4, AVI, MOV, MKV formats

🎨 **GUI Application**
- Easy-to-use tkinter interface
- Real-time preview
- Progress indication
- Output folder management

📦 **Executable Build**
- Create standalone .exe with PyInstaller
- No Python installation needed to run executable

## Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**
   ```bash
   python main.py
   ```

## Usage

### Running the GUI Application

**Option 1: Run with Python**
```bash
python main.py
```

**Option 2: Run Executable (after building)**
```bash
dist\ASCII_Image_Converter\ASCII_Image_Converter.exe
```

### GUI Instructions

1. **Select File Type**: Choose between "Image" or "Video"
2. **Browse File**: Click "Browse File" to select your image or video
3. **Configure Settings**:
   - **Width**: Set ASCII art width (20-300 characters)
   - **FPS**: For videos, set frames per second (1-60)
   - **Output Format** (Images only): 
     - Text File: ASCII art as text
     - Colored Image: ASCII art with colors as PNG
4. **Convert**: Click "Convert" button
5. **View Output**: Results appear in the preview area
6. **Access Files**: Click "Open Output Folder" to see generated files

### Output Files

All converted files are saved in the `output/` folder:

- **Images**:
  - `ascii_image.txt` - Text version
  - `ascii_image_colored.png` - Colored version

- **Videos**:
  - `ascii_video.avi` - Colored ASCII video
  - `ascii_video_frames.txt` - Text frames (if using text mode)

## Building an Executable

### Step 1: Install PyInstaller
```bash
pip install pyinstaller
```

### Step 2: Run Build Script (Windows)
```bash
build.bat
```

Or manually:
```bash
pyinstaller ascii_converter.spec
```

### Step 3: Find Executable
The executable will be created at:
```
dist\ASCII_Image_Converter\ASCII_Image_Converter.exe
```

You can now distribute this folder to others - they don't need Python installed!

## Command Line Usage (Advanced)

If you want to use the converter without the GUI:

```python
from converter import ASCIIConverter

# Create converter instance
converter = ASCIIConverter()

# Convert image to text
result, message = converter.image_to_ascii("path/to/image.jpg", new_width=100)
print(result)

# Convert image to colored PNG
output_path, message = converter.image_to_ascii_colored("path/to/image.jpg", new_width=100)

# Convert video
output_path, message = converter.video_to_ascii("path/to/video.mp4", new_width=80, fps=10)
```

## Supported Formats

### Images
- JPG / JPEG
- PNG
- BMP
- GIF

### Videos
- MP4
- AVI
- MOV
- MKV

## Troubleshooting

### Issue: "Failed to load image"
- Ensure the image file path is correct
- Try a different image format
- Check that the file is not corrupted

### Issue: "Failed to open video"
- Ensure the video file path is correct
- Try a different video format (MP4 works best)
- Check that ffmpeg is accessible (for some opencv installations)

### Issue: Executable is blocked by Windows
- Windows may warn about unknown publisher
- Click "More info" → "Run anyway"
- This is normal for self-built executables

### Issue: GUI doesn't appear
- Try running with Python directly: `python gui.py`
- Check tkinter is installed: `python -m tkinter`

## Project Structure

```
Ascii_Image_Convector/
├── main.py              # Entry point - launches GUI
├── gui.py               # GUI application (tkinter)
├── converter.py         # Core conversion logic
├── requirements.txt     # Python dependencies
├── ascii_converter.spec # PyInstaller configuration
├── build.bat           # Build script for Windows
└── output/             # Generated files (created on first use)
```

## Dependencies

- **opencv-python** - Image/video processing
- **Pillow** - Image handling
- **numpy** - Numerical operations
- **tkinter** - GUI (built-in with Python)

## Tips for Best Results

1. **Image Width**: 
   - Start with 100 characters
   - Increase for more detail, decrease for simpler art

2. **Video Processing**:
   - Lower FPS values create smaller files
   - Start with 10 FPS and adjust as needed

3. **Output Quality**:
   - Colored images show more detail than text-only
   - Terminal width affects text preview display

## Performance Notes

- Image conversion is very fast (< 1 second)
- Video conversion depends on:
  - Video resolution
  - Video length
  - Selected FPS
  - Computer performance

## Future Enhancements

Possible improvements:
- Live camera feed conversion
- Batch conversion for multiple files
- Web interface
- Animation export options
- Different character sets for different styles

## License

This project is free to use and modify.

## Support

For issues or questions:
1. Check Troubleshooting section above
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Try running `python main.py` to see detailed error messages

---

**Enjoy creating ASCII art!** 🎨
# My-Redemption
