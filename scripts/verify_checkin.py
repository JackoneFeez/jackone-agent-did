#!/usr/bin/env python3
"""verify_checkin.py — verifikasi tanda tangan pesan room Technocore.

Payload dihitung ULANG di sini (`<room>|<nonce>|<text>`) supaya kita tidak sekadar
mempercayai output tool. Kunci publik diturunkan dari field `from` (did:key).

Pakai:
  python3 scripts/verify_checkin.py                 # lobby, DID project ini
  python3 scripts/verify_checkin.py lobby --limit 100
  python3 scripts/verify_checkin.py lobby --did did:key:z6Mk...
"""
import argparse
import pathlib
import sys

TOOL = pathlib.Path.home() / "tools/technocore-did-gameplay"
sys.path.insert(0, str(TOOL))
import technocore_agent as T  # noqa: E402

DEFAULT_DID = "did:key:z6MkkKgQc8d1BYgxjB9Y4319VBawWgLWbydXea4ArfGv2UPG"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("room", nargs="?", default="lobby")
    ap.add_argument("--did", default=DEFAULT_DID)
    ap.add_argument("--limit", type=int, default=50)
    a = ap.parse_args()

    d = T.read_room(a.room, limit=a.limit)
    ms = d.get("messages") or []
    valid, mine, bad = 0, [], []
    for m in ms:
        try:
            payload = f"{a.room}|{m['nonce']}|{m['text']}".encode()
            T.public_key_from_did(m["from"]).verify(T.decode_signature(m["sig"]), payload)
            valid += 1
            if m.get("from") == a.did:
                mine.append((m.get("seq"), m.get("ts"), m.get("text")))
        except Exception as exc:
            bad.append((m.get("seq"), f"{type(exc).__name__}: {str(exc)[:70]}"))

    print(f"room '{a.room}': {len(ms)} pesan dibaca · {valid} tanda tangan VALID · {len(bad)} gagal")
    print(f"pesan dari DID project ini: {len(mine)}")
    for seq, ts, text in mine[-5:]:
        print(f"   ✅ seq {seq} · {ts} · {text!r}")
    for seq, err in bad[:5]:
        print(f"   ❌ seq {seq}: {err}")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
