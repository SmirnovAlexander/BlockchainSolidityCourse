from brownie import VRFCoordinatorV2Mock, LinkToken
from brownie import network, accounts, config, interface, Contract

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

contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorV2Mock,
    "link_token": LinkToken
}

def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.

    Args:
        contract_name (string)

    Returns:
        brownie.network.contract.ProjectContract: the most recently deployed version
        of this contract
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract

BASE_FEE = 0.1 * 10**18;
GAS_PRICE_LINK = 1 * 10**18;

def deploy_mocks(base_fee=BASE_FEE, gas_price_link=GAS_PRICE_LINK):
    account = get_account()
    VRFCoordinatorV2Mock.deploy(base_fee, gas_price_link, {"from": account})
    LinkToken.deploy({"from": account})
    print("Mocks deployed!")

def get_token_info(address, account):
    token = interface.IERC20Metadata(address)
    balance = token.balanceOf(account.address)
    name = token.name()
    decimals = token.decimals()
    return balance, name, decimals

