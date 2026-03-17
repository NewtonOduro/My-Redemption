"""
ASCII Art Converter - GUI Application
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
from converter import ASCIIConverter
import os

class ASCIIConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Converter")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Set style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.converter = ASCIIConverter()
        self.selected_file = tk.StringVar(value="No file selected")
        self.file_type = tk.StringVar(value="image")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title = ttk.Label(self.root, text="ASCII Art Converter", 
                         font=("Arial", 20, "bold"))
        title.pack(pady=10)
        
        # File selection frame
        file_frame = ttk.LabelFrame(self.root, text="Select File", padding=10)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        # File type selection
        type_frame = ttk.Frame(file_frame)
        type_frame.pack(fill="x", pady=5)
        ttk.Label(type_frame, text="File Type:").pack(side="left", padx=5)
        ttk.Radiobutton(type_frame, text="Image", variable=self.file_type, 
                       value="image").pack(side="left", padx=5)
        ttk.Radiobutton(type_frame, text="Video", variable=self.file_type, 
                       value="video").pack(side="left", padx=5)
        
        # File selection buttons
        button_frame = ttk.Frame(file_frame)
        button_frame.pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Browse File", 
                  command=self.select_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=lambda: self.selected_file.set("No file selected")
                  ).pack(side="left", padx=5)
        
        # Selected file display
        ttk.Label(file_frame, textvariable=self.selected_file, 
                 foreground="blue").pack(fill="x", padx=5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(self.root, text="Settings", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        # Width setting
        width_frame = ttk.Frame(settings_frame)
        width_frame.pack(fill="x", pady=5)
        ttk.Label(width_frame, text="Width (characters):").pack(side="left", padx=5)
        self.width_var = tk.StringVar(value="100")
        ttk.Spinbox(width_frame, from_=20, to=300, textvariable=self.width_var, 
                   width=10).pack(side="left", padx=5)
        
        # FPS setting (for video)
        fps_frame = ttk.Frame(settings_frame)
        fps_frame.pack(fill="x", pady=5)
        ttk.Label(fps_frame, text="Frames Per Second (video):").pack(side="left", padx=5)
        self.fps_var = tk.StringVar(value="10")
        ttk.Spinbox(fps_frame, from_=1, to=60, textvariable=self.fps_var, 
                   width=10).pack(side="left", padx=5)
        
        # Output type frame
        output_frame = ttk.LabelFrame(settings_frame, text="Output Format (Image)")
        output_frame.pack(fill="x", pady=5)
        self.output_var = tk.StringVar(value="text")
        ttk.Radiobutton(output_frame, text="Text File", variable=self.output_var, 
                       value="text").pack(side="left", padx=5)
        ttk.Radiobutton(output_frame, text="Colored Image", variable=self.output_var, 
                       value="colored").pack(side="left", padx=5)
        
        # Convert button
        self.convert_btn = ttk.Button(self.root, text="Convert", 
                                     command=self.convert)
        self.convert_btn.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill="x", padx=10, pady=5)
        
        # Output frame
        output_label = ttk.LabelFrame(self.root, text="Output/Preview", padding=10)
        output_label.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Button frame for output
        btn_frame = ttk.Frame(output_label)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Open Output Folder", 
                  command=self.open_output_folder).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Output", 
                  command=self.clear_output_text).pack(side="left", padx=5)
        
        # Output text
        self.output_text = scrolledtext.ScrolledText(output_label, height=15, 
                                                    wrap=tk.WORD, font=("Courier", 8))
        self.output_text.pack(fill="both", expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief="sunken")
        status_bar.pack(fill="x", side="bottom")
    
    def select_file(self):
        file_type = self.file_type.get()
        
        if file_type == "image":
            filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), 
                        ("All files", "*.*")]
        else:
            filetypes = [("Video files", "*.mp4 *.avi *.mov *.mkv"), 
                        ("All files", "*.*")]
        
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        
        if file_path:
            self.selected_file.set(file_path)
            self.status_var.set(f"File selected: {os.path.basename(file_path)}")
    
    def convert(self):
        file_path = self.selected_file.get()
        
        if file_path == "No file selected" or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid file")
            return
        
        # Start conversion in a separate thread
        thread = threading.Thread(target=self._convert_thread, args=(file_path,))
        thread.daemon = True
        thread.start()
    
    def _convert_thread(self, file_path):
        try:
            self.convert_btn.config(state="disabled")
            self.progress.start()
            self.status_var.set("Converting...")
            self.output_text.delete("1.0", "end")
            
            file_type = self.file_type.get()
            width = int(self.width_var.get())
            fps = int(self.fps_var.get())
            
            if file_type == "image":
                output_format = self.output_var.get()
                
                if output_format == "text":
                    result, message = self.converter.image_to_ascii(file_path, width)
                    
                    if result:
                        self.output_text.insert("1.0", result)
                        self.status_var.set(f"Conversion successful! Saved to: ascii_image.txt")
                        messagebox.showinfo("Success", 
                                          f"Image converted successfully!\n"
                                          f"Output saved to: output/ascii_image.txt")
                    else:
                        self.status_var.set(f"Conversion failed: {message}")
                        messagebox.showerror("Error", f"Conversion failed!\n{message}")
                
                else:  # colored
                    result, message = self.converter.image_to_ascii_colored(file_path, width)
                    
                    if result:
                        self.output_text.insert("1.0", 
                                               f"Colored ASCII image created!\n"
                                               f"Output: {result}")
                        self.status_var.set(f"Conversion successful! Saved to: ascii_image_colored.png")
                        messagebox.showinfo("Success", 
                                          f"Colored ASCII image created!\n"
                                          f"Output saved to: {result}")
                    else:
                        self.status_var.set(f"Conversion failed: {message}")
                        messagebox.showerror("Error", f"Conversion failed!\n{message}")
            
            else:  # video
                result, message = self.converter.video_to_ascii(file_path, width, fps)
                
                if result:
                    self.output_text.insert("1.0", 
                                           f"ASCII video created successfully!\n"
                                           f"Output: {result}\n\n"
                                           f"Message: {message}")
                    self.status_var.set(f"Conversion successful! {message}")
                    messagebox.showinfo("Success", 
                                      f"Video converted successfully!\n"
                                      f"{message}\n"
                                      f"Output saved to: {result}")
                else:
                    self.status_var.set(f"Conversion failed: {message}")
                    messagebox.showerror("Error", f"Conversion failed!\n{message}")
        
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        
        finally:
            self.progress.stop()
            self.convert_btn.config(state="normal")
    
    def open_output_folder(self):
        output_path = os.path.abspath("output")
        if os.path.exists(output_path):
            os.startfile(output_path)
        else:
            messagebox.showinfo("Info", "Output folder does not exist yet. "
                              "Convert a file first.")
    
    def clear_output_text(self):
        self.output_text.delete("1.0", "end")

def main():
    root = tk.Tk()
    app = ASCIIConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
