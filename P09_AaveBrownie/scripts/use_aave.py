from scripts.utils import get_account
from scripts.aave import Aave

LEND_AMOUNT = 0.1 * 1e18
# LEND_AMOUNT = 100 * 1e18
TOKEN_TO_BORROW = "btc"
# TOKEN_TO_BORROW = "dai"

def main():
    account = get_account()
    aave = Aave(account, TOKEN_TO_BORROW)

    # Initializing
    aave.print_state()

    # Deposit
    aave.deposit_eth(LEND_AMOUNT)
    aave.print_state()

    # Borrow
    aave.borrow()
    aave.print_state()

#     # Withdraw
#     aave.withdraw_aave_weth_to_eth()
#     aave.print_state()
