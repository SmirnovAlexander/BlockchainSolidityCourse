from scripts.deploy_token import deploy_token


def test_name():
    # Arrange
    token = deploy_token()
    # Act
    name = token.name()
    symbol = token.symbol()
    # Assert
    assert name == "Mark loh token", "Token name not matched! It is {name}"
    assert symbol == "MRKLOH", "Token name not matched! It is {symbol}"
