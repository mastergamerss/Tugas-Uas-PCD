import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure, util
from scipy.ndimage import gaussian_filter

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("900x600")
        
        # Set default font to Constantia
        self.root.option_add("*Font", "Constantia 10")
        
        # Header section with a label and an image
        header_frame = tk.Frame(self.root, bg="#C26D1E", height=100)  # Header color changed here
        header_frame.pack(fill="x")
        
        header_label = tk.Label(header_frame, text="TUGAS UAS PENGOLAHAN CITRA DIGITAL", font=("Constantia", 16), bg="#C26D1E")
        header_label.pack(pady=10)
        
        # Main image display area
        self.image_label = tk.Label(self.root, bg="#D2A04C")
        self.image_label.pack(fill="both", expand=True)
        
        # Button frame at the bottom
        self.button_frame = tk.Frame(self.root, bg="#D2A04C")
        self.button_frame.pack(side="bottom", fill="x", pady=10)
        
        # Button style configuration
        button_options = {"bg": "#263238", "fg": "white", "font": ("Constantia", 10), "width": 20}
        
        # Adding buttons according to the image layout
        self.open_button = tk.Button(self.button_frame, text="Open Image", command=self.open_image, **button_options)
        self.open_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.gray_button = tk.Button(self.button_frame, text="Convert to Grayscale", command=self.convert_to_grayscale, **button_options)
        self.gray_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.negative_button = tk.Button(self.button_frame, text="Convert to Negative", command=self.convert_to_negative, **button_options)
        self.negative_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.blur_button = tk.Button(self.button_frame, text="Apply Blur Effect", command=self.apply_blur, **button_options)
        self.blur_button.grid(row=0, column=3, padx=5, pady=5)
        
        self.contrast_button = tk.Button(self.button_frame, text="Contrast Stretching", command=self.contrast_stretching, **button_options)
        self.contrast_button.grid(row=0, column=4, padx=5, pady=5)
        
        self.noise_reduction_button = tk.Button(self.button_frame, text="Reduksi Noise", command=self.reduce_noise, **button_options)
        self.noise_reduction_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.brightness_button = tk.Button(self.button_frame, text="Brightness and color adjustment", command=self.adjust_brightness_and_color, **button_options)
        self.brightness_button.grid(row=1, column=1, padx=5, pady=5)
        
        self.sharpen_button = tk.Button(self.button_frame, text="Sharpening", command=self.sharpen_image, **button_options)
        self.sharpen_button.grid(row=1, column=2, padx=5, pady=5)
        
        self.histogram_button = tk.Button(self.button_frame, text="Show Histogram", command=self.show_histogram, **button_options)
        self.histogram_button.grid(row=1, column=3, padx=5, pady=5)
        
        self.reset_button = tk.Button(self.button_frame, text="Reset to Original", command=self.reset_to_original, **button_options)
        self.reset_button.grid(row=1, column=4, padx=5, pady=5)
        
        self.save_button = tk.Button(self.button_frame, text="Save Image", command=self.save_image, **button_options)
        self.save_button.grid(row=1, column=5, padx=5, pady=5)
        
        self.image = None
        self.original_image = None  
        self.processed_image = None
    
    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((self.root.winfo_screenwidth() // 2, self.root.winfo_screenheight() // 2))
            self.original_image = self.image.copy()
            self.display_image(self.image)
    
    def display_image(self, img):
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk
    
    def convert_to_grayscale(self):
        if self.image:
            self.processed_image = ImageOps.grayscale(self.image)
            self.display_image(self.processed_image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")
    
    def convert_to_negative(self):
        if self.image:
            self.processed_image = ImageOps.invert(self.image.convert("RGB"))
            self.display_image(self.processed_image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")
    
    def apply_blur(self):
        if self.image:
            self.processed_image = self.image.filter(ImageFilter.BLUR)
            self.display_image(self.processed_image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")
    
    def contrast_stretching(self):
        if self.image:
            img_array = np.array(self.image)
            p2, p98 = np.percentile(img_array, (2, 98))
            self.processed_image = Image.fromarray(np.uint8(exposure.rescale_intensity(img_array, in_range=(p2, p98))))
            self.display_image(self.processed_image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")
    
    def reduce_noise(self):
        if self.image:
            img_array = np.array(self.image)
            noisy_image = util.random_noise(img_array, mode='gaussian', var=0.01)
            denoised_image = gaussian_filter(noisy_image, sigma=1)
            self.processed_image = Image.fromarray((denoised_image * 255).astype(np.uint8))
            self.display_image(self.processed_image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")
    
    def adjust_brightness_and_color(self):
        if self.image:
            brightness_enhancer = ImageEnhance.Brightness(self.image)
            color_enhancer = ImageEnhance.Color(self.image)
            self.processed_image = brightness_enhancer.enhance(1.2)
            self.processed_image = color_enhancer.enhance(1.3)
            self.display_image(self.processed_image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")
    
    def sharpen_image(self):
        if self.image:
            self.processed_image = self.image.filter(ImageFilter.SHARPEN)
            self.display_image(self.processed_image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")
    
    def show_histogram(self):
        if self.processed_image:
            img_array = np.array(self.processed_image)
            plt.figure(figsize=(6, 4))
            plt.hist(img_array.ravel(), bins=256, range=(0, 255), histtype='step', color='black')
            plt.title('Image Histogram')
            plt.xlabel('Pixel Intensity')
            plt.ylabel('Frequency')
            plt.show()
        else:
            messagebox.showwarning("No Processed Image", "There is no processed image to display histogram.")
    
    def reset_to_original(self):
        if self.original_image:
            self.image = self.original_image.copy()
            self.processed_image = self.image
            self.display_image(self.image)
        else:
            messagebox.showwarning("No Image", "Please open an image first.")
    
    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("BMP files", "*.bmp"), ("TIFF files", "*.tiff")])
            if file_path:
                self.processed_image.save(file_path)
        else:
            messagebox.showwarning("No Processed Image", "There is no processed image to save.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()





