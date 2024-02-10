from PIL import Image


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


# Example usage
MAIN_IMG_PATH = "img/MAIN.jpg"
HIDDEN_IMG_PATH = "img/HIDDEN.jpg"
ENCRYPTED_IMG_PATH = "img/ENCRYPTED.png"
DECRYPTED_IMG_PATH = "img/DECRYPTED.png"

isEncrypted = False  # Set to True for encryption, False for decryption

if isEncrypted:
    # Encryption with 4 bits per channel (adjust as needed)
    encrypt(MAIN_IMG_PATH, HIDDEN_IMG_PATH, ENCRYPTED_IMG_PATH, num_bits=3)
    print("Encryption complete. Encrypted image saved at:", ENCRYPTED_IMG_PATH)
else:
    # Decryption with 4 bits per channel (should match the encryption setting)
    decrypt(ENCRYPTED_IMG_PATH, DECRYPTED_IMG_PATH, num_bits=3)
    print("Decryption complete. Decrypted image saved at:", DECRYPTED_IMG_PATH)
