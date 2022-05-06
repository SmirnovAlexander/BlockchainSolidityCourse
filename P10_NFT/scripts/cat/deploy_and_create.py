from scripts.utils import get_account, OPENSEA_URL
from brownie import MultifacetedCat, config, network


def deploy_and_create():
    account = get_account()
    multifaceted_cat = MultifacetedCat.deploy(
        {"from": account.address}, 
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )
    print(f"You can view your NFT at {OPENSEA_URL.format(multifaceted_cat.address, multifaceted_cat.tokenCounter() - 1)}")
    return multifaceted_cat

def main():
    deploy_and_create()
