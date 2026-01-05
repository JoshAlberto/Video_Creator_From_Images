# Video_Creator_From_Images
This project converts a folder of images into a uniform MP4 video.  
All images are resized to the exact target resolution (stretching if necessary) so that the final video has no black borders and a consistent format.

The script asks for:
- Folder name containing the images
- Duration per image (seconds)
- Final resolution (e.g. `1920x540`)

---

## Features

- Creates an MP4 video from numbered images (`Imagen1`, `Imagen2`, …)
- All images are stretched to the same resolution
- No black borders
- H.264 compatible output
- Automatically creates a working folder with scaled images
- Supports PNG and JPG images

---

## Requirements

- **Python 3.12 (64-bit)** recommended  
- **FFmpeg** installed and accessible from terminal  

---

## Install Python

Download Python 3.12 from:

https://www.python.org/downloads/release/python-312/

During installation:
- Enable **Add Python to PATH**
- Install `pip`

Check installation:

```powershell
py -3.12 --version
