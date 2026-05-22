# defi-protocol-templates — additional patterns and templates

## Governance Token

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GovernanceToken is ERC20Votes, Ownable {
    constructor() ERC20("Governance Token", "GOV") ERC20Permit("Governance Token") {
        _mint(msg.sender, 1000000 * 10**decimals());
    }

    function _afterTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override(ERC20Votes) {
        super._afterTokenTransfer(from, to, amount);
    }

    function _mint(address to, uint256 amount) internal override(ERC20Votes) {
        super._mint(to, amount);
    }

    function _burn(address account, uint256 amount) internal override(ERC20Votes) {
        super._burn(account, amount);
    }
}

contract Governor is Ownable {
    GovernanceToken public governanceToken;

    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 forVotes;
        uint256 againstVotes;
        uint256 startBlock;
        uint256 endBlock;
        bool executed;
        mapping(address => bool) hasVoted;
    }

    uint256 public proposalCount;
    mapping(uint256 => Proposal) public proposals;

    uint256 public votingPeriod = 17280; // ~3 days in blocks
    uint256 public proposalThreshold = 100000 * 10**18;

    event ProposalCreated(uint256 indexed proposalId, address proposer, string description);
    event VoteCast(address indexed voter, uint256 indexed proposalId, bool support, uint256 weight);
    event ProposalExecuted(uint256 indexed proposalId);

    constructor(address _governanceToken) {
        governanceToken = GovernanceToken(_governanceToken);
    }

    function propose(string memory description) external returns (uint256) {
        require(
            governanceToken.getPastVotes(msg.sender, block.number - 1) >= proposalThreshold,
            "Proposer votes below threshold"
        );

        proposalCount++;
        Proposal storage newProposal = proposals[proposalCount];
        newProposal.id = proposalCount;
        newProposal.proposer = msg.sender;
        newProposal.description = description;
        newProposal.startBlock = block.number;
        newProposal.endBlock = block.number + votingPeriod;

        emit ProposalCreated(proposalCount, msg.sender, description);
        return proposalCount;
    }

    function vote(uint256 proposalId, bool support) external {
        Proposal storage proposal = proposals[proposalId];
        require(block.number >= proposal.startBlock, "Voting not started");
        require(block.number <= proposal.endBlock, "Voting ended");
        require(!proposal.hasVoted[msg.sender], "Already voted");

        uint256 weight = governanceToken.getPastVotes(msg.sender, proposal.startBlock);
        require(weight > 0, "No voting power");

        proposal.hasVoted[msg.sender] = true;

        if (support) {
            proposal.forVotes += weight;
        } else {
            proposal.againstVotes += weight;
        }

        emit VoteCast(msg.sender, proposalId, support, weight);
    }

    function execute(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];
        require(block.number > proposal.endBlock, "Voting not ended");
        require(!proposal.executed, "Already executed");
        require(proposal.forVotes > proposal.againstVotes, "Proposal failed");

        proposal.executed = true;

        // Execute proposal logic here

        emit ProposalExecuted(proposalId);
    }
}
```

## Flash Loan

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IFlashLoanReceiver {
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 fee,
        bytes calldata params
    ) external returns (bool);
}

contract FlashLoanProvider {
    IERC20 public token;
    uint256 public feePercentage = 9; // 0.09% fee

    event FlashLoan(address indexed borrower, uint256 amount, uint256 fee);

    constructor(address _token) {
        token = IERC20(_token);
    }

    function flashLoan(
        address receiver,
        uint256 amount,
        bytes calldata params
    ) external {
        uint256 balanceBefore = token.balanceOf(address(this));
        require(balanceBefore >= amount, "Insufficient liquidity");

        uint256 fee = (amount * feePercentage) / 10000;

        // Send tokens to receiver
        token.transfer(receiver, amount);

        // Execute callback
        require(
            IFlashLoanReceiver(receiver).executeOperation(
                address(token),
                amount,
                fee,
                params
            ),
            "Flash loan failed"
        );

        // Verify repayment
        uint256 balanceAfter = token.balanceOf(address(this));
        require(balanceAfter >= balanceBefore + fee, "Flash loan not repaid");

        emit FlashLoan(receiver, amount, fee);
    }
}

// Example flash loan receiver
contract FlashLoanReceiver is IFlashLoanReceiver {
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 fee,
        bytes calldata params
    ) external override returns (bool) {
        // Decode params and execute arbitrage, liquidation, etc.
        // ...

        // Approve repayment
        IERC20(asset).approve(msg.sender, amount + fee);

        return true;
    }
}
```
