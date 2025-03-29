import math
import base64
import requests
import numpy as np
from PIL import Image
from io import BytesIO

MIN_PIXEL_COUNT = 64
MAX_PIXEL_COUNT = 1024 ** 2
SMALL_PIXEL_COUNT = 512 ** 2

class URLReadError (Exception):
    def __init__ (self):
        super().__init__(self, 'Failed to read image from provided URL.')

class PathReadError (Exception):
    def __init__ (self):
        super().__init__(self, 'Failed to read image from provided path.')

class ImageFormatError (Exception):
    def __init__(self):
        super().__init__(self, 'Image format not supported.')

class Base64ReadError (Exception):
    def __init__(self):
        super().__init__(self, 'Failed to read image from provided base64 string.')

def convert_RGB_A(img):
    if img.mode == 'RGB' or img.mode == 'RGBA':
        return img
    
    map = {
        '1': 'RGB',
        'L': 'RGB',
        'P': 'RGBA',
        'PA': 'RGBA',
    }

    if not img.mode in map:
        raise ImageFormatError()
    
    return img.convert(map.get(img.mode))

def try_read_image_from_path(path):
    try:
        img = Image.open(path)
    except:
        raise PathReadError()
    return convert_RGB_A(img)

def try_read_image_from_base64(base64_str):
    try:
        # Remove data URL prefix if present
        if ',' in base64_str:
            base64_str = base64_str.split(',')[1]
            
        # Decode base64 string
        image_data = base64.b64decode(base64_str)
        img = Image.open(BytesIO(image_data))
    except Exception as e:
        raise Base64ReadError()
    return convert_RGB_A(img)

def try_read_image_from_url(url):
    try:
        headers = {
            "User-Agent": "KittlVectorizing/1.0.0",
            "Accept": "image/*"  # Accept any image format
        }
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()  # Raise an exception for bad status codes
        
        # Check if the response is an image
        content_type = resp.headers.get('content-type', '').lower()
        if not content_type.startswith('image/'):
            # Try to detect image format from content
            try:
                img = Image.open(BytesIO(resp.content))
                return convert_RGB_A(img)
            except:
                raise URLReadError()
            
        img = Image.open(BytesIO(resp.content))
    except requests.exceptions.RequestException:
        raise URLReadError()
    except Exception as e:
        raise URLReadError()
    return convert_RGB_A(img)

def try_read_image(input_data):
    """
    Try to read an image from various input formats (URL, base64, or file path)
    
    Args:
        input_data (str): Can be a URL, base64 string, or file path
        
    Returns:
        PIL.Image: The loaded and converted image
        
    Raises:
        URLReadError: If URL reading fails
        Base64ReadError: If base64 decoding fails
        PathReadError: If file reading fails
        ImageFormatError: If image format is not supported
    """
    try:
        # Try base64 first if it looks like base64
        if input_data.startswith('data:image/') or input_data.startswith('iVBORw0KGgo') or input_data.startswith('/9j/'):
            return try_read_image_from_base64(input_data)
        
        # Try URL if it starts with http
        if input_data.startswith(('http://', 'https://')):
            return try_read_image_from_url(input_data)
            
        # Otherwise try as file path
        return try_read_image_from_path(input_data)
    except (URLReadError, Base64ReadError, PathReadError):
        raise
    except Exception as e:
        raise URLReadError()