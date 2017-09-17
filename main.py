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

node = Flask(__name__, template_folder='View', static_folder='View')

# Store the transactions that
# this node has in a list
transactions = Ledger.Ledger([])

# Create the blockchain and add the genesis block
wallets = []
blockchain = []
blockchain.append(utils.create_genesis_block())
previous_block = blockchain[0]
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"


@node.route('/transcation', methods=['POST'])
def transaction():
    if request.method == 'POST':
        # On each new POST request,
        # we extract the transaction data
        new_transation = request.get_json()
        # Then we add the transaction to our list
        transactions.update(new_transation)
        # Because the transaction was successfully
        # submitted, we log it to our console
        utils.update_all_blocks(wallets, new_transation)
        print("New transaction")
        print("FROM: {}".format(new_transation['from']))
        print("TO: {}".format(new_transation['to']))
        print("AMOUNT: {}\n".format(new_transation['amount']))
        # Then we let the client know it worked out
        return "Transaction submission successful\n"


# ...blockchain
# ...Block class definition

@node.route('/mine', methods=['GET', 'Post'])
def mine():
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
    chain_to_send = blockchain
    # Convert our blocks into dictionaries
    # so we can send them as json objects later
    for i in range(0, len(chain_to_send)):
        block_index = str(chain_to_send[i].index)
        block_timestamp = str(chain_to_send[i].timestamp)
        block_data = str(chain_to_send[i].data)
        block_hash = chain_to_send[i].hash
        chain_to_send[i] = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
        }
    # Send our chain to whomever requested it
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send


@node.route('/create-wallet', methods=['GET', 'POST'])
def create_wallet():
    if request.method == 'POST':
        wallet_name = request.form['wallet_name']
        new_wallet = utils.create_wallet(wallet_name)
        wallets.append(new_wallet)
        return redirect('/view-wallet/' + new_wallet.wallet_name)
    return render_template('create_wallet.html')


@node.route('/view-wallet/<wallet_name>')
def view_wallet(wallet_name):
    for wallet in wallets:
        if wallet_name in wallet.wallet_name:
            return render_template('view_wallet.html', wallet_name=wallet.wallet_name, private_key=wallet.private_key,
                                   blocks=wallet.blocks)
    return "Could not locate your wallet"


if __name__ == "__main__":
    node.run(debug=True)
