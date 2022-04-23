from scripts.utils import get_account
from brownie import interface, config, network

def wrap_coin(value=0.01*1e18):
    account = get_account()
    token = interface.IWrappedCoin(config["networks"][network.show_active()]["coin"])
    tx = token.deposit({"from": account, "value": value})
    tx.wait(1)
    balance = token.balanceOf(account.address) / 1e18
    print(f"Received {value / 1e18} {token.name()} on account. Total amount on account: {balance}")

def main():
    wrap_coin()
