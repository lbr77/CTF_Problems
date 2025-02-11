print("""Problem: you need to write a contract to make the CheckContract.result = true.""")
from web3 import Web3
from solcx import compile_source,set_solc_version
set_solc_version("0.8.27")
# install_solc("0.8.0")
# print("Installed solc 0.8.0")
from json import loads
import os
import subprocess
print('Launching anvil...')
anvil = subprocess.Popen("anvil",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
net = Web3(Web3.HTTPProvider("http://localhost:8545"))
# private_key = os.getenv("PRIVATE_KEY")
private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
account = net.eth.account.from_key(private_key)

def deploy(bytecode,abi):
    contract = net.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact({'from': account.address})
    tx_receipt = net.eth.wait_for_transaction_receipt(tx_hash)
    return net.eth.contract(
address=tx_receipt.contractAddress,
abi=abi,
    )
def deploy_compiled(file,contract):
    compiled = loads(open(f"out/{file}/{contract}.json").read())
    return deploy(compiled["bytecode"]["object"],compiled["abi"])


dex = deploy_compiled("DEX.sol","SimpleDEX")
print("Enter the source code of your attack contract(end with EOF):")
source_code = ""
while True:
    line = input()
    if line == "EOF":
        break
    source_code += line + "\n"


attack = compile_source(source_code,output_values=["abi","bin"])["<stdin>:AttackContract"]
attack = deploy(attack["bin"],attack["abi"])
print("attack deployed at",attack.address)

deploy_script = deploy_compiled("Check.sol","CheckRun")
print("Running the attack...")
tx_hash = deploy_script.functions.run(dex.address,attack.address).transact({'from': account.address})
tx_receipt = net.eth.wait_for_transaction_receipt(tx_hash)
print("Attack completed!")
result = deploy_script.functions.result().call()
anvil.terminate()
if result:
    print("You won! Here's your flag:",os.getenv("FLAG")) 
else:
    print("You lost! Try again!")
exit()