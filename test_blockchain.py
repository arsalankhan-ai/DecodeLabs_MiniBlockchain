"""
Unit Tests — Mini-Blockchain
==============================
DecodeLabs Internship — Blockchain Technology Project 1
Intern: Arsalan Khan | Batch 2026

Run with:
    python test_blockchain.py
"""

import unittest
from blockchain import Block, Blockchain


class TestBlock(unittest.TestCase):

    def test_block_creation(self):
        """Block should initialize with correct attributes"""
        block = Block(index=0, data={"msg": "test"}, prev_hash="0")
        self.assertEqual(block.index, 0)
        self.assertEqual(block.prev_hash, "0")
        self.assertEqual(block.nonce, 0)
        self.assertIsNotNone(block.hash)
        self.assertEqual(len(block.hash), 64)  # SHA-256 = 64 hex chars

    def test_hash_changes_on_data_change(self):
        """Changing block data must produce a completely different hash"""
        block = Block(index=1, data={"amount": 100}, prev_hash="abc123")
        original_hash = block.hash
        block.data["amount"] = 999  # tamper with data
        new_hash = block.compute_hash()
        self.assertNotEqual(original_hash, new_hash)

    def test_hash_determinism(self):
        """Same block content must always produce the same hash"""
        block = Block(index=1, data={"msg": "hello"}, prev_hash="0")
        hash1 = block.compute_hash()
        hash2 = block.compute_hash()
        self.assertEqual(hash1, hash2)


class TestBlockchain(unittest.TestCase):

    def setUp(self):
        """Create a fresh blockchain before each test"""
        self.bc = Blockchain()

    def test_genesis_block_exists(self):
        """Chain must start with exactly one Genesis Block"""
        self.assertEqual(len(self.bc.chain), 1)
        self.assertEqual(self.bc.chain[0].index, 0)
        self.assertEqual(self.bc.chain[0].prev_hash, "0")

    def test_genesis_block_meets_difficulty(self):
        """Genesis block hash must meet Proof of Work target"""
        target = "0" * Blockchain.DIFFICULTY
        self.assertTrue(self.bc.chain[0].hash.startswith(target))

    def test_add_block_increases_chain_length(self):
        """Adding a block must increase chain length by 1"""
        initial_length = len(self.bc.chain)
        self.bc.add_block({"sender": "A", "receiver": "B", "amount": 10})
        self.assertEqual(len(self.bc.chain), initial_length + 1)

    def test_new_block_linked_to_previous(self):
        """New block's prev_hash must equal previous block's hash"""
        self.bc.add_block({"sender": "Alice", "receiver": "Bob", "amount": 50})
        self.assertEqual(
            self.bc.chain[1].prev_hash,
            self.bc.chain[0].hash
        )

    def test_new_block_meets_difficulty(self):
        """Every mined block must start with required leading zeros"""
        self.bc.add_block({"msg": "test transaction"})
        target = "0" * Blockchain.DIFFICULTY
        self.assertTrue(self.bc.chain[-1].hash.startswith(target))

    def test_mine_three_blocks(self):
        """Must be able to mine at least 3 blocks successfully"""
        self.bc.add_block({"tx": 1, "amount": 100})
        self.bc.add_block({"tx": 2, "amount": 200})
        self.bc.add_block({"tx": 3, "amount": 300})
        self.assertEqual(len(self.bc.chain), 4)  # genesis + 3

    def test_valid_chain_returns_true(self):
        """validate_chain() must return True for an untampered chain"""
        self.bc.add_block({"sender": "A", "receiver": "B", "amount": 10})
        self.bc.add_block({"sender": "B", "receiver": "C", "amount": 20})
        self.assertTrue(self.bc.validate_chain())

    def test_tampered_data_detected(self):
        """Altering block data must be detected by validate_chain()"""
        self.bc.add_block({"sender": "Alice", "receiver": "Bob", "amount": 100})
        self.bc.add_block({"sender": "Bob", "receiver": "Charlie", "amount": 50})

        # Tamper with Block #1 data
        self.bc.chain[1].data["amount"] = 99999  # attacker changes amount

        # Chain should now be INVALID
        self.assertFalse(self.bc.validate_chain())

    def test_tampered_hash_detected(self):
        """Directly altering a block's hash must be detected"""
        self.bc.add_block({"msg": "legit transaction"})
        self.bc.chain[1].hash = "0000fakehashinjectedbyattacker1234567890abcdef"
        self.assertFalse(self.bc.validate_chain())


if __name__ == "__main__":
    print("="*60)
    print("  Running Unit Tests — DecodeLabs Mini-Blockchain")
    print("="*60)
    unittest.main(verbosity=2)
