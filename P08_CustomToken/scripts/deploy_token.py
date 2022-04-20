from scripts.utils import get_account
from brownie import MarkLohToken, network, config


def deploy_token():
    # account = get_account(idx="metamask-test")
    account = get_account()
    token = MarkLohToken.deploy(
        1000 * 10**18,
        "Mark loh token",
        "MRKLOH",
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )
    print(f"Deployed token at {token.address}")
    return token


def main():
    deploy_token()
