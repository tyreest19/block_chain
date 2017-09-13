class Wallet:

    def __init__(self, private_key, public_address):
        self.private_key = private_key
        self.public_address = public_address
        self.coins = []

    def send(self, public_address):
        pass