#!/usr/bin/env python3
"""Build dial/aod_ticks.png: the 12 hour markers from dial/dial_current.png, in white.

Removes the minute ticks by angle, then rescales brightness so the markers reach
full white, with their anti-aliased edges kept as alpha. Standard library only.

Usage: python3 tools/make_aod_ticks.py dial/dial_current.png dial/aod_ticks.png
"""
import math
import struct
import sys
import zlib

WINDOW_DEGREES = 3.0  # Hour markers fit inside this; minute ticks sit 6 degrees away.
MIN_LEVEL = 8  # Anything darker is background.


def read_rgb_png(path):
    data = open(path, "rb").read()
    pos, idat = 8, b""
    while pos < len(data):
        size = struct.unpack(">I", data[pos:pos + 4])[0]
        kind, body = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + size]
        pos += 12 + size
        if kind == b"IHDR":
            width, height, depth, color, _, _, interlace = struct.unpack(">IIBBBBB", body)
        elif kind == b"IDAT":
            idat += body
    if (depth, color, interlace) != (8, 2, 0):
        raise SystemExit("expected an 8-bit RGB, non-interlaced PNG")
    raw, stride, offset, prev, rows = zlib.decompress(idat), width * 3, 0, bytearray(width * 3), []
    for _ in range(height):
        kind, row = raw[offset], bytearray(raw[offset + 1:offset + 1 + stride])
        offset += 1 + stride
        for i in range(stride):
            a = row[i - 3] if i >= 3 else 0
            b = prev[i]
            c = prev[i - 3] if i >= 3 else 0
            if kind == 1:
                row[i] = (row[i] + a) & 255
            elif kind == 2:
                row[i] = (row[i] + b) & 255
            elif kind == 3:
                row[i] = (row[i] + (a + b) // 2) & 255
            elif kind == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                row[i] = (row[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(row)
        prev = row
    return width, height, rows


def write_rgba_png(path, width, height, pixels):
    def chunk(kind, body):
        crc = zlib.crc32(kind + body) & 0xFFFFFFFF
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", crc)

    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    with open(path, "wb") as out:
        out.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                  + chunk(b"IDAT", zlib.compress(bytes(pixels), 9)) + chunk(b"IEND", b""))


def main(source, target):
    width, height, rows = read_rgb_png(source)
    center = (width - 1) / 2

    def is_marker(x, y):
        angle = math.degrees(math.atan2(x - center, center - y)) % 360
        return abs(((angle + 15) % 30) - 15) <= WINDOW_DEGREES

    peak = max(rows[y][x * 3] for y in range(height) for x in range(width)
               if rows[y][x * 3] > MIN_LEVEL and is_marker(x, y))
    pixels = bytearray()
    for y in range(height):
        pixels.append(0)
        for x in range(width):
            level = rows[y][x * 3]
            if level > MIN_LEVEL and is_marker(x, y):
                pixels += bytes((255, 255, 255, min(255, level * 255 // peak)))
            else:
                pixels += bytes((0, 0, 0, 0))
    write_rgba_png(target, width, height, pixels)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
