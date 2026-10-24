"""BIP32 derivation path parser."""
import argparse
import re
import sys

HARDENED = 0x80000000
PURPOSES = {44: "BIP44 (legacy / account-based chains)", 49: "BIP49 (nested SegWit P2SH-P2WPKH)",
            84: "BIP84 (native SegWit P2WPKH)", 86: "BIP86 (Taproot P2TR)"}
COINS = {0: "Bitcoin", 1: "testnet (all coins)", 2: "Litecoin", 3: "Dogecoin", 60: "Ethereum",
         118: "Cosmos", 195: "Tron", 354: "Polkadot", 501: "Solana", 637: "Aptos", 784: "Sui"}
SEGMENT = re.compile(r"^(\d+)(['hH]?)$")


def parse(path: str) -> list[tuple[int, bool]]:
    parts = path.strip().split("/")
    if parts[0] != "m":
        raise ValueError("path must start with m")
    out = []
    for seg in parts[1:]:
        m = SEGMENT.match(seg)
        if not m:
            raise ValueError(f"bad segment {seg!r}")
        idx = int(m.group(1))
        if idx >= HARDENED:
            raise ValueError(f"index {idx} too large (max {HARDENED - 1})")
        out.append((idx, bool(m.group(2))))
    return out


def fmt(components) -> str:
    return "m" + "".join(f"/{i}{chr(39) if h else ''}" for i, h in components)


def raw(components) -> list[int]:
    return [i + HARDENED if h else i for i, h in components]


def explain(components) -> list[tuple[str, str, str]]:
    names = ["purpose", "coin", "account", "change", "index"]
    rows = []
    for pos, (i, h) in enumerate(components):
        label = names[pos] if pos < len(names) else f"level {pos + 1}"
        note = ""
        if pos == 0:
            note = PURPOSES.get(i, "non-standard purpose")
        elif pos == 1:
            note = f"{COINS[i]} (SLIP-44)" if i in COINS else "unknown coin type"
        elif pos == 3:
            note = {0: "external (receive)", 1: "internal (change)"}.get(i, "")
        if pos < 3 and components[0][0] in PURPOSES and not h:
            note += "  [warning: should be hardened]"
        rows.append((label, f"{i}{chr(39) if h else ''}", note))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--range", help="A-B, replaces the last index")
    a = ap.parse_args()
    try:
        comps = parse(a.path)
    except ValueError as e:
        sys.exit(f"invalid: {e}")

    if a.range:
        lo, hi = (int(x) for x in a.range.split("-"))
        hardened = comps[-1][1]
        for i in range(lo, hi + 1):
            print(fmt(comps[:-1] + [(i, hardened)]))
        return
    print(fmt(comps))
    for label, val, note in explain(comps):
        print(f"  {label:<9} {val:<6} {note}")
    print(f"  raw indexes: {raw(comps)}")


if __name__ == "__main__":
    main()
