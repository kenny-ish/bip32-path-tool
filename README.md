# bip32-path-tool

Explains BIP32 derivation paths such as `m/84'/0'/0'/0/5` and can list a range of address indexes.

```bash
python path.py "m/44'/60'/0'/0/0"
python path.py "m/84h/0h/0h/0/0" --range 0-4
python path.py "m/44'/501'/3'/0'"
```

```
m/44'/60'/0'/0/0
  purpose   44'   BIP44 (legacy / account-based chains)
  coin      60'   Ethereum (SLIP-44)
  account   0'
  change    0     external (receive)
  index     0
  raw indexes: [2147483692, 2147483708, 2147483648, 0, 0]
```

`'`, `h` and `H` are all accepted as the hardened marker. Indexes of 2^31 or more and malformed
segments are rejected. The tool knows purposes 44, 49, 84 and 86 and the common SLIP-44 coin types
(add more to `COINS`).

`--range A-B` replaces the last component and prints one path per index. That's the list a wallet
scans when it looks for used addresses.

It only works with the path notation and never touches keys.

## Tests

```bash
python -m unittest -v
```
