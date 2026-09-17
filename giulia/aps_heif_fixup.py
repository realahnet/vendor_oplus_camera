# SPDX-FileCopyrightText: 2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0

from hashlib import sha256
from pathlib import Path
from typing import Final


APSCLIENT_STOCK_SHA256: Final = (
    "b6669463a2dbdc22d20d0bb1a565ef9f1cc058f5f34c627a8d49971f7c509bec"
)
APSCLIENT_PATCHED_SHA256: Final = (
    "fadd66bfe6344294fa0d3055382b1506e8432d01a562849478be82973e5974f8"
)
_DLOPEN_TARGETS: Final = (
    (0x4C11B, b"libHeifEncoderWrapper.so", b"xibHeifEncoderWrapper.so"),
    (0x48551, b"libNativeWinBuffExchange.so", b"xibNativeWinBuffExchange.so"),
)


class ApsClientFixupError(RuntimeError):
    pass


def patch_apsclient_heif_selector(
    blob: bytes,
    *,
    expected_sha256: str = APSCLIENT_STOCK_SHA256,
) -> bytes:
    actual_sha256 = sha256(blob).hexdigest()
    if actual_sha256 != expected_sha256:
        msg = (
            "APS client SHA-256 mismatch: "
            f"expected {expected_sha256}, found {actual_sha256}"
        )
        raise ApsClientFixupError(msg)

    patched = bytearray(blob)
    for offset, expected, replacement in _DLOPEN_TARGETS:
        end = offset + len(expected)
        if blob[offset:end] != expected:
            found = blob[offset:end]
            msg = (
                f"APS client dlopen target mismatch at {offset:#x}: "
                f"expected {expected!r}, found {found!r}"
            )
            raise ApsClientFixupError(msg)
        patched[offset:end] = replacement

    result = bytes(patched)
    if expected_sha256 == APSCLIENT_STOCK_SHA256:
        actual_patched_sha256 = sha256(result).hexdigest()
        if actual_patched_sha256 != APSCLIENT_PATCHED_SHA256:
            msg = (
                "patched APS client SHA-256 mismatch: "
                f"expected {APSCLIENT_PATCHED_SHA256}, "
                f"found {actual_patched_sha256}"
            )
            raise ApsClientFixupError(msg)
    return result


def patch_apsclient_heif_selector_file(file_path: str) -> None:
    path = Path(file_path)
    path.write_bytes(patch_apsclient_heif_selector(path.read_bytes()))
