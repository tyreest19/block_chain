class Ledger:

    def __init__(self, transcations):
       self.transactions = transcations

    def update(self, transcation):
        self.transactions.append(transcation)

    def viewAllTranscation(self):
        return self.transactions
