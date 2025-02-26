import cv2
import os
import numpy as np
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Load the encrypted image
img = cv2.imread("encryptedImage.png")  # Ensure this is the correct path
height, width, _ = img.shape

# Read the IV from the saved file
if not os.path.exists("password_list.txt"):
    print("Error: 'password_list.txt' not found. Please run the encryption script first.")
    exit()

with open("password_list.txt", "rb") as f:
    iv = f.read()

# Ask for the password to decrypt
password = input("Enter passcode for Decryption: ")

# Generate a 256-bit key from the password
key = hashlib.sha256(password.encode()).digest()

# Retrieve message length from the first pixel (convert to int)
msg_len = int(img[0, 0, 0])

n, m = 0, 1  # Start from (0,1) to match encryption
ciphertext = bytearray()

# Extract the encrypted message from the blue channel
for _ in range(msg_len):
    ciphertext.append(int(img[n, m, 0]))  # Convert pixel value to integer

    # Move through pixels safely
    if m + 1 < width:
        m += 1
    elif n + 1 < height:
        n += 1
        m = 0
    else:
        print("Error: Reached image boundary unexpectedly.")
        break

# Decrypt the message using AES
try:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_msg = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

    print("Decryption successful! Message:", decrypted_msg)

except ValueError:
    print("Decryption failed: Incorrect password or corrupted data.")
