from cryptography.fernet import Fernet

class ChatCipher:
    def __init__(self, key):
        self.cipher = Fernet(key)

    def encrypt_msg(self, message: str) -> bytes:
        return self.cipher.encrypt(message.encode("utf-8"))
    
    def decrypt_msg(self, encrypted_data: bytes) -> str:
        return self.cipher.decrypt(encrypted_data).decode("utf-8")
