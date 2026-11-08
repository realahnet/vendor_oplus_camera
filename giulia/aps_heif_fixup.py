# SPDX-FileCopyrightText: 2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0

from hashlib import sha256
from pathlib import Path
from typing import Final


DLOPEN_TARGETS_HEIF: Final = (b"libHeifEncoderWrapper.so", b"xibHeifEncoderWrapper.so")
DLOPEN_TARGETS_WINBUFF: Final = (b"libNativeWinBuffExchange.so", b"xibNativeWinBuffExchange.so")

# Per-blob-generation configuration:
#   stock sha256 -> (dlopen target offsets, patched sha256)
#
# ColorOS 16 PKG110_16.0.10.500:
#   HeifEncoderWrapper: 0x4c11b, NativeWinBuffExchange: 0x48551
# ColorOS 15 PKG110_COS_15.0.0.840:
#   HeifEncoderWrapper: 0xd0277, NativeWinBuffExchange: 0xd0323
APSCLIENT_BLOBS: Final = {
    "b6669463a2dbdc22d20d0bb1a565ef9f1cc058f5f34c627a8d49971f7c509bec": (
        [0x4C11B, 0x48551],
        "fadd66bfe6344294fa0d3055382b1506e8432d01a562849478be82973e5974f8",
    ),
    "e1a74914de731b0af122ee715ff46e5520dcabd20db1ba3397ebe072959c7f29": (
        [0xD0277, 0xD0323],
        "67a6cdac348196297864b55bf89fcb590e1b201038a74ef00f58b45097cf5183",
    ),
}


class ApsClientFixupError(RuntimeError):
    pass


def patch_apsclient_heif_selector(blob: bytes) -> bytes:
    stock_sha256 = sha256(blob).hexdigest()

    entry = APSCLIENT_BLOBS.get(stock_sha256)
    if entry is None:
        msg = (
            "APS client SHA-256 mismatch: unknown blob generation, "
            f"found {stock_sha256}"
        )
        raise ApsClientFixupError(msg)

    offsets, expected_patched_sha256 = entry
    targets = (DLOPEN_TARGETS_HEIF, DLOPEN_TARGETS_WINBUFF)

    patched = bytearray(blob)
    for offset, (expected, replacement) in zip(offsets, targets):
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
    actual_patched_sha256 = sha256(result).hexdigest()
    if actual_patched_sha256 != expected_patched_sha256:
        msg = (
            "patched APS client SHA-256 mismatch: "
            f"expected {expected_patched_sha256}, "
            f"found {actual_patched_sha256}"
        )
        raise ApsClientFixupError(msg)
    return result


def patch_apsclient_heif_selector_file(file_path: str) -> None:
    path = Path(file_path)
    path.write_bytes(patch_apsclient_heif_selector(path.read_bytes()))
