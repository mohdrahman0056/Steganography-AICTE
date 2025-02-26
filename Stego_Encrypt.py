import cv2
import os
import numpy as np
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Load the image
img = cv2.imread("mypic.jpg")  # Replace with the correct image path
height, width, _ = img.shape

msg = input("Enter secret message: ")
password = input("Enter a passcode to encrypt: ")

# Generate a 256-bit key from password
key = hashlib.sha256(password.encode()).digest()

# Encrypt the message using AES
cipher = AES.new(key, AES.MODE_CBC)  # Using CBC mode
iv = cipher.iv  # Initialization vector (IV) must be stored for decryption
ciphertext = cipher.encrypt(pad(msg.encode(), AES.block_size))  # Encrypt and pad the message

# Store message length in the first pixel's blue channel
msg_len = len(ciphertext)
img[0, 0, 0] = msg_len

n, m = 0, 1  # Start from (0,1) to avoid overwriting length

# Embed encrypted message into the blue channel of the image
for byte in ciphertext:
    img[n, m, 0] = byte  # Store encrypted bytes in the blue channel

    # Move through pixels safely
    if m + 1 < width:
        m += 1
    elif n + 1 < height:
        n += 1
        m = 0
    else:
        print("Error: Message too long for image.")
        break

# Save the IV separately for decryption
with open("password_list.txt", "wb") as f:
    f.write(iv)

# Save the encrypted image
cv2.imwrite("encryptedImage.png", img)  # Use PNG to prevent compression loss
os.system("start encryptedImage.png")  # Open the encrypted image (Windows)

print("Encryption complete! Encrypted image saved as 'encryptedImage.png'.")
