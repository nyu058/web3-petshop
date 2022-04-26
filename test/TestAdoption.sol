pragma solidity ^0.5.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/Adoption.sol";

contract TestAdoption {
    // The address of the adoption contract to be tested
    Adoption adoption = Adoption(DeployedAddresses.Adoption());

    // The id of the pet that will be used for testing
    uint256 expectedPetId = 0;

    // The expected owner of adopted pet is this contract
    address expectedAdopter = address(this);

    function testUserCanAddPet() public {
        adoption.addPet("Doge", "Shiba", 10, "Osaka, Japan");
        uint size = adoption.getPetsLen();
        Assert.equal(
            size,
            1,
            "Pet list size should be the same as what is returned"
        );

    }

    function testUserCanAdoptPet() public {
        uint256 returnedId = adoption.adopt(expectedPetId);

        Assert.equal(
            returnedId,
            expectedPetId,
            "Adoption of the expected pet ID should match what is returned."
        );
    }
}
