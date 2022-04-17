// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// Get the latest ETH/USD price from chainlink price feed
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./Utils.sol";

contract Lottery is VRFConsumerBase, Ownable {

    address payable[] public players;
    address payable public recentWinner;
    uint256 public randomness;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lotteryState;
    uint256 public fee;
    bytes32 internal keyHash;
    event RequestedRandomness(bytes32 requestId);

    constructor(
        address _ethUsdPriceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50;
        ethUsdPriceFeed = AggregatorV3Interface(_ethUsdPriceFeedAddress);
        lotteryState = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }

    function enter() public payable {
        require(lotteryState == LOTTERY_STATE.OPEN, Utils.cat("Lottery state is not OPEN! It is ", returnState()));
        uint256 entranceFee = getEntranceFee();
        require(
            msg.value >= entranceFee,
            Utils.cat("Not enougth ETH! Minimum value is ", Strings.toString(entranceFee))
        );
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns (uint256) {
        (,int256 price,,,) = ethUsdPriceFeed.latestRoundData();
        uint256 priceAdjusted = uint256(price) * 10**10; // priceAdjusted = USD * 10**18
        // ether_needed = entry_fee / usd_per_ether 
        // wei_needed = (entry_fee / usd_per_ether) * 10**18
        // wei_needed = (entry_fee * 10**18 / usd_per_ether * 10**18) * 10**18
        // wei_needed = (entry_fee * 10**36 / usd_per_ether * 10**18)
        uint256 costToEnter = (usdEntryFee * 10**36) / priceAdjusted;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lotteryState == LOTTERY_STATE.CLOSED,
            Utils.cat("Can't start a new lottery! Lottery state is ", returnState())
        );
        lotteryState = LOTTERY_STATE.OPEN;
    }

    function endLottery() public {

        // uint256 randomNumber = uint256(
        //     keccak256(
        //         abi.encodePacked(
        //             msg.sender,
        //             block.number,
        //             block.difficulty,
        //             block.timestamp
        //         )
        //     )
        // ) % players.length;
        lotteryState = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyHash, fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lotteryState == LOTTERY_STATE.CALCULATING_WINNER,
            Utils.cat("Lottery state is not CALCULATING_WINNER! It is ", returnState())
        );
        require(
            _randomness > 0,
            Utils.cat("Randomness not found! It is ", Strings.toString(_randomness))
        );
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);

        // reset
        players = new address payable[](0);
        lotteryState = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }

    function getNumberOfPlayers() public view returns(uint count) {
        return players.length;
    }

    function returnState() public view returns (string memory) {
        if (lotteryState == LOTTERY_STATE.OPEN) return "OPEN";
        if (lotteryState == LOTTERY_STATE.CLOSED) return "CLOSED";
        if (lotteryState == LOTTERY_STATE.CALCULATING_WINNER) return "CALCULATING_WINNER";
        return "";
    }
}
