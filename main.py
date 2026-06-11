"""
DecodeLabs Blockchain Internship — Project 1
=============================================
Intern  : Arsalan Khan
Batch   : 2026
Domain  : Blockchain Technology

Run this file to see the complete Mini-Blockchain in action:
    - Genesis Block creation
    - Mining 3 subsequent blocks
    - Chain validation
    - Tampering simulation & detection
"""

from blockchain import Blockchain


def separator(title=""):
    width = 60
    if title:
        print(f"\n{'─'*width}")
        print(f"  {title}")
        print(f"{'─'*width}")
    else:
        print(f"\n{'─'*width}")


def main():

    print("="*60)
    print("  DecodeLabs — Mini-Blockchain Project")
    print("  Intern: Arsalan Khan | Batch 2026")
    print("="*60)


    # --------------------------------------------------------
    # STEP 1: Create Blockchain (mines Genesis Block)
    # --------------------------------------------------------
    separator("STEP 1: Creating the Blockchain")
    bc = Blockchain()


    # --------------------------------------------------------
    # STEP 2: Mine 3 subsequent blocks with transactions
    # --------------------------------------------------------
    separator("STEP 2: Mining 3 Subsequent Blocks")

    bc.add_block({
        "sender"   : "Arsalan Khan",
        "receiver" : "DecodeLabs",
        "amount"   : 100,
        "note"     : "Internship Registration Fee"
    })

    bc.add_block({
        "sender"   : "Alice",
        "receiver" : "Bob",
        "amount"   : 250,
        "note"     : "Payment for freelance work"
    })

    bc.add_block({
        "sender"   : "Bob",
        "receiver" : "Charlie",
        "amount"   : 75,
        "note"     : "Split bill transfer"
    })


    # --------------------------------------------------------
    # STEP 3: Display the full chain
    # --------------------------------------------------------
    separator("STEP 3: Full Blockchain State")
    bc.display_chain()


    # --------------------------------------------------------
    # STEP 4: Validate the chain (should be VALID)
    # --------------------------------------------------------
    separator("STEP 4: Chain Validation (Before Tampering)")
    result = bc.validate_chain()
    print(f"\n   Chain Valid: {result}")


    # --------------------------------------------------------
    # STEP 5: Simulate a tampering attack
    # --------------------------------------------------------
    separator("STEP 5: Tampering Attack Simulation")

    print("\n🚨 Simulating attack: Malicious actor alters Block #1 data...")
    print("   Original amount: 100")
    print("   Tampered amount: 99999  ← attacker tries to steal funds!\n")

    # Directly mutate block data (bypassing mining)
    bc.chain[1].data["amount"] = 99999
    # Note: hash is NOT recalculated — this is what an attacker would do

    print("   Block #1 data has been altered.")
    print("   Now running chain validation to detect the attack...\n")


    # --------------------------------------------------------
    # STEP 6: Validate after tampering (should FAIL)
    # --------------------------------------------------------
    separator("STEP 6: Chain Validation (After Tampering)")
    result = bc.validate_chain()
    print(f"\n   Chain Valid: {result}")

    if not result:
        print("\n🛡️  BLOCKCHAIN SECURITY CONFIRMED!")
        print("   The tampering was detected immediately.")
        print("   Cryptographic hashing makes data immutable.")
        print("   Changing even one character invalidates the entire chain.")


    # --------------------------------------------------------
    # STEP 7: Summary
    # --------------------------------------------------------
    separator("STEP 7: Project Summary")
    print(f"""
   ✅ Genesis Block created with Proof of Work
   ✅ 3 subsequent blocks mined successfully
   ✅ SHA-256 cryptographic hashing implemented
   ✅ Proof of Work difficulty: {bc.DIFFICULTY} leading zeros
   ✅ Dual-check validation (hash integrity + chain linkage)
   ✅ Tampering detection confirmed
   ✅ Total blocks in chain: {bc.length}

   Key Skills Demonstrated:
   • Cryptographic Hashing (SHA-256)
   • Data Structures (Block & Blockchain classes)
   • Proof of Work consensus mechanism
   • Chain validation & tamper detection
   • Object-Oriented Programming (Python)
    """)

    print("="*60)
    print("  Project 1 Complete — DecodeLabs Blockchain Internship")
    print("="*60)


if __name__ == "__main__":
    main()
