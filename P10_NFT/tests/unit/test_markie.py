import pytest
from brownie import network

from scripts.utils import LOCAL_ENVIRONMENTS, get_account
from scripts.deploy_and_create import deploy_and_create

def test_can_create_markie():
    if network.show_active() not in LOCAL_ENVIRONMENTS:
        pytest.skip()
    markie = deploy_and_create()
    assert markie.ownerOf(0) == get_account()
