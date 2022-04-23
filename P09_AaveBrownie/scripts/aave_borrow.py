from scripts.utils import get_account, LOCAL_ENVIRONMENTS
from brownie import config, network, interface
from scripts.wrap_coin import wrap_coin 
import time

LEND_AMOUNT = 0.01 * 1e18

def lend():
    account = get_account()

    # Initializing
    weth_gateway = interface.IWETHGateway(config["networks"][network.show_active()]["weth_gateway"])
    weth_address = weth_gateway.getWETHAddress()
    aave_weth_address = config["networks"][network.show_active()]["aave_weth_address"]
    pool = get_lending_pool()

    print_state(pool, account, weth_address, aave_weth_address)

    # Deposit
    deposit_eth(pool, weth_gateway, LEND_AMOUNT, account)
    print_state(pool, account, weth_address, aave_weth_address)

    # Withdraw
    # withdraw_eth_to_wrapped(pool, weth_address, account, LEND_AMOUNT)
    withdraw_eth_to_wrapped(pool, weth_address, account)
    withdraw_wrapped_to_native(weth_address, LEND_AMOUNT, account)
    print_state(pool, account, weth_address, aave_weth_address)


def print_state(pool, account, weth_address, aave_weth_address):
    print("---------------------------")
    print(f"Native token amount: {account.balance() / 1e18}")
    _ = get_wrapped_balance(weth_address, account)
    _ = get_wrapped_balance(aave_weth_address, account)
    available_borrow, total_debt = get_borrowable_data(pool, account)
    print("---------------------------")

def deposit_eth(pool, weth_gateway, amount, account):
    print(f"Depositing {amount / 1e18} native token to pool...")
    tx = weth_gateway.depositETH(pool, account.address, 0, {"from": account, "value": amount})
    tx.wait(1)

def withdraw_eth_to_wrapped(pool, weth_address, account, amount=None):
    print(f"Withdrawing {amount / 1e18} native token from pool...")
    tx = pool.withdraw(weth_address, amount, account.address, {"from": account.address})
    tx.wait(1)

def get_borrowable_data(pool, account):
    (
        total_collateral,
        total_debt,
        available_borrow,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = pool.getUserAccountData(account.address)
    print(f"Deposited: {total_collateral}")
    print(f"Borrowed: {total_debt}")
    print(f"May borrow: {available_borrow}")
    return available_borrow, total_debt

def get_wrapped_balance(address, account):
    wrapped_coin = interface.IWrappedCoin(address)
    balance = wrapped_coin.balanceOf(account.address)
    print(f"{wrapped_coin.name()} amount: {balance / 1e18}")
    return balance

def withdraw_wrapped_to_native(address, amount, account):
    wrapped_coin = interface.IWrappedCoin(address)
    print(f"Withdrawing {amount / 1e18} {wrapped_coin.name} to account")
    tx = wrapped_coin.withdraw(amount, {"from": account.address})
    tx.wait(1)

# def get_erc20_balance(address):
#     erc20_address = config["networks"][network.show_active()]["coin"]
#     erc20 = interface.IERC20(erc20_address)
#     return erc20.balanceOf(address) / 1e18

# def approve_erc20(amount, spender, erc20_address, account):
#     print("Approving ERC20 token...")
#     erc20 = interface.IERC20(erc20_address)
#     tx = erc20.approve(spender, amount, {"from": account})
#     tx.wait(1)
#     print("Approved!")


def get_lending_pool():
    print("Getting lending pool adress...")
    pool_address_provider = interface.IPoolAddressProvider(config["networks"][network.show_active()]["pool_address_provider"])
    pool_address = pool_address_provider.getPool()
    # print(f"Received pool address: {pool_address}")
    pool = interface.IPool(pool_address)
    return pool



def main():
    lend()
