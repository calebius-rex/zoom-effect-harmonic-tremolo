"""Draw and encode the Harmonic pedal cover as Zoom's 128x64 1-bpp RLE."""

from __future__ import annotations

W, H = 128, 64

# Small 3x5 font: enough for the title and control labels on the LCD.
FONT = {
    "A": ("010", "101", "111", "101", "101"),
    "C": ("011", "100", "100", "100", "011"),
    "D": ("110", "101", "101", "101", "110"),
    "E": ("111", "100", "110", "100", "111"),
    "H": ("101", "101", "111", "101", "101"),
    "I": ("111", "010", "010", "010", "111"),
    "M": ("101", "111", "111", "101", "101"),
    "P": ("110", "101", "110", "100", "100"),
    "R": ("110", "101", "110", "101", "101"),
    "T": ("111", "010", "010", "010", "010"),
    " ": ("000", "000", "000", "000", "000"),
}


class Canvas:
    def __init__(self) -> None:
        self.pixels = [[0] * W for _ in range(H)]

    def px(self, x: int, y: int, value: int = 1) -> None:
        if 0 <= x < W and 0 <= y < H:
            self.pixels[y][x] = 1 if value else 0

    def hline(self, x0: int, x1: int, y: int, value: int = 1) -> None:
        if x0 > x1:
            x0, x1 = x1, x0
        for x in range(x0, x1 + 1):
            self.px(x, y, value)

    def vline(self, x: int, y0: int, y1: int, value: int = 1) -> None:
        if y0 > y1:
            y0, y1 = y1, y0
        for y in range(y0, y1 + 1):
            self.px(x, y, value)

    def line(self, x0: int, y0: int, x1: int, y1: int, value: int = 1) -> None:
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        error = dx + dy
        while True:
            self.px(x0, y0, value)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * error
            if e2 >= dy:
                error += dy
                x0 += sx
            if e2 <= dx:
                error += dx
                y0 += sy

    def rect(self, x0: int, y0: int, x1: int, y1: int, value: int = 1) -> None:
        self.hline(x0, x1, y0, value)
        self.hline(x0, x1, y1, value)
        self.vline(x0, y0, y1, value)
        self.vline(x1, y0, y1, value)

    def circle(self, cx: int, cy: int, radius: int, value: int = 1) -> None:
        x, y, error = radius, 0, 0
        while x >= y:
            for px, py in ((x, y), (y, x), (-y, x), (-x, y),
                           (-x, -y), (-y, -x), (y, -x), (x, -y)):
                self.px(cx + px, cy + py, value)
            y += 1
            if error <= 0:
                error += 2 * y + 1
            if error > 0:
                x -= 1
                error -= 2 * x + 1

    def text(self, text: str, x: int, y: int, scale: int = 1,
             spacing: int = 1, value: int = 1) -> None:
        for char in text.upper():
            for row, bits in enumerate(FONT.get(char, FONT[" "])):
                for col, bit in enumerate(bits):
                    if bit == "1":
                        for sy in range(scale):
                            for sx in range(scale):
                                self.px(x + col * scale + sx,
                                        y + row * scale + sy, value)
            x += 3 * scale + spacing


def _draw_cover() -> Canvas:
    c = Canvas()
    c.rect(1, 1, 126, 62)

    # Inverse-video title bar, a common visual cue in the reference pack.
    for y in range(2, 15):
        c.hline(2, 125, y)
    title = "HARMONIC"
    scale, spacing = 2, 1
    width = len(title) * (3 * scale + spacing) - spacing
    c.text(title, (W - width) // 2, 5, scale=scale, spacing=spacing, value=0)

    # Fine monochrome grid and paired, alternating harmonic-tremolo traces.
    for x in range(12, 120, 12):
        for y in range(17, 35, 4):
            c.px(x, y)
    for y in (18, 26, 34):
        c.hline(9, 118, y)

    upper = [(10, 25), (17, 25), (22, 20), (27, 30), (32, 20),
             (38, 29), (44, 21), (50, 27), (56, 20), (62, 30),
             (68, 21), (74, 27), (80, 25), (86, 25), (92, 20),
             (98, 30), (104, 21), (110, 28), (118, 20)]
    lower = [(x, y + 7) for x, y in upper]
    for points in (upper, lower):
        for a, b in zip(points, points[1:]):
            c.line(a[0], a[1], b[0], b[1])

    # Vertical beat markers distinguish the two out-of-phase bands.
    for x, top, bottom in ((16, 20, 33), (32, 18, 34), (48, 20, 33),
                           (64, 18, 34), (80, 20, 33), (96, 18, 34),
                           (112, 20, 33)):
        c.vline(x, top, bottom)

    # Three control legends and dial marks, placed clear of the value boxes.
    for cx, label in ((24, "RATE"), (65, "DEPTH"), (106, "MIX")):
        label_width = len(label) * 4 - 1
        c.text(label, cx - label_width // 2, 38)
        c.circle(cx, 53, 5)
        c.line(cx, 53, cx, 49)

    return c


def encode_zoom_rle(canvas: Canvas) -> bytes:
    """Encode a 128x64 monochrome canvas in the Zoom ZDL cover RLE format."""
    raw = []
    for block_y in range(8):
        for x in range(W):
            byte = 0
            for bit_y in range(8):
                if canvas.pixels[block_y * 8 + bit_y][x]:
                    byte |= 1 << bit_y
            raw.append(byte)

    encoded = bytearray()
    i = 0
    while i < len(raw):
        if i + 1 < len(raw) and raw[i] == raw[i + 1]:
            j = i + 2
            while j < len(raw) and raw[j] == raw[i] and j - i < 257:
                j += 1
            encoded.extend((raw[i], raw[i], j - i - 2))
            i = j
        else:
            encoded.append(raw[i])
            i += 1
    while len(encoded) % 4:
        encoded.append(0)
    return bytes(encoded)


def make_harmonic_cover() -> bytes:
    """Return the finished pedal image as Zoom's encoded cover bytes."""
    return encode_zoom_rle(_draw_cover())
