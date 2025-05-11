from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)


def encrypt_data(data: int) -> str:
  data_str = str(data)
  encrypted_data = cipher_suite.encrypt(data_str.encode())
  return encrypted_data.decode()


def decrypt_data(encrypted_data: str) -> int:
  decrypted_data = cipher_suite.decrypt(encrypted_data.encode()).decode()
  return int(decrypted_data)
