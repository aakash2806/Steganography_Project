import cv2, numpy as np, os

# -------- Utility Functions --------
int_to_bits = lambda num, l: [int(b) for b in format(num, f'0{l}b')]
str_to_bits = lambda s: [int(b) for char in s for b in format(ord(char), '08b')]

def embed_data(img, data_bits):
    flat = img.flatten()
    if len(data_bits) > len(flat):
        raise ValueError("Data too large to embed!")
    for i, bit in enumerate(data_bits):
        flat[i] = (flat[i] & 254) | bit
    return flat.reshape(img.shape)

# -------- Encryption Function --------
def encrypt():
    folder = r"F:\Python\testing"  # Change if needed
    img_path = os.path.join(folder, "mypic.jpg")
    
    if not os.path.exists(img_path):
        print("Error: Input image not found!")
        return
    
    image = cv2.imread(img_path)
    if image is None:
        print("Error: Failed to load image!")
        return
    
    secret = input("Enter secret message: ")
    code = input("Enter passcode: ")
    if not secret or not code:
        print("Error: Secret message and passcode are required!")
        return

    # Create header: [16 bits for code length] + [code] + [32 bits for message length] + [secret]
    header = (
        int_to_bits(len(code), 16) +
        str_to_bits(code) +
        int_to_bits(len(secret), 32) +
        str_to_bits(secret)
    )
    
    try:
        encoded = embed_data(image, header)
    except ValueError as e:
        print("Error:", e)
        return
    
    output_path = os.path.join(folder, "encryptedpic.png")
    cv2.imwrite(output_path, encoded)
    print("Encryption complete! Output saved to:", output_path)

if __name__ == "__main__":
    encrypt()
