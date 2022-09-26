from scripts.utils import get_account, upgrade, encode_function_data
from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    exceptions,
)
import pytest


def test_proxy_upgrades():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin,
        box_encoded_initializer_function,
        {"from": account, "gas": 1e6},
    )

    box_v2 = BoxV2.deploy({"from": account})
    box_proxy = Contract.from_abi("BoxV2", proxy, BoxV2.abi)

    with pytest.raises(exceptions.VirtualMachineError):
        box_proxy.increment({"from": account})

    transaction = upgrade(account, proxy, box_v2, proxy_admin)
    assert box_proxy.retrieve() == 0
    box_proxy.increment({"from": account})
    assert box_proxy.retrieve() == 1
