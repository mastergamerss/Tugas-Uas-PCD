import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance
import numpy as np
from skimage import util
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("900x600")
        
        # Set default font to Constantia
        self.root.option_add("*Font", "Constantia 10")
        
        # Header section with a label and an image
        header_frame = tk.Frame(self.root, bg="#C26D1E", height=100)
        header_frame.pack(fill="x")
        
        header_label = tk.Label(header_frame, text="TUGAS UAS PENGOLAHAN CITRA DIGITAL", font=("Constantia", 16), bg="#C26D1E")
        header_label.pack(pady=10)
        
        # Main image display area
        self.image_label = tk.Label(self.root, bg="#D2A04C")
        self.image_label.pack(fill="both", expand=True)
        
        # Button frame at the bottom
        self.button_frame = tk.Frame(self.root, bg="#D2A04C")
        self.button_frame.pack(side="bottom", fill="x", pady=10)

        # Slider frame on the right
        self.slider_frame = tk.Frame(self.root, bg="#D2A04C")
        self.slider_frame.pack(side="right", fill="y", padx=10)

        # Button style configuration
        button_options = {"bg": "#263238", "fg": "white", "font": ("Constantia", 10), "width": 20}
        
        # Adding buttons according to the image layout
        self.open_button = tk.Button(self.button_frame, text="Buka Gambar", command=self.open_image, **button_options)
        self.open_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.gray_button = tk.Button(self.button_frame, text="Ubah ke Grayscale", command=self.convert_to_grayscale, **button_options)
        self.gray_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.negative_button = tk.Button(self.button_frame, text="Ubah ke Negatif", command=self.convert_to_negative, **button_options)
        self.negative_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.blur_button = tk.Button(self.button_frame, text="Terapkan Efek Blur", command=self.apply_blur, **button_options)
        self.blur_button.grid(row=0, column=3, padx=5, pady=5)
        
        self.contrast_button = tk.Button(self.button_frame, text="Kontras", command=self.contrast_stretching, **button_options)
        self.contrast_button.grid(row=0, column=4, padx=5, pady=5)
        
        self.noise_reduction_button = tk.Button(self.button_frame, text="Reduksi Noise", command=self.reduce_noise, **button_options)
        self.noise_reduction_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.brightness_button = tk.Button(self.button_frame, text="Atur Kecerahan", command=self.adjust_brightness_and_color, **button_options)
        self.brightness_button.grid(row=1, column=1, padx=5, pady=5)
        
        self.sharpen_button = tk.Button(self.button_frame, text="Penajaman", command=self.sharpen_image, **button_options)
        self.sharpen_button.grid(row=1, column=2, padx=5, pady=5)
        
        self.histogram_button = tk.Button(self.button_frame, text="Tampilkan Histogram", command=self.show_histogram, **button_options)
        self.histogram_button.grid(row=1, column=3, padx=5, pady=5)
        
        self.reset_button = tk.Button(self.button_frame, text="Reset ke Asli", command=self.reset_to_original, **button_options)
        self.reset_button.grid(row=1, column=4, padx=5, pady=5)
        
        self.save_button = tk.Button(self.button_frame, text="Simpan Gambar", command=self.save_image, **button_options)
        self.save_button.grid(row=1, column=5, padx=5, pady=5)
        
        self.image = None
        self.original_image = None  
        self.processed_image = None
        self.slider = None
        self.slider_label = None

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
            self._remove_existing_slider()
            # Create a new slider for grayscale
            self.slider_label = tk.Label(self.slider_frame, text="Grayscale", font=("Constantia", 10), bg="#D2A04C")
            self.slider_label.pack(side="top", pady=5)
            self.slider = tk.Scale(self.slider_frame, from_=0, to=100, orient="horizontal", command=self.update_grayscale, bg="#D2A04C", length=300, sliderlength=30)
            self.slider.pack(side="top", pady=5)
        else:
            messagebox.showwarning("No Image", "Silakan buka gambar terlebih dahulu.")
    
    def update_grayscale(self, value):
        if self.image:
            value = int(value)  # Grayscale level should be an integer
            grayscale_image = ImageOps.grayscale(self.image)
            # Apply grayscale with some intensity; this example is simple and does not use the slider
            self.processed_image = grayscale_image
            self.display_image(self.processed_image)
    
    def convert_to_negative(self):
        if self.image:
            self._remove_existing_slider()
            # Create a new slider for negative
            self.slider_label = tk.Label(self.slider_frame, text="Negatif", font=("Constantia", 10), bg="#D2A04C")
            self.slider_label.pack(side="top", pady=5)
            self.slider = tk.Scale(self.slider_frame, from_=0, to=100, orient="horizontal", command=self.update_negative, bg="#D2A04C", length=300, sliderlength=30)
            self.slider.pack(side="top", pady=5)
        else:
            messagebox.showwarning("No Image", "Silakan buka gambar terlebih dahulu.")
    
    def update_negative(self, value):
        if self.image:
            value = int(value)  # Negative level should be an integer
            if value == 0:
                self.processed_image = ImageOps.invert(self.image.convert("RGB"))
            else:
                self.processed_image = ImageOps.invert(self.image.convert("RGB"))  # Example, you can customize further
            self.display_image(self.processed_image)

    def apply_blur(self):
        if self.image:
            self._remove_existing_slider()
            # Create a new slider for blur
            self.slider_label = tk.Label(self.slider_frame, text="Blur", font=("Constantia", 10), bg="#D2A04C")
            self.slider_label.pack(side="top", pady=5)
            self.slider = tk.Scale(self.slider_frame, from_=0, to=10, orient="horizontal", resolution=0.1, command=self.update_blur, bg="#D2A04C", length=300, sliderlength=30)
            self.slider.pack(side="top", pady=5)
        else:
            messagebox.showwarning("No Image", "Silakan buka gambar terlebih dahulu.")
    
    def update_blur(self, value):
        if self.image:
            self.processed_image = self.image.filter(ImageFilter.GaussianBlur(float(value)))
            self.display_image(self.processed_image)
    
    def contrast_stretching(self):
        if self.image:
            self._remove_existing_slider()
            # Create a new slider for contrast
            self.slider_label = tk.Label(self.slider_frame, text="Kontras", font=("Constantia", 10), bg="#D2A04C")
            self.slider_label.pack(side="top", pady=5)
            self.slider = tk.Scale(self.slider_frame, from_=0.5, to=2, orient="horizontal", resolution=0.1, command=self.update_contrast, bg="#D2A04C", length=300, sliderlength=30)
            self.slider.pack(side="top", pady=5)
        else:
            messagebox.showwarning("No Image", "Silakan buka gambar terlebih dahulu.")
    
    def update_contrast(self, value):
        if self.image:
            contrast_enhancer = ImageEnhance.Contrast(self.image)
            self.processed_image = contrast_enhancer.enhance(float(value))
            self.display_image(self.processed_image)

    def adjust_brightness_and_color(self):
        if self.image:
            self._remove_existing_slider()
            # Create a new slider for brightness
            self.slider_label = tk.Label(self.slider_frame, text="Kecerahan", font=("Constantia", 10), bg="#D2A04C")
            self.slider_label.pack(side="top", pady=5)
            self.slider = tk.Scale(self.slider_frame, from_=0.5, to=2, orient="horizontal", resolution=0.1, command=self.update_brightness, bg="#D2A04C", length=300, sliderlength=30)
            self.slider.pack(side="top", pady=5)
        else:
            messagebox.showwarning("No Image", "Silakan buka gambar terlebih dahulu.")
    
    def update_brightness(self, value):
        if self.image:
            brightness_enhancer = ImageEnhance.Brightness(self.image)
            self.processed_image = brightness_enhancer.enhance(float(value))
            self.display_image(self.processed_image)
    
    def sharpen_image(self):
        if self.image:
            self._remove_existing_slider()
            # Create a new slider for sharpening
            self.slider_label = tk.Label(self.slider_frame, text="Penajaman", font=("Constantia", 10), bg="#D2A04C")
            self.slider_label.pack(side="top", pady=5)
            self.slider = tk.Scale(self.slider_frame, from_=0, to=10, orient="horizontal", command=self.update_sharpen, bg="#D2A04C", length=300, sliderlength=30)
            self.slider.pack(side="top", pady=5)
        else:
            messagebox.showwarning("No Image", "Silakan buka gambar terlebih dahulu.")
    
    def update_sharpen(self, value):
        if self.image:
            try:
                threshold_value = int(float(value))
                self.processed_image = self.image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=threshold_value))
                self.display_image(self.processed_image)
            except ValueError:
                messagebox.showerror("Error", "Invalid threshold value for sharpening.")
    
    def reduce_noise(self):
        if self.image:
            self._remove_existing_slider()
            # Create a new slider for noise reduction
            self.slider_label = tk.Label(self.slider_frame, text="Reduksi Noise", font=("Constantia", 10), bg="#D2A04C")
            self.slider_label.pack(side="top", pady=5)
            self.slider = tk.Scale(self.slider_frame, from_=0, to=100, orient="horizontal", command=self.update_noise_reduction, bg="#D2A04C", length=300, sliderlength=30)
            self.slider.pack(side="top", pady=5)
        else:
            messagebox.showwarning("No Image", "Silakan buka gambar terlebih dahulu.")
    
    def update_noise_reduction(self, value):
        if self.image:
            noise_level = int(value)
            img_array = np.array(self.image)
            noisy_image = util.random_noise(img_array, var=noise_level**2 / 10000.0)
            smoothed_image = gaussian_filter(noisy_image, sigma=1)
            self.processed_image = Image.fromarray(np.uint8(smoothed_image * 255))
            self.display_image(self.processed_image)
    
    def show_histogram(self):
        if self.image:
            img_array = np.array(self.image.convert("L"))
            plt.hist(img_array.ravel(), bins=256, color='gray')
            plt.title("Histogram")
            plt.xlabel("Pixel Value")
            plt.ylabel("Frequency")
            plt.show()
        else:
            messagebox.showwarning("No Image", "Silakan buka gambar terlebih dahulu.")
    
    def reset_to_original(self):
        if self.original_image:
            self.image = self.original_image
            self.display_image(self.image)
            self.processed_image = None
            self._remove_existing_slider()
        else:
            messagebox.showwarning("No Image", "Tidak ada gambar yang bisa direset.")
    
    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                self.processed_image.save(file_path)
        else:
            messagebox.showwarning("No Image", "Silakan olah gambar terlebih dahulu sebelum menyimpan.")
    
    def _remove_existing_slider(self):
        if self.slider:
            self.slider.destroy()
            self.slider_label.destroy()
            self.slider = None
            self.slider_label = None

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()






