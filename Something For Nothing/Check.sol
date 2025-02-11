// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../src/DEX.sol";
interface IAttack {
    function attack(address _token0, address _token1, address _token2, address _dex, address _profitReceiver) external;
}
contract CheckRun {
    address profitReceiver = 0x0000000000000000000000000000000000000001;
    bool public result;

    function run(address _dex, address _attack) external {
        IToken USDT = new IToken("Tether USD", "USDT", address(this));
        IToken VNB = new IToken("VN Coin", "VNB", address(this));
        IToken WMB = new IToken("WM Coin", "WMB", address(this));

        USDT.approve(_dex,type(uint256).max);
        VNB.approve(_dex,type(uint256).max);
        WMB.approve(_dex,type(uint256).max);
        
        SimpleDEX dex = SimpleDEX(_dex);
        dex.createLiquidityPool(address(USDT), address(VNB));
        dex.addLiquidity(0, 10000 ether, 100_000 ether);
        dex.createLiquidityPool(address(VNB), address(WMB));
        dex.addLiquidity(1, 100_000 ether, 100_000 ether);
        dex.createLiquidityPool(address(USDT), address(WMB));
        dex.addLiquidity(2, 10_000 ether, 10_000 ether);
        uint256 restUSDT = USDT.balanceOf(address(this));
        USDT.approve(address(dex), restUSDT);
        dex.addLoan(restUSDT, address(USDT));
        uint256 restVNB = VNB.balanceOf(address(this));
        VNB.approve(address(dex), restVNB);
        dex.addLoan(restVNB, address(VNB));
        uint256 restWMB = WMB.balanceOf(address(this));
        WMB.approve(address(dex), restWMB);
        dex.addLoan(restWMB, address(WMB));

        uint256 balance = USDT.balanceOf(profitReceiver);
        IAttack attack = IAttack(_attack);
        attack.attack(address(USDT), address(VNB), address(WMB), address(dex), profitReceiver);

        uint256 balanceAfter = USDT.balanceOf(profitReceiver);
        if (balanceAfter - balance > 0) {
            result = true;
        } else {
            result = false;
        }
    }
}
