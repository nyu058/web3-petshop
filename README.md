# web3-PetShop

### Introduction
An enhanced python implementation of Dapp https://trufflesuite.com/guides/pet-shop/

### Run
#### Tests

To run the unit tests:
`truffle test`

#### Using Docker 
```
docker build -t petshop-python .
docker run -p 5001:5001 -d petshop-python
```
The UI can be accessed at http://localhost:5001/

#### Dependencies
```
Python Version: >= 3.6
Flask version: 2.1.1
web3.py version: 5.29
Solidity version: 8.3
Truffle version: 5.5.2
Ganache version: 7.0.1
```

#### From CLI
- make sure all the dependencies above are installed
- Ganache running on port 7545
- `truffle compile`
- `python src/app.py` 
