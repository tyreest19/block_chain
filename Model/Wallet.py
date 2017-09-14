import uuid

class Wallet:
    """Wallets containing blocks"""
    def __init__(self, wallet_name):
        self.private_key = str(uuid.uuid4())
        self.wallet_name = wallet_name
        self.blocks = []

    def send(self, block, wallets, wallet_name):
        for wallet in wallets:
            if wallet.wallet_name == wallet_name:
                wallet.blocks.append(block)
                self.blocks.remove(block)
        return {'From': self.wallet_name, 'To': wallet_name, 'Data:': block}

    def returnAsDict(self):
        return {
            "Private Key": self.private_key,
            "Wallet Name": self.wallet_name,
            "Blocks": self.blocks
        }

