pragma solidity ^0.5.0;
// pragma experimental ABIEncoderV2;

contract Adoption {
    struct Pet{
      string name;
      string breed;
      uint256 age;
      string location;
    }
    mapping(address => uint256[]) public adoptions;
    mapping(address => uint256[]) public registrations;
    address[] public adoptors;
    Pet[] public allPets;
    uint256[] public adoptedPetIds;
    // Adopting a pet
    function adopt(uint256 petId) public returns (uint256) {
        require(petId >= 0 && petId < allPets.length);
        adoptedPetIds.push(petId);
        adoptions[msg.sender].push(petId);
        return petId;
    }

    function addPet(string memory name, string memory breed, uint256 age, string memory location) public {
      Pet memory pet = Pet(name, breed, age, location);
      registrations[msg.sender].push(allPets.push(pet) - 1);
    }
    function getPetsLen() public view returns (uint256) {
      return allPets.length;
    }
    // function getAllPets() public view returns (Pet[] memory) {
    //   return allPets;
    // }

    // Retrieving the adopters
    function getAdopters() public view returns (address[] memory) {
        return adoptors;
    }
    // Retrieving the adopted pets
    function getAllAdoptedPets() public view returns (uint256[] memory) {
        return adoptedPetIds;
    }
    // Retrieving the adopted pets of a given account
    function getAdoptedPets(address account) public view returns (uint256[] memory) {
        return adoptions[account];
    }
    // Retrieving the pets added by a given account
    function getRegisteredPets(address account) public view returns (uint256[] memory) {
        return registrations[account];
    }
}
