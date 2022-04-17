from brownie import accounts, config, network, exceptions
from brownie import Lottery
from scripts.deploy_lottery import deploy_lottery
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link, get_contract
from web3 import Web3
import pytest


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    entrance_fee = lottery.getEntranceFee()
    expected_entrance_fee = Web3.toWei(50 / 2500, "ether")
    # Assert
    assert expected_entrance_fee == entrance_fee, f"entrance fee is {entrance_fee / 1e18}, but should be {expected_entrance_fee / 1e18}"

def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": account, "value": entrance_fee})

def test_can_start_and_enter():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    # Act
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": entrance_fee})
    # Assert
    assert lottery.players(0) == account.address

def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": entrance_fee})
    # Act
    fund_with_link(lottery.address)
    lottery.endLottery({"from": account})
    # Assert
    assert lottery.returnState() == "CALCULATING_WINNER"

def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    # Arrange
    STATIC_RNG = 779
    lottery = deploy_lottery()
    lottery.startLottery({"from": get_account()})


    lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=3), "value": lottery.getEntranceFee()})
    n_players = lottery.getNumberOfPlayers()

    fund_with_link(lottery.address)

    starting_balance_of_account = get_account(index=STATIC_RNG%n_players).balance()
    balance_of_lottery = lottery.balance()

    tx = lottery.endLottery({"from": get_account()})
    request_id = tx.events["RequestedRandomness"]["requestId"]

    # Act
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": get_account()}
    )

    # Assert
    assert n_players == 4
    assert lottery.recentWinner() == get_account(index=STATIC_RNG%n_players)
    assert lottery.balance() == 0
    assert get_account(index=STATIC_RNG%n_players).balance() == starting_balance_of_account + balance_of_lottery
