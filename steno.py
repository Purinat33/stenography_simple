from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog


class ImageEncryptorDecryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryptor & Decryptor")

        # File paths for images
        self.main_img_path = ""
        self.hidden_img_path = ""
        self.encrypted_img_path = ""

        # Create UI elements
        self.main_img_label = tk.Label(root, text="MAIN Image:")
        self.hidden_img_label = tk.Label(root, text="HIDDEN Image:")
        self.encrypted_img_label = tk.Label(
            root, text="ENCRYPTED Image to be decrypted:")

        self.main_img_button = tk.Button(
            root, text="Upload", command=self.upload_main_image)
        self.hidden_img_button = tk.Button(
            root, text="Upload", command=self.upload_hidden_image)
        self.encrypted_img_button = tk.Button(
            root, text="Upload", command=self.upload_encrypted_image)

        self.encrypt_button = tk.Button(
            root, text="Encrypt", command=self.encrypt)
        self.decrypt_button = tk.Button(
            root, text="Decrypt", command=self.decrypt)

        self.status_label = tk.Label(root, text="")
        self.status_label.grid(row=4, column=0, columnspan=2)

        # Place UI elements using grid
        self.main_img_label.grid(row=0, column=0)
        self.main_img_button.grid(row=0, column=1)

        self.hidden_img_label.grid(row=1, column=0)
        self.hidden_img_button.grid(row=1, column=1)

        self.encrypted_img_label.grid(row=2, column=0)
        self.encrypted_img_button.grid(row=2, column=1)

        self.encrypt_button.grid(row=3, column=0)
        self.decrypt_button.grid(row=3, column=1)

    def upload_main_image(self):
        self.main_img_path = filedialog.askopenfilename(
            title="Select MAIN Image")
        if self.main_img_path:
            self.main_img_button.config(text=f"Uploaded: {self.main_img_path}")

    def upload_hidden_image(self):
        self.hidden_img_path = filedialog.askopenfilename(
            title="Select HIDDEN Image")
        if self.hidden_img_path:
            self.hidden_img_button.config(
                text=f"Uploaded: {self.hidden_img_path}")

    def upload_encrypted_image(self):
        self.encrypted_img_path = filedialog.askopenfilename(
            title="Select ENCRYPTED Image to be decrypted")
        if self.encrypted_img_path:
            self.encrypted_img_button.config(
                text=f"Uploaded: {self.encrypted_img_path}")

    def encrypt(self):
        if self.main_img_path and self.hidden_img_path:
            save_path = filedialog.asksaveasfilename(
                title="Save Encrypted Image As", defaultextension=".png")
            if save_path:
                encrypt(self.main_img_path, self.hidden_img_path,
                        save_path, num_bits=3)
                self.status_label.config(
                    text=f"Encryption complete. Encrypted image saved at: {save_path}")
        else:
            self.status_label.config(
                text="Please select both MAIN and HIDDEN images for encryption.")

    def decrypt(self):
        if self.encrypted_img_path:
            save_path = filedialog.asksaveasfilename(
                title="Save Decrypted Image As", defaultextension=".png")
            if save_path:
                decrypt(self.encrypted_img_path, save_path, num_bits=3)
                self.status_label.config(
                    text=f"Decryption complete. Decrypted image saved at: {save_path}")
        else:
            self.status_label.config(
                text="Please select the ENCRYPTED image for decryption.")


def encrypt(main_img_path, hidden_img_path, encrypted_img_path, num_bits=2):
    # Open the images
    main_img = Image.open(main_img_path)
    hidden_img = Image.open(hidden_img_path)

    # Ensure the images have the same size
    if main_img.size != hidden_img.size:
        raise ValueError(
            "Main and hidden images must have the same dimensions.")

    # Convert images to RGB mode
    main_img = main_img.convert("RGB")
    hidden_img = hidden_img.convert("RGB")

    # Get the pixel arrays
    main_pixels = list(main_img.getdata())
    hidden_pixels = list(hidden_img.getdata())

    # Calculate mask for specified number of bits
    mask = (1 << num_bits) - 1

    # Encrypt by replacing the specified number of bits
    encrypted_pixels = [
        (
            (main_pixel[0] & ~mask) | (hidden_pixel[0] >> (8 - num_bits)),
            (main_pixel[1] & ~mask) | (hidden_pixel[1] >> (8 - num_bits)),
            (main_pixel[2] & ~mask) | (hidden_pixel[2] >> (8 - num_bits)),
        )
        for main_pixel, hidden_pixel in zip(main_pixels, hidden_pixels)
    ]

    # Create a new image with the encrypted pixels
    encrypted_img = Image.new("RGB", main_img.size)
    encrypted_img.putdata(encrypted_pixels)
    encrypted_img.save(encrypted_img_path)


def decrypt(encrypted_img_path, decrypted_img_path, num_bits=2):
    # Open the encrypted image
    encrypted_img = Image.open(encrypted_img_path)

    # Get the pixel array
    encrypted_pixels = list(encrypted_img.getdata())

    # Decrypt by extracting the specified number of bits
    decrypted_pixels = [
        (
            (pixel[0] & ((1 << num_bits) - 1)) << (8 - num_bits),
            (pixel[1] & ((1 << num_bits) - 1)) << (8 - num_bits),
            (pixel[2] & ((1 << num_bits) - 1)) << (8 - num_bits),
        )
        for pixel in encrypted_pixels
    ]

    # Create a new image with the decrypted pixels
    decrypted_img = Image.new("RGB", encrypted_img.size)
    decrypted_img.putdata(decrypted_pixels)
    decrypted_img.save(decrypted_img_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorDecryptorApp(root)
    root.mainloop()
