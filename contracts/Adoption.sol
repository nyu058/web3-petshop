pragma solidity ^0.5.0;

contract Adoption {
    mapping(address => uint256[]) public adoptions;
    address[] public adoptors;
    uint256[] public adoptedIds;
    // Adopting a pet
    function adopt(uint256 petId) public returns (uint256) {
        require(petId >= 0);

        adoptions[msg.sender].push(petId);
        adoptors.push(msg.sender);
        adoptedIds.push(petId);
        return petId;
    }

    // Retrieving the adopters
    function getAdopters() public view returns (address[] memory) {
        return adoptors;
    }
    // Retrieving the adopted pets
    function getAdoptedPets() public view returns (uint256[] memory) {
        return adoptedIds;
    }
}
