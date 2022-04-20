import json
from sqlite3 import adapt
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename


# compile your smart contract with truffle first
truffleFile = json.load(open('./build/contracts/Adoption.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# web3.py instance
w3 = Web3(HTTPProvider("http://localhost:7545/"))


# Instantiate and deploy contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get transaction hash from deployed contract
tx_hash = contract.constructor().transact(
    {'from': w3.eth.accounts[0], 'gas': 410000})

# Get tx receipt to get contract address
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']

# Contract instance in concise mode
contract_instance = w3.eth.contract(
    abi=abi, address=contract_address, ContractFactoryClass=ConciseContract)

with open("src/pets.json") as f:
    pets_data = json.load(f)


def get_new_id(pets):
    return sorted([e['id'] for e in pets], reverse=True)[0]+1


app = Flask(__name__)


@app.route("/")
def index():

    adopted = contract_instance.getAdoptedPets()
    for pet in pets_data:
        if pet['id'] in adopted:
            pet['adopted'] = True

    return render_template('index.html', pets=pets_data)


@app.route("/pet", methods=['POST'])
def add_pet():
    age = int(request.form.get('age'))
    name = request.form.get('name')
    breed = request.form.get('breed')
    location = request.form.get('location')
    f = request.files['picture']
    filename = f"static/images/{secure_filename(f.filename)}"
    id = get_new_id(pets_data)
    pet = {"age": age, "name": name, "picture": filename,
           "location": location, "breed": breed, "id": id}
    f.save(f"src/{filename}")
    pets_data.append(pet)
    return redirect(url_for("index"))


@app.route("/adopt")
def adopt():
    id = int(request.args.get('id'))
    account = w3.eth.accounts[0]

    contract_instance.adopt(id, transact={"from": account})
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
