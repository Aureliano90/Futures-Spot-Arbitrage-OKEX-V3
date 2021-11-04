class Key:

    def __init__(self, account=1):
        if account == 1:
            self.api_key = ""
            self.secret_key = ""
            self.passphrase = ""
        elif account == 2:
            self.api_key = ""
            self.secret_key = ""
            self.passphrase = ""
        else:
            print("账户不存在")
            exit()
