class Wallet:
    """Wallets containing blocks"""
    def __init__(self, private_key, public_address):
        self.private_key = private_key
        self.public_address = public_address
        self.blocks = []

    def send(self, block, wallets, public_address):
        for wallet in wallets:
            if wallet.public_address == public_address:
                wallet.blocks.append(block)
                self.blocks.remove(block)
        return {'From': self.public_address, 'To': public_address, 'Data:': block}

