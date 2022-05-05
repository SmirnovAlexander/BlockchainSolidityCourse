// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract CheerfulCat is ERC721URIStorage, VRFConsumerBaseV2 {

    uint256 public tokenCounter;

    uint64 s_subscriptionId;
    address vrfCoordinator;
    bytes32 s_keyHash;
    uint32 callbackGasLimit;
    uint16 requestConfirmations;
    uint32 numWords;

    constructor(
        uint64 _s_subscriptionId,
        address _vrfCoordinator,
        bytes32 _s_keyHash
    )
    VRFConsumerBaseV2(_vrfCoordinator)
    ERC721("CheerfulCat", "CHRFLCAT") {
        tokenCounter = 0;

        s_subscriptionId = _s_subscriptionId;
        vrfCoordinator = _vrfCoordinator;
        s_keyHash = _s_keyHash;
        callbackGasLimit = 40000;
        requestConfirmations = 3;
        numWords =  1;
    }

    function fulfillRandomWords(uint256 requestId , uint256[] memory randomWords) internal override {
    }


}
