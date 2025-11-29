import hashlib

def hash_password(password: str) -> str:
<<<<<<< HEAD
    """
    Genera un hash SHA-256 en formato hex (igual que el que tienes en la tabla admins).
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Compara la contraseña en texto plano contra el hash guardado en la BD.
    """
    return hash_password(password) == stored_hash
=======

    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:

    return pwd_context.verify(password, hashed)
>>>>>>> origin/dev
