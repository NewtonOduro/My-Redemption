"""
ASCII Art Converter Module
Converts images and videos to ASCII art
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# ASCII characters from darkest to lightest
ASCII_CHARS = "@%#*+=-:. "

class ASCIIConverter:
    def __init__(self):
        self.output_folder = "output"
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def resize_image(self, image, new_width=100):
        """Resize image while maintaining aspect ratio"""
        height, width = image.shape[:2]
        ratio = height / width
        new_height = int(new_width * ratio * 0.55)  # 0.55 to account for character aspect ratio
        resized = cv2.resize(image, (new_width, new_height))
        return resized
    
    def get_ascii_char(self, pixel_value):
        """Convert pixel value to ASCII character"""
        index = int((pixel_value / 255) * (len(ASCII_CHARS) - 1))
        return ASCII_CHARS[index]
    
    def image_to_ascii(self, image_path, new_width=100, output_text=True):
        """Convert image to ASCII art"""
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                return None, "Failed to load image"
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Resize image
            resized = self.resize_image(gray, new_width)
            
            # Convert pixels to ASCII
            height, width = resized.shape
            ascii_art = []
            
            for y in range(height):
                row = ""
                for x in range(width):
                    pixel = resized[y, x]
                    row += self.get_ascii_char(pixel)
                ascii_art.append(row)
            
            ascii_string = "\n".join(ascii_art)
            
            # Save to text file if requested
            if output_text:
                output_path = os.path.join(self.output_folder, "ascii_image.txt")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(ascii_string)
            
            return ascii_string, "Success"
        
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def image_to_ascii_colored(self, image_path, new_width=100):
        """Convert image to colored ASCII art (saves as image)"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None, "Failed to load image"
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            resized_gray = self.resize_image(gray, new_width)
            
            # Resize original for color mapping
            height, width = resized_gray.shape
            resized_color = cv2.resize(img, (width, height))
            
            # Create output image
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.4
            font_thickness = 1
            
            # Calculate output size
            cell_width = 8
            cell_height = 15
            output_height = height * cell_height
            output_width = width * cell_width
            
            output_img = np.ones((output_height, output_width, 3), dtype=np.uint8) * 255
            
            # Fill with ASCII characters
            for y in range(height):
                for x in range(width):
                    pixel = resized_gray[y, x]
                    char = self.get_ascii_char(pixel)
                    
                    # Get color from original image
                    b, g, r = resized_color[y, x]
                    color = (int(b), int(g), int(r))
                    
                    # Place character
                    x_pos = x * cell_width
                    y_pos = y * cell_height + 12
                    cv2.putText(output_img, char, (x_pos, y_pos), font, 
                               font_scale, color, font_thickness)
            
            output_path = os.path.join(self.output_folder, "ascii_image_colored.png")
            cv2.imwrite(output_path, output_img)
            
            return output_path, "Success"
        
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def video_to_ascii(self, video_path, new_width=80, fps=10):
        """Convert video to ASCII art video"""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return None, "Failed to open video"
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            original_fps = cap.get(cv2.CAP_PROP_FPS)
            frame_skip = int(original_fps / fps)
            
            # Get first frame to determine size
            ret, frame = cap.read()
            if not ret:
                return None, "Failed to read first frame"
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized = self.resize_image(gray, new_width)
            height, width = resized.shape
            
            # Create video writer for colored ASCII output
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.4
            font_thickness = 1
            
            cell_width = 8
            cell_height = 15
            output_height = height * cell_height
            output_width = width * cell_width
            
            output_path = os.path.join(self.output_folder, "ascii_video.avi")
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_path, fourcc, fps, 
                                 (output_width, output_height))
            
            frame_count = 0
            processed_frames = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_skip == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    resized_gray = self.resize_image(gray, new_width)
                    resized_color = cv2.resize(frame, (width, height))
                    
                    output_frame = np.ones((output_height, output_width, 3), 
                                          dtype=np.uint8) * 255
                    
                    for y in range(height):
                        for x in range(width):
                            pixel = resized_gray[y, x]
                            char = self.get_ascii_char(pixel)
                            b, g, r = resized_color[y, x]
                            color = (int(b), int(g), int(r))
                            
                            x_pos = x * cell_width
                            y_pos = y * cell_height + 12
                            cv2.putText(output_frame, char, (x_pos, y_pos), 
                                       font, font_scale, color, font_thickness)
                    
                    out.write(output_frame)
                    processed_frames += 1
                
                frame_count += 1
            
            cap.release()
            out.release()
            
            return output_path, f"Success - {processed_frames} frames processed"
        
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def video_to_ascii_text(self, video_path, new_width=80, fps=2):
        """Convert video to ASCII text frames (for terminal output)"""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return None, "Failed to open video"
            
            original_fps = cap.get(cv2.CAP_PROP_FPS)
            frame_skip = int(original_fps / fps) if fps > 0 else 1
            
            output_path = os.path.join(self.output_folder, "ascii_video_frames.txt")
            
            with open(output_path, "w", encoding="utf-8") as f:
                frame_count = 0
                processed_frames = 0
                
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    if frame_count % frame_skip == 0:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        resized = self.resize_image(gray, new_width)
                        
                        height, width = resized.shape
                        f.write(f"\n--- Frame {processed_frames} ---\n")
                        
                        for y in range(height):
                            for x in range(width):
                                pixel = resized[y, x]
                                f.write(self.get_ascii_char(pixel))
                            f.write("\n")
                        
                        processed_frames += 1
                    
                    frame_count += 1
            
            cap.release()
            return output_path, f"Success - {processed_frames} frames saved"
        
        except Exception as e:
            return None, f"Error: {str(e)}"
