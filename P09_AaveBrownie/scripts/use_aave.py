from scripts.utils import get_account
from scripts.aave import Aave

DEPOSIT_AMOUNT = 0.01 * 1e18
TOKEN_TO_BORROW = "dai"  # one of ("dai", "btc")

def main():
    account = get_account()
    aave = Aave(account, TOKEN_TO_BORROW)

    # Initializing
    aave.print_state()

    # Deposit
    aave.deposit_eth(DEPOSIT_AMOUNT)
    aave.print_state()

    # Borrow
    aave.borrow()
    aave.print_state()

    # Repay
    aave.repay()
    aave.print_state()

    # Withdraw
    aave.withdraw_aave_weth_to_eth()
    aave.print_state()
