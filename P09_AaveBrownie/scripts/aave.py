from brownie import config, network, interface


class Aave:

    def __init__(self, account):

        self.account = account

        self.weth_gateway = interface.IWETHGateway(config["networks"][network.show_active()]["weth_gateway"])
        self.pool_address_provider = interface.IPoolAddressesProvider(config["networks"][network.show_active()]["pool_address_provider"])

        print("Getting weth adress...")
        self.weth_address = self.weth_gateway.getWETHAddress()
        print("Getting lending pool adress...")
        self.pool_address = self.pool_address_provider.getPool()
        self.aave_weth_address = config["networks"][network.show_active()]["aave_weth_address"]

        self.pool = interface.IPool(self.pool_address)

    def deposit_eth(self, amount):
        print(f"Depositing {amount / 1e18} native token to pool...")
        tx = self.weth_gateway.depositETH(self.pool, self.account.address, 0, {"from": self.account.address, "value": amount})
        tx.wait(1)

    def withdraw_aave_weth_to_eth(self, amount=None):
        self.withdraw_aave_weth_to_weth(amount)
        self.withdraw_weth_to_eth(amount)

    def withdraw_aave_weth_to_weth(self, amount=None):
        if not amount:
            amount = 2**256-1
        print(f"Withdrawing {amount / 1e18} aave wrapped native token from pool...")
        tx = self.pool.withdraw(self.weth_address, amount, self.account.address, {"from": self.account.address})
        tx.wait(1)

    def withdraw_weth_to_eth(self, amount=None):
        wrapped_coin = interface.IWETH(self.weth_address)
        if not amount:
            amount = wrapped_coin.balanceOf(self.account)
        print(f"Withdrawing {amount / 1e18} {wrapped_coin.name()} to account")
        tx = wrapped_coin.withdraw(amount, {"from": self.account.address})
        tx.wait(1)

    def get_wrapped_balance(self, address):
        wrapped_coin = interface.IWETH(address)
        balance = wrapped_coin.balanceOf(self.account.address)
        name = wrapped_coin.name()
        return balance, name

    def get_borrowable_data(self):
        (
            total_collateral,
            total_debt,
            available_borrow,
            current_liquidation_threshold,
            ltv,
            health_factor,
        ) = self.pool.getUserAccountData(self.account.address)
        return total_collateral, available_borrow, total_debt

    def print_state(self):
        weth_balance, weth_name = self.get_wrapped_balance(self.weth_address)
        aave_weth_balance, aave_weth_name = self.get_wrapped_balance(self.aave_weth_address)
        total_collateral, available_borrow, total_debt = self.get_borrowable_data()
        print("---------------------------")
        print(f"Native token amount: {self.account.balance() / 1e18}")
        print(f"{weth_name} amount: {weth_balance / 1e18}")
        print(f"{aave_weth_name} amount: {aave_weth_balance / 1e18}")
        print(f"Deposited: {total_collateral}")
        print(f"Borrowed: {total_debt}")
        print(f"May borrow: {available_borrow}")
        print("---------------------------")
