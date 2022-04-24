// SPDX-License-Identifier: agpl-3.0
pragma solidity 0.8.10;

import {IERC20Metadata} from '@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol';

interface IWETH is IERC20Metadata {
  function deposit() external payable;

  function withdraw(uint256) external;
}
