from math import floor
from brownie import config, network, interface
from scripts.utils import get_token_info, get_asset_price, approve_erc20


class Aave:

    def __init__(self, account, token_to_borrow):

        self.account = account
        self.token_to_borrow = token_to_borrow

        self.weth_gateway = interface.IWETHGateway(config["networks"][network.show_active()]["weth_gateway"])
        self.pool_address_provider = interface.IPoolAddressesProvider(config["networks"][network.show_active()]["pool_address_provider"])

        # setting adresses
        print("Getting weth adress...")
        self.weth_address = self.weth_gateway.getWETHAddress()
        print("Getting lending pool adress...")
        self.pool_address = self.pool_address_provider.getPool()
        self.aave_weth_address = config["networks"][network.show_active()]["aave_weth_address"]
        self.borrowed_token_address = config["networks"][network.show_active()][self.token_to_borrow]
        self.aave_oracle_address = config["networks"][network.show_active()]["aave_oracle"]

        self.pool = interface.IPool(self.pool_address)

    def deposit_eth(self, amount):
        print(f"Depositing {amount / 1e18} native token to pool...")
        tx = self.weth_gateway.depositETH(self.pool, self.account.address, 0, {"from": self.account.address, "value": amount})
        tx.wait(1)

    def borrow(self, amount=None, health_factor=0.5):
        _, _, decimals = get_token_info(self.borrowed_token_address, self.account)
        if not amount:
            # borrow maximum amount
            price = get_asset_price(self.aave_oracle_address, self.borrowed_token_address) / 1e8
            _, available_borrow, _, _ = self.get_borrowable_data()
            available_borrow /= 1e8
            amount = floor((available_borrow / price) * health_factor * 10**decimals)
        print(f"Borrowing {amount / 10**decimals} of tokens from pool...")
        tx = self.pool.borrow(self.borrowed_token_address, amount, 1, 0, self.account.address, {"from": self.account.address})
        tx.wait(1)

    def repay(self, amount=None):
        balance, _, decimals = get_token_info(self.borrowed_token_address, self.account)
        if not amount:
            # TODO: amount should be min between borrowed amount
            #       and account balance
            amount = balance
            # amount = 2**256-1
        print(f"Repaying {amount / 10**decimals} of tokens to pool...")
        approve_erc20(self.borrowed_token_address, self.account.address, self.pool_address, amount)
        tx = self.pool.repay(self.borrowed_token_address, amount, 1, self.account.address, {"from": self.account.address})
        tx.wait(1)

    def withdraw_aave_weth_to_eth(self, amount=None):
        self.withdraw_aave_weth_to_weth(amount)
        self.withdraw_weth_to_eth(amount)

    def withdraw_aave_weth_to_weth(self, amount=None):
        if not amount:
            # withdraw maximum amount
            total_collateral, available_borrow, total_debt, ltv = self.get_borrowable_data()
            ltv /= 10000 # available_borrow / total_collateral (when initial deposited)
            if total_debt > 0:
                available_to_withdraw = round(available_borrow / ltv * 0.99) # debt is always growing
                print(f"Available to withdraw: {available_to_withdraw / 1e8}")
                weth_price = get_asset_price(self.aave_oracle_address, self.weth_address)
                print(f"Wrapped asset price: {weth_price / 1e8}")
                amount = ((available_to_withdraw / 1e8) / (weth_price / 1e8)) * 1e18
            else:
                amount = 2**256-1
        print(f"Withdrawing {amount / 1e18} aave wrapped native token from pool to wrapped native token...")
        tx = self.pool.withdraw(self.weth_address, amount, self.account.address, {"from": self.account.address})
        tx.wait(1)

    def withdraw_weth_to_eth(self, amount=None):
        wrapped_coin = interface.IWETH(self.weth_address)
        if not amount:
            amount = wrapped_coin.balanceOf(self.account)
        print(f"Withdrawing {amount / 1e18} {wrapped_coin.name()} from wrapped native token to native token...")
        tx = wrapped_coin.withdraw(amount, {"from": self.account.address})
        tx.wait(1)

    def get_borrowable_data(self):
        """
        Returns in 8-digit USD
        """
        (
            total_collateral,
            total_debt,
            available_borrow,
            current_liquidation_threshold,
            ltv,
            health_factor,
        ) = self.pool.getUserAccountData(self.account.address)
        return total_collateral, available_borrow, total_debt, ltv

    def print_state(self):
        weth_balance, weth_name, weth_decimals = get_token_info(self.weth_address, self.account)
        aave_weth_balance, aave_weth_name, aave_weth_decimals = get_token_info(self.aave_weth_address, self.account)
        borrowed_token_balance, borrowed_token_name, borrowed_token_decimals = get_token_info(self.borrowed_token_address, self.account)
        borrowed_token_price = get_asset_price(self.aave_oracle_address, self.borrowed_token_address)
        total_collateral, available_borrow, total_debt, ltv = self.get_borrowable_data()
        print("------------------------------------------------------")
        print(f"Native token amount: {self.account.balance() / 1e18}")
        print(f"{weth_name} amount: {weth_balance / 10**weth_decimals}")
        print(f"{aave_weth_name} amount: {aave_weth_balance / 10**aave_weth_decimals}")
        print(f"{borrowed_token_name} amount: {borrowed_token_balance / 10**borrowed_token_decimals}")
        print(f"{borrowed_token_name} price: {borrowed_token_price / 1e8}")
        print(f"{borrowed_token_name} value: {borrowed_token_balance / 10**borrowed_token_decimals * borrowed_token_price / 1e8}")
        print("---------------------------")
        print(f"Deposited: {total_collateral / 1e8} USD")
        print(f"Borrowed: {total_debt / 1e8} USD")
        print(f"May borrow: {available_borrow / 1e8} USD")
        print("------------------------------------------------------")
