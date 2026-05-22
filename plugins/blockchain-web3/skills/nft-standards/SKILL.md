---
name: nft-standards
description: Implement NFT standards (ERC-721, ERC-1155) with proper metadata handling, minting strategies, and marketplace integration. Use when creating NFT contracts, building NFT marketplaces, or implementing digital asset systems.
---

# NFT Standards

Master ERC-721 and ERC-1155 NFT standards, metadata best practices, and advanced NFT features.

## When to Use This Skill

- Creating NFT collections (art, gaming, collectibles)
- Implementing marketplace functionality
- Building on-chain or off-chain metadata
- Creating soulbound tokens (non-transferable)
- Implementing royalties and revenue sharing
- Developing dynamic/evolving NFTs

## ERC-721 (Non-Fungible Token Standard)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MyNFT is ERC721URIStorage, ERC721Enumerable, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant MINT_PRICE = 0.08 ether;
    uint256 public constant MAX_PER_MINT = 20;

    constructor() ERC721("MyNFT", "MNFT") {}

    function mint(uint256 quantity) external payable {
        require(quantity > 0 && quantity <= MAX_PER_MINT, "Invalid quantity");
        require(_tokenIds.current() + quantity <= MAX_SUPPLY, "Exceeds max supply");
        require(msg.value >= MINT_PRICE * quantity, "Insufficient payment");

        for (uint256 i = 0; i < quantity; i++) {
            _tokenIds.increment();
            uint256 newTokenId = _tokenIds.current();
            _safeMint(msg.sender, newTokenId);
            _setTokenURI(newTokenId, generateTokenURI(newTokenId));
        }
    }

    function generateTokenURI(uint256 tokenId) internal pure returns (string memory) {
        // Return IPFS URI or on-chain metadata
        return string(abi.encodePacked("ipfs://QmHash/", Strings.toString(tokenId), ".json"));
    }

    // Required overrides
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal override(ERC721, ERC721Enumerable) {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}
```

## ERC-1155 (Multi-Token Standard)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GameItems is ERC1155, Ownable {
    uint256 public constant SWORD = 1;
    uint256 public constant SHIELD = 2;
    uint256 public constant POTION = 3;

    mapping(uint256 => uint256) public tokenSupply;
    mapping(uint256 => uint256) public maxSupply;

    constructor() ERC1155("ipfs://QmBaseHash/{id}.json") {
        maxSupply[SWORD] = 1000;
        maxSupply[SHIELD] = 500;
        maxSupply[POTION] = 10000;
    }

    function mint(
        address to,
        uint256 id,
        uint256 amount
    ) external onlyOwner {
        require(tokenSupply[id] + amount <= maxSupply[id], "Exceeds max supply");

        _mint(to, id, amount, "");
        tokenSupply[id] += amount;
    }

    function mintBatch(
        address to,
        uint256[] memory ids,
        uint256[] memory amounts
    ) external onlyOwner {
        for (uint256 i = 0; i < ids.length; i++) {
            require(tokenSupply[ids[i]] + amounts[i] <= maxSupply[ids[i]], "Exceeds max supply");
            tokenSupply[ids[i]] += amounts[i];
        }

        _mintBatch(to, ids, amounts, "");
    }

    function burn(
        address from,
        uint256 id,
        uint256 amount
    ) external {
        require(from == msg.sender || isApprovedForAll(from, msg.sender), "Not authorized");
        _burn(from, id, amount);
        tokenSupply[id] -= amount;
    }
}
```

## Metadata Standards

### Off-Chain Metadata (IPFS)

```json
{
  "name": "NFT #1",
  "description": "Description of the NFT",
  "image": "ipfs://QmImageHash",
  "attributes": [
    {
      "trait_type": "Background",
      "value": "Blue"
    },
    {
      "trait_type": "Rarity",
      "value": "Legendary"
    },
    {
      "trait_type": "Power",
      "value": 95,
      "display_type": "number",
      "max_value": 100
    }
  ]
}
```

### On-Chain Metadata

```solidity
contract OnChainNFT is ERC721 {
    struct Traits {
        uint8 background;
        uint8 body;
        uint8 head;
        uint8 rarity;
    }

    mapping(uint256 => Traits) public tokenTraits;

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        Traits memory traits = tokenTraits[tokenId];

        string memory json = Base64.encode(
            bytes(
                string(
                    abi.encodePacked(
                        '{"name": "NFT #', Strings.toString(tokenId), '",',
                        '"description": "On-chain NFT",',
                        '"image": "data:image/svg+xml;base64,', generateSVG(traits), '",',
                        '"attributes": [',
                        '{"trait_type": "Background", "value": "', Strings.toString(traits.background), '"},',
                        '{"trait_type": "Rarity", "value": "', getRarityName(traits.rarity), '"}',
                        ']}'
                    )
                )
            )
        );

        return string(abi.encodePacked("data:application/json;base64,", json));
    }

    function generateSVG(Traits memory traits) internal pure returns (string memory) {
        // Generate SVG based on traits
        return "...";
    }
}
```

## Royalties (EIP-2981)

```solidity
import "@openzeppelin/contracts/interfaces/IERC2981.sol";

contract NFTWithRoyalties is ERC721, IERC2981 {
    address public royaltyRecipient;
    uint96 public royaltyFee = 500; // 5%

    constructor() ERC721("Royalty NFT", "RNFT") {
        royaltyRecipient = msg.sender;
    }

    function royaltyInfo(uint256 tokenId, uint256 salePrice)
        external
        view
        override
        returns (address receiver, uint256 royaltyAmount)
    {
        return (royaltyRecipient, (salePrice * royaltyFee) / 10000);
    }

    function setRoyalty(address recipient, uint96 fee) external onlyOwner {
        require(fee <= 1000, "Royalty fee too high"); // Max 10%
        royaltyRecipient = recipient;
        royaltyFee = fee;
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, IERC165)
        returns (bool)
    {
        return interfaceId == type(IERC2981).interfaceId ||
               super.supportsInterface(interfaceId);
    }
}
```

## Additional patterns and templates

More detailed templates and worked examples live in `references/details.md`. Read that file for the full pattern library.

