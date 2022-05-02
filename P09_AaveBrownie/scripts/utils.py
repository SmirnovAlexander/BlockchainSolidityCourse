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
