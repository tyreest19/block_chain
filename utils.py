import datetime as date
from flask import request
from Model import Block
from Model import Wallet

class WalletNotFoundError(Exception):
  """Error message that appears when a wallet does not exist"""


def create_genesis_block():
  """Creates the first block of the block chain"""
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block.Block(0, date.datetime.now(), {"from": "no one", "to":"tyree", "amount": 3, "proof-of-work": 1,
                                              "transactions": []}, "0")

def proof_of_work(last_proof):
  # Create a variable that we will use to find
  # our next proof of work
  incrementor = last_proof + 1
  # Keep incrementing the incrementor until
  # it's equal to a number divisible by 9
  # and the proof of work of the previous
  # block in the chain
  while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
    incrementor += 1
  # Once that number is found,
  # we can return it as a proof
  # of our work
  return incrementor

def next_block(last_block):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = "Hey! I'm block " + str(this_index)
  this_hash = last_block.hash
  return Block.Block(this_index, this_timestamp, this_data, this_hash)

def update_all_blocks(wallets, new_transcation):
  for wallet in wallets:
    for block in wallet.blocks:
      block.data['transactions'].append(new_transcation)
      block.hash_block()

def create_wallet(wallet_name):
  return Wallet.Wallet(wallet_name)

def find_wallet(name, wallets):
  for wallet in wallets:
    if wallet.wallet_name == name:
      return wallet
  raise WalletNotFoundError("The wallet name that you searched for does not exist!")
