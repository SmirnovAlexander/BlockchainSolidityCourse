from brownie import accounts, config, network
from brownie import Lottery
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account}
    )
    entrance_fee = lottery.getEntranceFee()
    assert entrance_fee > Web3.toWei(0.01, "ether"), f"entrance fee is {entrance_fee}"
    assert entrance_fee < Web3.toWei(0.02, "ether"), f"entrance fee is {entrance_fee}"
