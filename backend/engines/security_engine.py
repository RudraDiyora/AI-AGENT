import bcrypt


class SECURITY_ENGINE:
    def __init__(self):
        self.securityVersion = "bcrypt-hash"
    # password handling
    def hashPassword(self, password: str) -> str:
        # convert the raw password into its bytes
        password_bytes = password.encode('utf-8')

        # generate the hash
        hashed_password = bcrypt.hashpw(password_bytes,  bcrypt.gensalt())

        # covert the hashedpassword(bytes) back into a string
        return hashed_password.decode('utf-8')
    def verifyPassword(self, raw_password, hashed_password) -> bool:
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    