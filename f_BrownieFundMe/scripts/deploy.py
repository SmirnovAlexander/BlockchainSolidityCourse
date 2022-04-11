from brownie import accounts, config
from brownie import FundMe
from scripts.utils import get_account

def deploy_fund_me():

    account = get_account()
    print(account)
    fund_me = FundMe.deploy({"from": account})
    print(f"Contract deployed to {fund_me.address}")
    # get_account()
    # res = 

def main():
    deploy_fund_me()

