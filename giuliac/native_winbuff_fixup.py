# SPDX-FileCopyrightText: 2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0

"""
libNativeWinBuffExchange.so fixup for AOSP-17 buffer queue ABI.

The blob calls IGraphicBufferConsumer::releaseBuffer through the vtable
using the legacy 5-argument ABI (slot, frameNumber, eglDisplay, eglFence,
fence) where the Fence reference lives in x5. AOSP 17 (with
bq_gl_fence_cleanup enabled) ships the modern 3-argument ABI where the
Fence reference lives in x3.

This patch rewrites the argument setup so the fence pointer lands in x3:
    mov x3, xzr   ->   mov x3, x5

The surrounding instruction sequence is content-verified so the patch
fails loudly if a firmware update changes the blob's code generation.

Two blob generations are supported, identified by stock SHA-256:

- ColorOS 16 PKG110_16.0.10.500 (attachHardwareBufferToBufferQ):
      add  x5, sp, #0          ; legacy fence position
      mov  x0, x20
      mov  x2, xzr
      mov  x3, xzr             <-- byte 15 patched
      ldr  x8, [x8, #0x48]
      mov  x4, xzr
      blr  x8

- ColorOS 15 PKG110_COS_15.0.0.840 (exchangeHardwareBufferBetweenBufferQ):
      add  x5, sp, #0          ; legacy fence position
      mov  x2, xzr
      mov  x3, xzr             <-- byte 11 patched
      ldr  x8, [x8, #0x38]
      mov  x4, xzr
      blr  x8
"""

from hashlib import sha256
from pathlib import Path
from typing import Final


# The dispatch site sequence leading up to the vtable call of
# releaseBuffer, unique within each blob generation.
#
# The patch byte is the Rm register field of the `mov x3, ...`
# instruction (byte 2 of the little-endian instruction encoding).
_STOCK_BYTE: Final = 0x1F    # xzr (legacy: eglDisplay = null)
_PATCHED_BYTE: Final = 0x05  # x5  (modern: fence reference)

_CALLSEQUENCES: Final = {
    # stock sha256 -> (call sequence, patch offset, patched sha256)

    # ColorOS 16 PKG110_16.0.10.500 attachHardwareBufferToBufferQ
    # (mov x3 is the 4th instruction: offset byte 14)
    "59cd5a8bcc724f6e43860405d421f5e81839f1c7a969e6b2562367142423b155": (
        bytes.fromhex(
            "e5030091"  # add x5, sp, #0
            "e00314aa"  # mov x0, x20
            "e2031faa"  # mov x2, xzr
            "e3031faa"  # mov x3, xzr
            "082540f9"  # ldr x8, [x8, #0x48]
            "e4031faa"  # mov x4, xzr
            "00013fd6"  # blr x8
        ),
        14,
        "e4b2c3d1883ade848f35b7ead71ae8c1a876f4dd71346ea1cf15b5c9a7c7ec1c",
    ),
    # ColorOS 15 PKG110_COS_15.0.0.840 exchangeHardwareBufferBetweenBufferQ
    # (mov x3 is the 3rd instruction: offset byte 10)
    "08830734d4d8baeac59664f94db5ce2c5b78c0d008c9ea5d504db5ddbef61b11": (
        bytes.fromhex(
            "e5030091"  # add x5, sp, #0
            "e2031faa"  # mov x2, xzr
            "e3031faa"  # mov x3, xzr
            "081d40f9"  # ldr x8, [x8, #0x38]
            "e4031faa"  # mov x4, xzr
            "00013fd6"  # blr x8
        ),
        10,
        "0a7d5a5c40a087181b2e83651f670c800429fb7aca4f6e1bd6cad1a3e75c3d3e",
    ),
}


class NativeWinBuffExchangeFixupError(RuntimeError):
    pass


def patch_native_win_buff_exchange(blob: bytes) -> bytes:
    """Patch releaseBuffer call from legacy 5-arg ABI to modern 3-arg ABI."""

    stock_sha256 = sha256(blob).hexdigest()
    entry = _CALLSEQUENCES.get(stock_sha256)
    if entry is None:
        raise NativeWinBuffExchangeFixupError(
            f"libNativeWinBuffExchange: unknown blob generation "
            f"(stock sha256 {stock_sha256})"
        )

    call_sequence, patch_offset, expected_patched_sha256 = entry

    count = blob.count(call_sequence)
    if count == 0:
        raise NativeWinBuffExchangeFixupError(
            "libNativeWinBuffExchange: releaseBuffer call sequence not found"
        )
    if count > 1:
        raise NativeWinBuffExchangeFixupError(
            f"libNativeWinBuffExchange: call sequence found {count} times "
            "(expected exactly 1)"
        )

    offset = blob.index(call_sequence) + patch_offset
    if blob[offset] != _STOCK_BYTE:
        raise NativeWinBuffExchangeFixupError(
            f"libNativeWinBuffExchange: byte at {offset:#x} is "
            f"{blob[offset]:#04x}, expected {_STOCK_BYTE:#04x}"
        )

    patched = bytearray(blob)
    patched[offset] = _PATCHED_BYTE

    result = bytes(patched)
    actual_patched_sha256 = sha256(result).hexdigest()
    if actual_patched_sha256 != expected_patched_sha256:
        raise NativeWinBuffExchangeFixupError(
            f"libNativeWinBuffExchange: patched sha256 mismatch: "
            f"expected {expected_patched_sha256}, "
            f"found {actual_patched_sha256}"
        )
    return result


def patch_native_win_buff_exchange_file(file_path: str) -> None:
    path = Path(file_path)
    path.write_bytes(patch_native_win_buff_exchange(path.read_bytes()))
