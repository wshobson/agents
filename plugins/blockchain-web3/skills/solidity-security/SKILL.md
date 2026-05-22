---
name: solidity-security
description: Master smart contract security best practices to prevent common vulnerabilities and implement secure Solidity patterns. Use when writing smart contracts, auditing existing contracts, or implementing security measures for blockchain applications.
---

# Solidity Security

Master smart contract security best practices, vulnerability prevention, and secure Solidity development patterns.

## When to Use This Skill

- Writing secure smart contracts
- Auditing existing contracts for vulnerabilities
- Implementing secure DeFi protocols
- Preventing reentrancy, overflow, and access control issues
- Optimizing gas usage while maintaining security
- Preparing contracts for professional audits
- Understanding common attack vectors

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Testing for Security

```javascript
// Hardhat test example
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Security Tests", function () {
  it("Should prevent reentrancy attack", async function () {
    const [attacker] = await ethers.getSigners();

    const VictimBank = await ethers.getContractFactory("SecureBank");
    const bank = await VictimBank.deploy();

    const Attacker = await ethers.getContractFactory("ReentrancyAttacker");
    const attackerContract = await Attacker.deploy(bank.address);

    // Deposit funds
    await bank.deposit({ value: ethers.utils.parseEther("10") });

    // Attempt reentrancy attack
    await expect(
      attackerContract.attack({ value: ethers.utils.parseEther("1") }),
    ).to.be.revertedWith("ReentrancyGuard: reentrant call");
  });

  it("Should prevent integer overflow", async function () {
    const Token = await ethers.getContractFactory("SecureToken");
    const token = await Token.deploy();

    // Attempt overflow
    await expect(token.transfer(attacker.address, ethers.constants.MaxUint256))
      .to.be.reverted;
  });

  it("Should enforce access control", async function () {
    const [owner, attacker] = await ethers.getSigners();

    const Contract = await ethers.getContractFactory("SecureContract");
    const contract = await Contract.deploy();

    // Attempt unauthorized withdrawal
    await expect(contract.connect(attacker).withdraw(100)).to.be.revertedWith(
      "Ownable: caller is not the owner",
    );
  });
});
```

## Audit Preparation

```solidity
contract WellDocumentedContract {
    /**
     * @title Well Documented Contract
     * @dev Example of proper documentation for audits
     * @notice This contract handles user deposits and withdrawals
     */

    /// @notice Mapping of user balances
    mapping(address => uint256) public balances;

    /**
     * @dev Deposits ETH into the contract
     * @notice Anyone can deposit funds
     */
    function deposit() public payable {
        require(msg.value > 0, "Must send ETH");
        balances[msg.sender] += msg.value;
    }

    /**
     * @dev Withdraws user's balance
     * @notice Follows CEI pattern to prevent reentrancy
     * @param amount Amount to withdraw in wei
     */
    function withdraw(uint256 amount) public {
        // CHECKS
        require(amount <= balances[msg.sender], "Insufficient balance");

        // EFFECTS
        balances[msg.sender] -= amount;

        // INTERACTIONS
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```
