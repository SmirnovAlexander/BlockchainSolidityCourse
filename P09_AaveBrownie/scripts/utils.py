from brownie import network, accounts, config, interface

LOCAL_ENVIRONMENTS = [
    "mainnet-fork-dev",
    "polygon-main-fork",
]

def get_account(index=None, idx=None):
    if index:
        return accounts[index]
    if idx:
        return accounts.load(idx)
    if (network.show_active() in LOCAL_ENVIRONMENTS):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

def get_token_info(address, account):
    token = interface.IERC20Metadata(address)
    balance = token.balanceOf(account.address)
    name = token.name()
    decimals = token.decimals()
    return balance, name, decimals

def get_asset_price(oracle_address, asset_address):
    aave_oracle = interface.IAaveOracle(oracle_address)
    price = aave_oracle.getAssetPrice(asset_address)
    return price

def approve_erc20(asset_address, from_address, to_address, amount):
    token = interface.IERC20Metadata(asset_address)
    print(f"Approving sending {amount / 10**token.decimals()} {token.name()}...")
    tx = token.approve(to_address, amount, {"from": from_address})
    tx.wait(1)
