"""Export saved Firefox logins to CSV using libnss3 (D-064).

Same mechanism as the well-known firefox_decrypt tool: ask NSS (the library
Firefox itself uses) to decrypt the entries in logins.json with the key from
key4.db. The owner (Kllosha) explicitly requested this export of his own
credentials into his assistant's secret store.

Firefox can stay open: we copy the profile's key4.db / cert9.db / logins.json
into a temp dir and point NSS at the copy, so we never fight Firefox for the
live files. If a Primary Password is set, pass it as argv[1].

Usage:
    python3 firefox_export.py [primary_password] > firefox-logins.csv
"""
import base64
import csv
import ctypes as ct
import glob
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

PROFILES = Path.home() / ".mozilla" / "firefox"


class SECItem(ct.Structure):
    _fields_ = [("type", ct.c_uint), ("data", ct.c_char_p), ("len", ct.c_uint)]


def _find_profile() -> Path:
    # Prefer the default-release profile that actually has logins.json.
    candidates = sorted(PROFILES.glob("*"), key=lambda p: p.name)
    with_logins = [p for p in candidates if (p / "logins.json").is_file()]
    if not with_logins:
        raise SystemExit("no Firefox profile with logins.json found")
    # default-release wins if present
    for p in with_logins:
        if "default-release" in p.name:
            return p
    return with_logins[0]


def main() -> int:
    primary_pw = sys.argv[1] if len(sys.argv) > 1 else ""
    profile = _find_profile()
    logins = json.loads((profile / "logins.json").read_text())["logins"]

    workdir = Path(tempfile.mkdtemp(prefix="ffexport_"))
    try:
        for name in ("key4.db", "cert9.db", "logins.json", "pkcs11.txt"):
            src = profile / name
            if src.exists():
                shutil.copy2(src, workdir / name)

        nss = ct.CDLL("libnss3.so")
        if nss.NSS_Init(f"sql:{workdir}".encode()) != 0:
            raise SystemExit("NSS_Init failed")
        try:
            # Authenticate the key slot (needed even with an empty password).
            slot = nss.PK11_GetInternalKeySlot()
            if nss.PK11_CheckUserPassword(slot, primary_pw.encode()) != 0:
                raise SystemExit("wrong Primary Password (pass it as argv[1])")
            nss.PK11_FreeSlot(slot)

            def decrypt(b64: str) -> str:
                raw = base64.b64decode(b64)
                inp = SECItem(0, raw, len(raw))
                out = SECItem(0, None, 0)
                if nss.PK11SDR_Decrypt(ct.byref(inp), ct.byref(out), None) != 0:
                    return "<decrypt-failed>"
                return ct.string_at(out.data, out.len).decode("utf-8", "replace")

            writer = csv.writer(sys.stdout)
            writer.writerow(["url", "username", "password"])
            for entry in logins:
                writer.writerow([
                    entry.get("hostname", ""),
                    decrypt(entry["encryptedUsername"]),
                    decrypt(entry["encryptedPassword"]),
                ])
        finally:
            nss.NSS_Shutdown()
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
