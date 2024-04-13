import hashlib

class UserIDRequired(Exception):
    pass

class UserIDTaken(Exception):
    pass

class UserNameRequired(Exception):
    pass

class PasswordRequired(Exception):
    pass

class PasswordTooWeak(Exception):
    pass


class User:
    def __init__(self, user_values: tuple):
        self.user_id = user_values[0]
        self.username = user_values[1]
        self.password = user_values[2]
        
    def validate_info(user_id: int, username: str, user_password: str):
        if not user_id:
            raise UserIDRequired
        if not username:
            raise UserNameRequired
        if not user_password:
            raise PasswordRequired
        if not User.validate_passwords(user_password):
            raise PasswordTooWeak

        return (user_id, username, User.get_password_hash(user_password))
    
    def values(self):
        return (self.user_id, self.username, self.password)

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
        