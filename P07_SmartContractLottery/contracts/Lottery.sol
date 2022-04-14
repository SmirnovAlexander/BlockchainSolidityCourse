// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// Get the latest ETH/USD price from chainlink price feed
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./Utils.sol";

contract Lottery is Ownable {

    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lotteryState;

    constructor(address _ethUsdPriceFeedAddress) {
        usdEntryFee = 50;
        ethUsdPriceFeed = AggregatorV3Interface(_ethUsdPriceFeedAddress);
        lotteryState = LOTTERY_STATE.CLOSED;
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
        lotteryState == LOTTERY_STATE.OPEN;
    }
    function endLottery() public {}

    function returnState() public view returns (string memory) {
        if (lotteryState == LOTTERY_STATE.OPEN) return "OPEN";
        if (lotteryState == LOTTERY_STATE.CLOSED) return "CLOSE";
        if (lotteryState == LOTTERY_STATE.CALCULATING_WINNER) return "CALCULATING_WINNER";
        return "";
    }
}
