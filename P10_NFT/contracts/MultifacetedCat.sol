// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract MultifacetedCat is ERC721URIStorage, VRFConsumerBaseV2 {

    enum CAT_TYPE {CHEERFUL, FAT, THOUGHTFUL}

    uint256 public tokenCounter;
    mapping(uint256 => CAT_TYPE) public tokenIdToType;
    mapping(uint256 => address) requestIdToSender;

    event requestedCat(uint256 requestId, address requester);
    event catAssigned(uint256 tokenId, CAT_TYPE cat_type);

    uint64 s_subscriptionId;
    VRFCoordinatorV2Interface vrfCoordinator;
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
    ERC721("MultifacetedCat", "MLTFCTDCAT") {
        tokenCounter = 0;

        s_subscriptionId = _s_subscriptionId;
        vrfCoordinator = VRFCoordinatorV2Interface(_vrfCoordinator);
        s_keyHash = _s_keyHash;
        callbackGasLimit = 1000000;
        requestConfirmations = 3;
        numWords =  1;
    }

    function createCat() public returns(bytes32) {

        uint256 requestId = vrfCoordinator.requestRandomWords(
            s_keyHash,
            s_subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
       );
       requestIdToSender[requestId] = msg.sender;
       emit requestedCat(requestId, msg.sender);
    }

    function fulfillRandomWords(uint256 requestId , uint256[] memory randomWords) internal override {
        // emit catAssigned(1, CAT_TYPE(randomWords[0] % 3));
        CAT_TYPE cat_type = CAT_TYPE(randomWords[0] % 3);
        tokenIdToType[tokenCounter] = cat_type;
        emit catAssigned(tokenCounter, cat_type);
        _safeMint(requestIdToSender[requestId], tokenCounter);
        tokenCounter += 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not owner or approved");
        _setTokenURI(tokenId, _tokenURI);
    }
}
