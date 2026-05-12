import sys
from pathlib import Path

# Allow running this script directly from the repo root.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
	sys.path.insert(0, str(ROOT_DIR))

from src.encryption.vault import SimpleVault
vault = SimpleVault()

# Test round-trip
original = "Nguyen Van A - CCCD: 012345678901"
encrypted = vault.encrypt_data(original)
print("Encrypted:", encrypted)

decrypted = vault.decrypt_data(encrypted)
print("Decrypted:", decrypted)
assert decrypted == original, "Encryption round-trip FAILED!"
print("✓ Encryption test passed")