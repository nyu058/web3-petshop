import json
from web3 import Web3, HTTPProvider
import web3
from web3.contract import ConciseContract
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from time import localtime, strftime

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
    {'from': w3.eth.accounts[0]})

# Get tx receipt to get contract address
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']

# Contract instance in concise mode
contract_instance = w3.eth.contract(
    abi=abi, address=contract_address, ContractFactoryClass=ConciseContract)

# init blockchain with pet data using account[0]
with open("src/pets.json") as f:
    # load initial pets data into cache
    pets_data = json.load(f)
print("Initializing blockchain with pets data")
for pet in pets_data:
    contract_instance.addPet(pet['name'], pet['breed'], pet['age'], pet['location'], transact={
        "from": w3.eth.accounts[0]})
    pet['added_on'] = strftime("%Y-%m-%d %H:%M:%S", localtime())
    pet['adopted_on'] = 'N/A'
    pet['adopter'] = 'N/A'
    id = contract_instance.getPetsLen() - 1
    pet['id'] = id

stats = {}


def update_stats():
    adopted_count = len(contract_instance.getAllAdoptedPets())
    stats.update({
        "customer_count": len(set(contract_instance.getAdopters())),
        "adopted_count": adopted_count,
        "available_pets": len(pets_data) - adopted_count,
        "top_breed": get_top_breed()
    })


def get_top_breed():
    breed_count = {}
    for pet in pets_data:
        if pet.get('adopted'):
            if pet['breed'] not in breed_count:
                breed_count.setdefault(pet['breed'], 1)
            else:
                breed_count[pet['breed']] += 1
    if not breed_count:
        return "Unknown"
    return max(breed_count, key=breed_count.get)


update_stats()


def get_transactions_by_address(address):
    # slow
    result = []
    for i in range(0, w3.eth.get_block_number()+1):
        transactions = w3.eth.get_block(i)['transactions']
        for txn_hash in transactions:
            txn = w3.eth.get_transaction(txn_hash)
            if txn['from'] == address or txn['to'] == address:
                result.append({
                    "from": txn['from'],
                    "to": txn['to'],
                    "hash": txn['hash'].hex(),
                    "blockNumber": txn['blockNumber']
                })
    return result


app = Flask(__name__)


@app.route("/")
def index():
    # i use account[0] as the service account so we're not showing it here
    curr_account = request.args.get('account', w3.eth.accounts[1])

    return render_template('index.html', pets=pets_data, curr_account=curr_account, accounts=w3.eth.accounts[1:], **stats)


@app.route("/accounts/<account>")
def account(account):
    my_pets = contract_instance.getAdoptedPets(account)
    my_pet_lst = []
    for my_pet_id in my_pets:
        for pet in pets_data:
            if pet['id'] == my_pet_id:
                my_pet_lst.append(pet)
                break
    my_added_pets = contract_instance.getRegisteredPets(account)
    my_added_pets_lst = []
    for my_pet_id in my_added_pets:
        for pet in pets_data:
            if pet['id'] == my_pet_id:
                my_added_pets_lst.append(pet)
                break
    txns = get_transactions_by_address(account)
    return render_template("account.html", my_pets=my_pet_lst, my_added_pets=my_added_pets_lst, curr_account=account, transactions=txns)


@app.route("/pet", methods=['POST'])
def add_pet():
    age = int(request.form.get('age'))
    name = request.form.get('name')
    breed = request.form.get('breed')
    location = request.form.get('location')
    account = request.form.get('account')
    f = request.files['picture']
    filename = f"static/images/{secure_filename(f.filename)}"
    contract_instance.addPet(
        name, breed, age, location, transact={"from": account})
    pet = {
        "age": age, 
        "name": name, 
        "picture": filename,
        "location": location, 
        "breed": breed, 
        "id": contract_instance.getPetsLen() - 1, 
        'added_on': strftime("%Y-%m-%d %H:%M:%S", localtime()), 
        'adopted_on': 'N/A', 
        'adopter': 'N/A'
        }
    f.save(f"src/{filename}")
    # update cache and statistics
    pets_data.append(pet)
    update_stats()
    return redirect(url_for("index"))


@app.route("/adopt")
def adopt():
    id = int(request.args.get('id'))
    account = request.args.get('account')

    contract_instance.adopt(id, transact={"from": account})
    adopted = contract_instance.getAllAdoptedPets()
    # update cache and statistics
    for pet in pets_data:
        if pet['id'] in adopted:
            pet['adopted'] = True
            pet['adopted_on'] = strftime("%Y-%m-%d %H:%M:%S", localtime())
            pet['adopter'] = account
    update_stats()
    return redirect(url_for("index", account=account))


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0', use_reloader=False)
