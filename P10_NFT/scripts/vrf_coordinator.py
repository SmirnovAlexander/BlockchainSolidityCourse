from brownie import VRFCoordinatorV2Mock, config, network
from scripts.utils import get_contract, get_token_info, get_account, LOCAL_ENVIRONMENTS
from brownie.convert import to_bytes


class VRFCoordinator:
    def __init__(self, account, sub_id=None):

        self.account = account
        self.sub_id = sub_id
        self.vrf_coordinator = get_contract("vrf_coordinator")
        self.link_token = get_contract("link_token")

        if not self.sub_id:
            self.create_subscription()

    def create_subscription(self):
        print(f"Creating new subscription...")
        tx = self.vrf_coordinator.createSubscription({"from": self.account.address})
        tx.wait(1)
        self.sub_id = tx.events["SubscriptionCreated"]["subId"]
        print(f"Created subscription under id {self.sub_id}")

    def fund_with_link(self, amount):
        print(f"Sending {amount / 10**18} LINK to subscription {self.sub_id}...")
        if network.show_active() in LOCAL_ENVIRONMENTS:
            tx = self.vrf_coordinator.fundSubscription(
                self.sub_id,
                amount
            )
        else:
            sub_id_bytes = to_bytes(self.sub_id)
            tx = self.link_token.transferAndCall(
                self.vrf_coordinator.address,
                amount,
                sub_id_bytes,
                {"from": self.account.address}
            )
        tx.wait(1)

    def add_consumer(self, address):
        print(f"Adding consumer {address} to {self.sub_id}...")
        tx = self.vrf_coordinator.addConsumer(
            self.sub_id,
            address,
            {"from": self.account.address}
        )
        tx.wait(1)

    def print_state(self):
        link_balance, link_name, link_decimals = get_token_info(self.link_token.address, self.account)
        print("------------------------------------------------------")
        print(f"Native coin amount: {self.account.balance() / 1e18}")
        print(f"{link_name} amount: {link_balance / 10**link_decimals}")
        if self.sub_id:
            balance, req_count, owner, consumers = self.vrf_coordinator.getSubscription(self.sub_id)
            print(f"Subscription {self.sub_id} balance: {balance / 1e18}")
            print(f"Subscription {self.sub_id} req_count: {req_count}")
            print(f"Subscription {self.sub_id} owner: {owner}")
            print(f"Subscription {self.sub_id} consumers: {consumers}")
        print("------------------------------------------------------")


def setup_vrf_coordinator(link_amount=1*1e18):
    
    account = get_account()
    sub_id = config["networks"][network.show_active()].get("chainlink_subscription_id", None)

    vrf_coordinator = VRFCoordinator(account, sub_id)
    vrf_coordinator.print_state()

    # vrf_coordinator.fund_with_link(link_amount)

    return vrf_coordinator
