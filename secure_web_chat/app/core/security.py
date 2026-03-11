from passlib.context import CryptContext

# ハッシュ化の設定 (bcryptアルゴリズムを使用)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """ パスワードをハッシュ化する """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ 入力されたパスワードと保存されているハッシュを照合する """
    return pwd_context.verify(plain_password, hashed_password)