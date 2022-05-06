from scripts.utils import get_account, OPENSEA_URL
from brownie import Markie, config, network


SAMPLE_TOKEN_URI = "https://ipfs.io/ipfs/QmcniohknCzUnwK3hhBmbmc1wFbESy1PbcEQhVxo5uQ3F7?filename=mark.json"


def deploy_and_create():
    account = get_account()
    markie = Markie.deploy(
        {"from": account.address}, 
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )
    tx = markie.createCollectible(SAMPLE_TOKEN_URI, {"from": account.address})
    tx.wait(1)
    print(f"You can view your NFT at {OPENSEA_URL.format(markie.address, markie.tokenCounter() - 1)}")
    return markie

def main():
    deploy_and_create()
