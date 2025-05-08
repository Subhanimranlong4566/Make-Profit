# create_wallet.py

from wallet import generate_keys

private_key, public_key = generate_keys()

print("Private Key:\n", private_key)
print("Public Key:\n", public_key)
