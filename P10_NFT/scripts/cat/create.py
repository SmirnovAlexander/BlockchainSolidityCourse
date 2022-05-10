
from scripts.utils import get_account, OPENSEA_URL, get_contract
from brownie import MultifacetedCat, config, network
from scripts.vrf_coordinator import setup_vrf_coordinator

SAMPLE_TOKEN_URI = "https://ipfs.io/ipfs/QmcniohknCzUnwK3hhBmbmc1wFbESy1PbcEQhVxo5uQ3F7?filename=mark.json"

def create():

    account = get_account()
    multifaceted_cat = MultifacetedCat[-1]

    print("Issuing new token...")
    tx = multifaceted_cat.createCat({"from": account.address})
    tx.wait(1)

    print(f"You can view your NFT at {OPENSEA_URL.format(multifaceted_cat.address, multifaceted_cat.tokenCounter() - 1)}")

def main():
    create()
