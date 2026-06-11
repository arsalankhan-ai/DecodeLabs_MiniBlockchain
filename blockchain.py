"""
Mini-Blockchain Implementation
================================
DecodeLabs Internship — Blockchain Technology Project 1
Intern: Arsalan Khan
Batch: 2026

Concepts Covered:
- SHA-256 Cryptographic Hashing
- Block Data Structure
- Proof of Work (Mining)
- Chain Validation
- Tampering Detection
"""

import hashlib
import time
import json


# ============================================================
#  BLOCK CLASS
# ============================================================

class Block:
    """
    Represents a single block in the blockchain.

    Attributes:
        index       : Position of the block in the chain (height)
        timestamp   : Time when the block was mined
        data        : Transaction payload (sender, receiver, amount)
        prev_hash   : Hash of the previous block (links the chain)
        nonce       : Mining variable incremented during Proof of Work
        hash        : SHA-256 hash of this block's contents
    """

    def __init__(self, index, data, prev_hash="0"):
        self.index     = index
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.data      = data          # e.g. {"sender": "Alice", "receiver": "Bob", "amount": 50}
        self.prev_hash = prev_hash
        self.nonce     = 0
        self.hash      = self.compute_hash()

    def compute_hash(self):
        """
        Generates the SHA-256 hash fingerprint of this block.
        Any change to any field completely changes the hash output.
        """
        block_content = json.dumps({
            "index"     : self.index,
            "timestamp" : self.timestamp,
            "data"      : self.data,
            "prev_hash" : self.prev_hash,
            "nonce"     : self.nonce
        }, sort_keys=True)

        return hashlib.sha256(block_content.encode()).hexdigest()

    def __repr__(self):
        return (
            f"\n{'='*60}\n"
            f"  Block #{self.index}\n"
            f"{'='*60}\n"
            f"  Timestamp : {self.timestamp}\n"
            f"  Data      : {json.dumps(self.data, indent=14)}\n"
            f"  Prev Hash : {self.prev_hash[:20]}...\n"
            f"  Hash      : {self.hash[:20]}...\n"
            f"  Nonce     : {self.nonce}\n"
            f"{'='*60}"
        )


# ============================================================
#  BLOCKCHAIN CLASS
# ============================================================

class Blockchain:
    """
    Manages the chain of blocks.

    Responsibilities:
        - Creating the Genesis Block
        - Mining new blocks with Proof of Work
        - Validating the entire chain integrity
        - Detecting tampering attempts
    """

    DIFFICULTY = 4   # Hash must start with this many leading zeros e.g. "0000..."

    def __init__(self):
        self.chain = []
        print("\n🔗 Initializing Blockchain...")
        print(f"   Proof of Work Difficulty: {self.DIFFICULTY} leading zeros")
        self._create_genesis_block()

    # ----------------------------------------------------------
    #  GENESIS BLOCK
    # ----------------------------------------------------------

    def _create_genesis_block(self):
        """
        Creates Block 0 — the first block in the chain.
        Its prev_hash is hardcoded to '0' since it has no parent.
        """
        print("\n⛏  Mining Genesis Block (Block #0)...")
        genesis = Block(
            index     = 0,
            data      = {"message": "Genesis Block — The Beginning of the Chain"},
            prev_hash = "0"
        )
        genesis = self._proof_of_work(genesis)
        self.chain.append(genesis)
        print(f"✅ Genesis Block mined! Hash: {genesis.hash[:30]}...")

    # ----------------------------------------------------------
    #  PROOF OF WORK
    # ----------------------------------------------------------

    def _proof_of_work(self, block):
        """
        Mining loop: increments nonce until the hash meets
        the difficulty target (starts with DIFFICULTY leading zeros).

        Algorithm:
            H_new = SHA256(index + timestamp + data + prev_hash + nonce)
            Repeat until H_new starts with '0000'
        """
        target = "0" * self.DIFFICULTY
        attempts = 0

        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash   = block.compute_hash()
            attempts    += 1

        print(f"   ✔ Block mined after {attempts:,} attempts | Nonce: {block.nonce}")
        return block

    # ----------------------------------------------------------
    #  ADD NEW BLOCK
    # ----------------------------------------------------------

    def add_block(self, data):
        """
        Creates, mines, and appends a new block to the chain.

        Args:
            data (dict): Transaction payload
        """
        prev_block = self.chain[-1]
        new_block  = Block(
            index     = len(self.chain),
            data      = data,
            prev_hash = prev_block.hash
        )
        print(f"\n⛏  Mining Block #{new_block.index}...")
        new_block = self._proof_of_work(new_block)
        self.chain.append(new_block)
        print(f"✅ Block #{new_block.index} added! Hash: {new_block.hash[:30]}...")
        return new_block

    # ----------------------------------------------------------
    #  CHAIN VALIDATION (Dual-Check)
    # ----------------------------------------------------------

    def validate_chain(self):
        """
        Validates the entire blockchain integrity using two checks:

        Check 1 — Stored Hash Integrity:
            Does Hash(block_data) == block.hash?
            If not → data inside the block was tampered with.

        Check 2 — Prev-Hash Linkage:
            Does block.prev_hash == previous_block.hash?
            If not → a block was removed, inserted, or re-sequenced.

        Returns:
            True  — chain is valid and untampered
            False — chain has been compromised
        """
        print("\n🔍 Validating Blockchain Integrity...")
        print(f"   Checking {len(self.chain)} blocks...\n")

        for i in range(1, len(self.chain)):
            current  = self.chain[i]
            previous = self.chain[i - 1]

            # --- Check 1: Hash Integrity ---
            recalculated_hash = current.compute_hash()
            if current.hash != recalculated_hash:
                print(f"   ❌ TAMPERED! Block #{current.index} — Hash mismatch!")
                print(f"      Stored Hash      : {current.hash[:30]}...")
                print(f"      Recalculated Hash: {recalculated_hash[:30]}...")
                return False
            else:
                print(f"   ✅ Block #{current.index} — Hash integrity: VALID")

            # --- Check 2: Chain Linkage ---
            if current.prev_hash != previous.hash:
                print(f"   ❌ BROKEN LINK! Block #{current.index} prev_hash doesn't match Block #{previous.index} hash!")
                return False
            else:
                print(f"   ✅ Block #{current.index} — Chain linkage: VALID")

        print("\n✅ Blockchain is VALID — No tampering detected.")
        return True

    # ----------------------------------------------------------
    #  DISPLAY CHAIN
    # ----------------------------------------------------------

    def display_chain(self):
        """Prints all blocks in the chain."""
        print(f"\n{'#'*60}")
        print(f"  BLOCKCHAIN — {len(self.chain)} Blocks")
        print(f"{'#'*60}")
        for block in self.chain:
            print(block)

    # ----------------------------------------------------------
    #  PROPERTIES
    # ----------------------------------------------------------

    @property
    def length(self):
        return len(self.chain)

    def get_block(self, index):
        return self.chain[index] if 0 <= index < len(self.chain) else None
