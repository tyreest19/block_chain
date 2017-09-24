import datetime as date
import hashlib as hasher
import json
import utils
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from Model import Block
from Model import Ledger
from Model import Wallet

node = Flask(__name__, template_folder='View', static_folder='View')

# Store the transactions that
# this node has in a list
transactions = Ledger.Ledger([])

# Create the blockchain and add the genesis block
wallets = [] # Collections of all wallets
blockchain = [] # Collection of all coins
blockchain.append(utils.create_genesis_block())
previous_block = blockchain[0]
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

@node.route('/')
def home():
    return render_template('index.html')
@node.route('/transaction', methods=['GET', 'POST'])
def transaction():
    """Sends 1 block of data to reliever. Then redirects to receivers page."""
    if request.method == 'POST':
        sender_wallet_name = request.form['sender_name']
        receiver_wallet_name = request.form['receiver_name']
        sender_wallet = utils.find_wallet(sender_wallet_name, wallets)
        recorded_transaction = sender_wallet.send(wallets, receiver_wallet_name)
        utils.update_all_blocks(wallets, recorded_transaction)
        return redirect('/view-wallet/' + receiver_wallet_name)
    return render_template("transaction.html")


@node.route('/mine', methods=['GET', 'Post'])
def mine():
    """Mines for block and appends it to users wallet."""
    if request.method == 'POST':
        # Get the last proof of work
        last_block = blockchain[len(blockchain) - 1]
        last_proof = last_block.data['proof-of-work']
        print(last_proof)
        # Find the proof of work for
        # the current block being mined
        # Note: The program will hang here until a new
        #       proof of work is found
        proof = utils.proof_of_work(last_proof)
        # Once we find a valid proof of work,
        # we know we can mine a block so
        # we reward the miner by adding a transaction
        # Now we can gather the data needed
        # to create the new block
        new_block_data = {
            "proof-of-work": proof,
            "transactions": transactions.viewAllTranscation(),
            "amount": 1
        }
        new_block_index = last_block.index + 1
        new_block_timestamp = this_timestamp = str(date.datetime.now())
        last_block_hash = last_block.hash
        # Now create the
        # new block!
        mined_block = Block.Block(
            new_block_index,
            new_block_timestamp,
            new_block_data,
            last_block_hash,
        )
        wallet_name = request.form['wallet_name']
        wallet = utils.find_wallet(wallet_name, wallets)
        wallet.receive(mined_block, miner_address)
        blockchain.append(mined_block)
        mined_transactions = {"from": "network", "to": miner_address, "Data": mined_block.returnAsDict()}
        transactions.update(mined_transactions)
        utils.update_all_blocks(wallets, mined_transactions)
        # Let the client know we mined a block
        return redirect('/view-wallet/' + wallet_name)
    return render_template('mine.html')


@node.route('/blocks', methods=['GET'])
def get_blocks():
    """Returns all blockschain as a string"""
    return str(blockchain)

@node.route('/create-wallet', methods=['GET', 'POST'])
def create_wallet():
    """Page which allows users to create a wallet"""
    if request.method == 'POST':
        wallet_name = request.form['wallet_name']
        new_wallet = utils.create_wallet(wallet_name)
        wallets.append(new_wallet)
        return redirect('/view-wallet/' + new_wallet.wallet_name)
    return render_template('create_wallet.html')

@node.route('/view-wallet/<wallet_name>')
def view_wallet(wallet_name):
    """Url to view any wallet in the system."""
    for wallet in wallets:
        if wallet_name in wallet.wallet_name:
            return render_template('view_wallet.html', wallet_name=wallet.wallet_name, private_key=wallet.private_key,
                                   blocks=wallet.blocks)
    raise utils.WalletNotFoundError("You attempted to view a wallet that does not exist!")

if __name__ == "__main__":
    node.run(debug=True)
