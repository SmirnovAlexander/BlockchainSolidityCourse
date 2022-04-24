from scripts.utils import get_account
from scripts.aave import Aave

LEND_AMOUNT = 0.01 * 1e18

def main():
    account = get_account()
    aave = Aave(account)

    # Initializing
    aave.print_state()

    # Deposit
    aave.deposit_eth(LEND_AMOUNT)
    aave.print_state()

    # Withdraw
    aave.withdraw_aave_weth_to_eth()
    aave.print_state()
