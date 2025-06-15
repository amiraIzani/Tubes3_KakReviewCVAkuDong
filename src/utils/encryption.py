import os
import base64
from dotenv import load_dotenv

# Load environment variables to get the secret key
load_dotenv()

# Fetch the secret key from environment variables.
SECRET_KEY = os.getenv('ATS_ENCRYPTION_KEY', 'default_super_secret_key_that_is_long')

def _vigenere(text: str, key: str, encrypt: bool = True) -> str:
    """Internal function to perform Vigenère encryption or decryption."""
    processed_text = ""
    key_index = 0
    key_len = len(key)
    for char in text:
        char_code = ord(char)
        key_char_code = ord(key[key_index % key_len])
        if encrypt:
            encrypted_code = (char_code + key_char_code) % 256
            processed_text += chr(encrypted_code)
        else:
            decrypted_code = (char_code - key_char_code + 256) % 256
            processed_text += chr(decrypted_code)
        key_index += 1
    return processed_text

def encrypt(plaintext: any) -> str | None:
    """
    Encrypts a plaintext string. If the input is not a string, it returns it
    as-is without causing an error.
    """
    # --- FIX: More robust type checking ---
    # Only attempt to encrypt if the input is a non-empty string.
    if not isinstance(plaintext, str) or not plaintext:
        # This will handle None, empty strings, lists, numbers, etc. gracefully.
        return plaintext

    try:
        encrypted_text = _vigenere(plaintext, SECRET_KEY, encrypt=True)
        encrypted_bytes = encrypted_text.encode('utf-8', 'surrogatepass')
        base64_bytes = base64.b64encode(encrypted_bytes)
        base64_string = base64_bytes.decode('utf-8')
        return base64_string
    except Exception as e:
        # Added a debug print to see what data caused the failure.
        print(f"[Cipher] Encryption failed for value '{plaintext}' of type {type(plaintext)}: {e}")
        return plaintext # Return original text on failure

def decrypt(ciphertext: any) -> str | None:
    """
    Decrypts a ciphertext string. If the input is not a string, it returns it
    as-is without causing an error.
    """
    # --- FIX: More robust type checking ---
    if not isinstance(ciphertext, str) or not ciphertext:
        return ciphertext

    try:
        base64_bytes = ciphertext.encode('utf-8')
        encrypted_bytes = base64.b64decode(base64_bytes)
        encrypted_text = encrypted_bytes.decode('utf-8', 'surrogatepass')
        decrypted_text = _vigenere(encrypted_text, SECRET_KEY, encrypt=False)
        return decrypted_text
    except Exception:
        # If decryption fails (e.g., it was never encrypted), return the original text.
        # This prevents crashes if you have mixed encrypted/unencrypted data.
        return ciphertext
