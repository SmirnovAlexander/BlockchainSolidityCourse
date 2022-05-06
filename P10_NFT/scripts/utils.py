from brownie import network, accounts, config

LOCAL_ENVIRONMENTS = [
    "development",
    "mainnet-fork-dev",
    "polygon-main-fork",
]

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

def get_account(index=None, idx=None):
    if index:
        return accounts[index]
    if idx:
        return accounts.load(idx)
    if (network.show_active() in LOCAL_ENVIRONMENTS):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])
