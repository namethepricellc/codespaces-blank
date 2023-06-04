from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
import requests
import json
import time

# Define the web3 provider
w3 = Web3(Web3.HTTPProvider('https://rpc-mainnet.maticvigil.com/'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

# Define the contract address and ABI
contract_address = "<CONTRACT_ADDRESS>"
contract_abi = json.loads("<CONTRACT_ABI>")

# Define the account
private_key = "<PRIVATE_KEY>"
account = Account.from_key(private_key)

# Define the minimum profit
minimum_profit = 0.01

# Define the gas limit
gas_limit = 1000000

# Define the gas price
min_gas_price = 1
max_gas_price = 100

# Define the function to calculate the gas cost

def calculate_gas_cost(gas_price, gas_used):
    return gas_price * gas_used

# Define the function to check if a transaction is profitable

def is_profitable(tx):
    # Get the transaction details
    tx_details = w3.eth.getTransaction(tx)
    # Get the transaction receipt
    tx_receipt = w3.eth.getTransactionReceipt(tx)
    # Get the gas used
    gas_used = tx_receipt['gasUsed']
    # Get the gas price
    gas_price = tx_details['gasPrice']
    # Calculate the gas cost
    gas_cost = calculate_gas_cost(gas_price, gas_used)
    # Get the value of the transaction
    value = tx_details['value']
    # Calculate the profit
    profit = value - gas_cost
    # Check if the profit is greater than the minimum profit
    if profit > minimum_profit:
        return True
    else:
        return False

# Define the function to perform the sandwich attack

def perform_sandwich_attack(tx):
    # Get the transaction details
    tx_details = w3.eth.getTransaction(tx)
    # Get the target address
    target = tx_details['to']
    # Get the data
    data = tx_details['input']
    # Encode the target and data parameters
    params = abi.encode(target, data)
    # Define the contract instance
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    # Call the sandwichAttack function
    tx_hash = contract.functions.sandwichAttack(target, params).transact({
        'from': account.address,
        'gas': gas_limit,
        'gasPrice': w3.toWei(min_gas_price, 'gwei')
    })
    # Wait for the transaction to be mined
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # Get the gas used
    gas_used = tx_receipt['gasUsed']
    # Get the gas price
    gas_price = tx_receipt['gasPrice']
    # Calculate the gas cost
    gas_cost = calculate_gas_cost(gas_price, gas_used)
    # Get the value of the transaction
    value = tx_details['value']
    # Calculate the profit
    profit = value - gas_cost
    # Print the profit
    print(f"Profit: {profit}")

# Define the function to scan the mempool

def scan_mempool():
    # Get the current block number
    current_block = w3.eth.blockNumber
    # Define the URL for the Mempool API
    url = f"https://api.polygonscan.com/v1/transactions/pending?module=proxy&action=eth_getBlockByNumber&tag={hex(current_block)}&apikey=<API_KEY>"
    # Make the API request
    response = requests.get(url)
    # Parse the response
    data = response.json()
    # Get the transactions
    transactions = data['result']['transactions']
    # Loop through the transactions
    for tx in transactions:
        # Check if the transaction is profitable
        if is_profitable(tx['hash']):
            # Perform the sandwich attack
            perform_sandwich_attack(tx['hash'])

# Define the main function

def main():
    # Loop forever
    while True:
        # Scan the mempool
        scan_mempool()
        # Wait for 10 seconds
        time.sleep(10)

if __name__ == '__main__':
    main()