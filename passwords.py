import hashlib

def get_password_hash(password: str) -> str:
    sha = hashlib.sha256(password.encode('UTF-8'))
    return sha.hexdigest()

def validate_passwords(password: str) -> str:
    SpecialSym =['$', '@', '#', '%', '*']
     
    if len(password) < 7:
        return False
    if not any(char.isdigit() for char in password):
        return False    
    if not any(char.isupper() for char in password):
        return False    
    if not any(char.islower() for char in password):
        return False        
    if not any(char in SpecialSym for char in password):
        return False
    return True

print(validate_passwords("Passw0rd@"))