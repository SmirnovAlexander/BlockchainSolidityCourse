from brownie import accounts, config, network, exceptions
from brownie import Lottery
from scripts.deploy_lottery import deploy_lottery
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link, get_contract
from web3 import Web3
import time
import pytest




def test_can_pick_winner_correctly():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})

    lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})
    n_players = lottery.getNumberOfPlayers()

    fund_with_link(lottery.address)

    starting_balance_of_account = get_account().balance()
    balance_of_lottery = lottery.balance()

    lottery.endLottery({"from": get_account()})
    time.sleep(60)
    # request_id = tx.events["RequestedRandomness"]["requestId"]
    # STATIC_RNG = 779

    # Act
    assert lottery.recentWinner() == account.address
    assert lottery.balance() == 0
