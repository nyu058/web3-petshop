# ASP1050 Project -- PetShop.py
Author: **Qi Guo** <guoqi0909@gmail.com>

### Introduction
Hello! My name is Qi Guo and this is my submission for my final project for the course ASP1050.

For this project, I have taken the Pet Shop tutorial DApp as the base and have made some significant overhauls to it's backend for it to support all the features listed below. To simplify the development process I have rewrote the entire backend in Python with Flask and web3.py as it's the language I'm more comfortable with. 

Some highlights of this DApp include:
- Refactored `contracts/Adoption.sol` with new data structures and methods to support the new features
- Used in-memory caching for storing pet's data so less calls are made to the blockchain itself for faster performance
- New UI components made with Jquery and Bootstrap to support the new features
- Packaged everything into a docker container for easy setup & run
- 



### Features Implemented
1. Adding/registering pets (and their photos*) transferred from Marketplace or somewhere else
2. Keeping track of and publishing the most adopted (or most purchased) breed
3. Keeping track all pets the user has added to the shop with feature #1
4. Keeping track the time of when the pet has been added to the shop
5. Keeping track user account info and user account transaction history
6. Keeping track user account info and pets the user has adopted
7. Keeping track of a pet registry that keeps track of the owner of the pet as well as other details of the pet 
8. Keeping track of how many customers have been served and how many pets adopted

### Dependencies
Python Version: >= 3.6
Flask version: 2.1.1
web3.py version: 5.29
Solidity version: 8.3
Truffle version: 5.5.2
Ganache version: 7.0.1

### Run

To run the unit tests:
`truffle test`

#### Using Docker 
```
docker build -t petshop-python .
docker run -p 5001:5001 -it petshop-python
```
The UI can be accessed at http://localhost:5001/

#### From CLI
- make sure all the dependencies above are installed
- Ganache running on port 7545
- `truffle compile`
- `pip install -r requirement.txt` 
- `python src/app.py` 
