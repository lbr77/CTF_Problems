// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "./IToken.sol";

contract SimpleDEX is ReentrancyGuard {
    struct AMM {
        IToken token0;
        IToken token1;
        uint256 reserve0;
        uint256 reserve1;
        mapping(address => uint256) lpBalances0;
        mapping(address => uint256) lpBalances1;
    }

    AMM[] public amms;

    event FlashLoan(address indexed borrower, uint256 amount);

    constructor() {}

    function addAMM(address _token0, address _token1) external {
        require(_token0 != _token1, "Tokens must be different");

        amms.push();
        uint256 index = amms.length - 1;
        AMM storage amm = amms[index];

        amm.token0 = IToken(_token0);
        amm.token1 = IToken(_token1);
        amm.reserve0 = 0;
        amm.reserve1 = 0;
    }

    function createLiquidityPool(address _token0, address _token1) external {
        require(_token0 != _token1, "Tokens must be different");

        amms.push();
        uint256 index = amms.length - 1;
        AMM storage amm = amms[index];

        amm.token0 = IToken(_token0);
        amm.token1 = IToken(_token1);
        amm.reserve0 = 0;
        amm.reserve1 = 0;
    }

    function addLiquidity(uint256 ammIndex, uint256 amount0, uint256 amount1) external {
        AMM storage amm = amms[ammIndex];
        require(amm.token0.transferFrom(msg.sender, address(this), amount0), "Transfer of token0 failed");
        require(amm.token1.transferFrom(msg.sender, address(this), amount1), "Transfer of token1 failed");

        amm.reserve0 += amount0;
        amm.reserve1 += amount1;
        amm.lpBalances0[msg.sender] += amount0;
        amm.lpBalances1[msg.sender] += amount1;
    }

    function removeLiquidity(uint256 ammIndex, uint256 lpAmount) external {
        AMM storage amm = amms[ammIndex];
        uint256 amount0 = lpAmount * amm.lpBalances0[msg.sender] / 100;
        uint256 amount1 = lpAmount * amm.lpBalances1[msg.sender] / 100;
        require(amm.token0.transfer(msg.sender, amount0), "Transfer of token0 failed");
        require(amm.token1.transfer(msg.sender, amount1), "Transfer of token1 failed");

        amm.reserve0 -= amount0;
        amm.reserve1 -= amount1;
        amm.lpBalances0[msg.sender] -= amount0;
        amm.lpBalances1[msg.sender] -= amount1;
    }

    function getPrice(uint256 ammIndex) external view returns (uint256) {
        AMM storage amm = amms[ammIndex];

        require(amm.reserve1 > 0, "Insufficient liquidity");
        return amm.reserve0 / amm.reserve1;
    }

    function swap(uint256 ammIndex, uint256 amountIn, bool isToken0) external {
        AMM storage amm = amms[ammIndex];

        uint256 reserveIn = isToken0 ? amm.reserve0 : amm.reserve1;
        uint256 reserveOut = isToken0 ? amm.reserve1 : amm.reserve0;

        uint256 amountOut = getAmountOut(amountIn, reserveIn, reserveOut);

        if (isToken0) {
            require(amm.token0.transferFrom(msg.sender, address(this), amountIn), "Transfer of token0 failed");
            require(amm.token1.transfer(msg.sender, amountOut), "Transfer of token1 failed");
            amm.reserve0 += amountIn;
            amm.reserve1 -= amountOut;
        } else {
            require(amm.token1.transferFrom(msg.sender, address(this), amountIn), "Transfer of token1 failed");
            require(amm.token0.transfer(msg.sender, amountOut), "Transfer of token0 failed");
            amm.reserve1 += amountIn;
            amm.reserve0 -= amountOut;
        }
    }

    function addLoan(uint256 amount, address token) external {
        require(IToken(token).transferFrom(msg.sender, address(this), amount), "Transfer of tokens failed");
    }

    function flashLoan(uint256 amount, address token) external nonReentrant {
        emit FlashLoan(msg.sender, amount);
        require(IToken(token).balanceOf(address(this)) >= amount, "Not enough tokens in pool");

        IToken(token).transfer(msg.sender, amount);
        (bool success,) = msg.sender.call(abi.encodeWithSignature("executeOperation(uint256,address)", amount, token));
        require(success, "Callback failed");

        require(IToken(token).transferFrom(msg.sender, address(this), amount), "Transfer of tokens failed");

        emit FlashLoan(msg.sender, amount);
    }

    function getAmountOut(uint256 amountIn, uint256 reserveIn, uint256 reserveOut) internal pure returns (uint256) {
        require(amountIn > 0, "Insufficient input amount");
        require(reserveIn > 0 && reserveOut > 0, "Insufficient liquidity");
        uint256 amountInWithFee = amountIn * 1000;
        uint256 numerator = amountInWithFee * reserveOut;
        uint256 denominator = reserveIn * 1000 + amountInWithFee;
        return numerator / denominator;
    }
}
