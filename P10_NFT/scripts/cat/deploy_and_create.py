from scripts.utils import get_account, OPENSEA_URL, get_contract
from brownie import MultifacetedCat, config, network
from scripts.vrf_coordinator import setup_vrf_coordinator

SAMPLE_TOKEN_URI = "https://ipfs.io/ipfs/QmcniohknCzUnwK3hhBmbmc1wFbESy1PbcEQhVxo5uQ3F7?filename=mark.json"
LINK_AMOUNT = 10*1e18

# TODO1
# - uncomment fund with link
# - uncomment etherscan verification

def deploy_and_create():
    vrf_coordinator = setup_vrf_coordinator(LINK_AMOUNT)

    account = get_account()
    print("Deploying contract...")
    multifaceted_cat = MultifacetedCat.deploy(
        vrf_coordinator.sub_id,
        vrf_coordinator.vrf_coordinator.address, # maybe load from get_contract
        config["networks"][network.show_active()]["key_hash"], # if does not matter change to some default value and remove from config
        {"from": account.address}, 
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )

    vrf_coordinator.add_consumer(multifaceted_cat)
    vrf_coordinator.print_state()

    print("Issuing new token...")
    tx = multifaceted_cat.createCat({"from": account.address})
    tx.wait(1)

    print(f"You can view your NFT at {OPENSEA_URL.format(multifaceted_cat.address, multifaceted_cat.tokenCounter() - 1)}")

    # print(f"You can view your NFT at {OPENSEA_URL.format(multifaceted_cat.address, multifaceted_cat.tokenCounter() - 1)}")

    # print("Setting URI...")
    # tx = multifaceted_cat.setTokenURI(0, SAMPLE_TOKEN_URI, {"from": account.address})
    # tx.wait(1)


    # print(f"You can view your NFT at {OPENSEA_URL.format(multifaceted_cat.address, multifaceted_cat.tokenCounter() - 1)}")

    return multifaceted_cat

def main():
    multifaceted_cat = deploy_and_create()
