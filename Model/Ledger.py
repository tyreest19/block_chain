class Ledger:
    """Contains all the transcations and creation of new blocks"""
    def __init__(self, transcations):
       self.transactions = transcations

    def update(self, transcation):
        self.transactions.append(transcation)

    def viewAllTranscation(self):
        return self.transactions
