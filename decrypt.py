import cv2, numpy as np, os

# -------- Utility Functions --------
bits_to_int = lambda bits: int("".join(str(b) for b in bits), 2)
bits_to_str = lambda bits: "".join(
    chr(int("".join(str(b) for b in bits[i:i+8]), 2)) for i in range(0, len(bits), 8)
)

# -------- Decryption Function --------
def decrypt():
    folder = r"F:\Python\testing"  # Change if needed
    img_path = os.path.join(folder, "encryptedpic.png")
    
    if not os.path.exists(img_path):
        print("Error: Encrypted image not found!")
        return
    
    image = cv2.imread(img_path)
    if image is None:
        print("Error: Failed to load encrypted image!")
        return
    
    flat = image.flatten()
    # Retrieve passcode length (first 16 bits)
    p_len = bits_to_int([flat[i] & 1 for i in range(16)])
    start = 16
    embedded_code = bits_to_str([flat[i] & 1 for i in range(start, start + p_len * 8)])
    start += p_len * 8
    # Retrieve secret message length (next 32 bits)
    s_len = bits_to_int([flat[i] & 1 for i in range(start, start + 32)])
    start += 32
    secret = bits_to_str([flat[i] & 1 for i in range(start, start + s_len * 8)])
    
    code = input("Enter passcode to decrypt: ")
    if code == embedded_code:
        print("Decrypted message:", secret)
    else:
        print("Error: Incorrect passcode!")

if __name__ == "__main__":
    decrypt()
