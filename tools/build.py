#!/usr/bin/env python3
"""Gera os arquivos de cor do Arkmos Night a partir da paleta Tokyo Night.

A paleta fica só aqui. Tudo o que tem cor no repositório sai deste script:

    color-schemes/ArkmosNight.colors              esquema de cores do KDE
    plasma/desktoptheme/arkmos-night/colors       cores do estilo do Plasma
    konsole/ArkmosNight.colorscheme               cores do Konsole
    docs/preview.svg (+ .png)                     imagem de prévia
    plasma/look-and-feel/.../previews/            prévias do tema global

Uso, a partir da raiz do repositório:

    python3 tools/build.py

As prévias em PNG/JPG precisam do ImageMagick (comando `magick`). Sem ele, o
script gera só os arquivos de cor e o SVG da prévia.
"""
import shutil
import subprocess
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
LNF_ID = "com.github.alexrogaleski.arkmosnight"

# Tokyo Night, variante Night (folke/tokyonight.nvim)
P = {
    "black":          "#15161e",
    "bg_dark":        "#16161e",
    "bg":             "#1a1b26",
    "bg_hl":          "#292e42",
    "fg_gutter":      "#3b4261",
    "terminal_black": "#414868",
    "comment":        "#565f89",
    "dark5":          "#737aa2",
    "fg_dark":        "#a9b1d6",
    "fg":             "#c0caf5",
    "blue0":          "#3d59a1",
    "blue":           "#7aa2f7",
    "cyan":           "#7dcfff",
    "magenta":        "#bb9af7",
    "red":            "#f7768e",
    "orange":         "#ff9e64",
    "yellow":         "#e0af68",
    "green":          "#9ece6a",
    "teal":           "#73daca",
    # cores brilhantes do terminal
    "br_red":         "#ff899d",
    "br_green":       "#9fe044",
    "br_yellow":      "#faba4a",
    "br_blue":        "#8db0ff",
    "br_magenta":     "#c7a9ff",
    "br_cyan":        "#a4daff",
    # tons da variante Day, para texto sobre a seleção azul clara
    "day_red":        "#c64343",
    "day_yellow":     "#8c6c3e",
    "day_green":      "#387068",
    "day_purple":     "#7847bd",
}


def rgb(h):
    h = h.lstrip("#")
    return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def mix(a, b, t):
    """Mistura a cor a com b; t=1 devolve a, t=0 devolve b."""
    a, b = a.lstrip("#"), b.lstrip("#")
    out = []
    for i in (0, 2, 4):
        x, y = int(a[i:i + 2], 16), int(b[i:i + 2], 16)
        out.append(round(x * t + y * (1 - t)))
    return "#" + "".join(f"{c:02x}" for c in out)


def write(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print("  ", rel)


# --------------------------------------------------------------------------
# Esquema de cores do KDE
# --------------------------------------------------------------------------

def group(bg, bg_alt, fg=P["fg"], inactive=P["dark5"]):
    return {
        "BackgroundAlternate": bg_alt,
        "BackgroundNormal": bg,
        "DecorationFocus": P["blue"],
        "DecorationHover": P["blue"],
        "ForegroundActive": P["blue"],
        "ForegroundInactive": inactive,
        "ForegroundLink": P["blue"],
        "ForegroundNegative": P["red"],
        "ForegroundNeutral": P["yellow"],
        "ForegroundNormal": fg,
        "ForegroundPositive": P["green"],
        "ForegroundVisited": P["magenta"],
    }


def color_scheme():
    sections = {
        # Botões um tom acima do fundo, para se destacarem da janela.
        "Colors:Button": group(P["bg_hl"], P["fg_gutter"]),
        "Colors:Complementary": group(P["bg_dark"], P["bg"]),
        # Barra de título e barras de ferramentas.
        "Colors:Header": group(P["bg_dark"], P["bg"]),
        "Colors:Header][Inactive": group(P["bg_dark"], P["bg"], fg=P["fg_dark"], inactive=P["comment"]),
        # Seleção em azul claro com texto escuro.
        "Colors:Selection": {
            "BackgroundAlternate": P["blue0"],
            "BackgroundNormal": P["blue"],
            "DecorationFocus": P["blue"],
            "DecorationHover": P["cyan"],
            "ForegroundActive": P["bg_dark"],
            "ForegroundInactive": P["bg_hl"],
            "ForegroundLink": P["bg_dark"],
            "ForegroundNegative": P["day_red"],
            "ForegroundNeutral": P["day_yellow"],
            "ForegroundNormal": P["bg_dark"],
            "ForegroundPositive": P["day_green"],
            "ForegroundVisited": P["day_purple"],
        },
        "Colors:Tooltip": group(P["bg_dark"], P["bg"]),
        # Listas e campos de texto mais escuros que a janela, como no Breeze.
        "Colors:View": group(P["bg_dark"], P["bg"]),
        "Colors:Window": group(P["bg"], P["bg_dark"]),
    }

    out = ["""[ColorEffects:Disabled]
Color=56,56,56
ColorAmount=0
ColorEffect=0
ContrastAmount=0.65
ContrastEffect=1
IntensityAmount=0.1
IntensityEffect=2

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color=112,111,110
ColorAmount=0.025
ColorEffect=2
ContrastAmount=0.1
ContrastEffect=2
Enable=false
IntensityAmount=0
IntensityEffect=0
"""]
    for name, keys in sections.items():
        out.append(f"[{name}]")
        out += [f"{k}={rgb(keys[k])}" for k in sorted(keys)]
        out.append("")

    out.append(f"""[General]
ColorScheme=ArkmosNight
Name=Arkmos Night
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground={rgb(P['bg_dark'])}
activeBlend={rgb(P['fg'])}
activeForeground={rgb(P['fg'])}
inactiveBackground={rgb(P['bg_dark'])}
inactiveBlend={rgb(P['comment'])}
inactiveForeground={rgb(P['comment'])}
""")
    return "\n".join(out)


# --------------------------------------------------------------------------
# Konsole
# --------------------------------------------------------------------------

def konsole():
    # (normal, intenso) para as cores 0 a 7
    ansi = [
        (P["black"], P["terminal_black"]),
        (P["red"], P["br_red"]),
        (P["green"], P["br_green"]),
        (P["yellow"], P["br_yellow"]),
        (P["blue"], P["br_blue"]),
        (P["magenta"], P["br_magenta"]),
        (P["cyan"], P["br_cyan"]),
        (P["fg_dark"], P["fg"]),
    ]
    out = []

    def entry(name, color):
        out.append(f"[{name}]\nColor={rgb(color)}\n")

    entry("Background", P["bg"])
    entry("BackgroundFaint", P["bg"])
    entry("BackgroundIntense", P["bg"])
    for i, (normal, intense) in enumerate(ansi):
        entry(f"Color{i}", normal)
        entry(f"Color{i}Faint", mix(normal, P["bg"], 0.6))
        entry(f"Color{i}Intense", intense)
    entry("Foreground", P["fg"])
    entry("ForegroundFaint", P["dark5"])
    entry("ForegroundIntense", P["fg"])
    out.append("""[General]
Anchor=0.5,0.5
Blur=false
ColorRandomization=false
Description=Arkmos Night
FillStyle=Tile
Opacity=1
Wallpaper=
WallpaperFlipType=NoFlip
WallpaperOpacity=1
""")
    return "\n".join(out)


# --------------------------------------------------------------------------
# Prévia (desenho ilustrativo, não é captura de tela)
# --------------------------------------------------------------------------

PREVIEW = Template("""<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080" font-family="Noto Sans, Adwaita Sans, sans-serif">
  <defs>
    <radialGradient id="glow1" cx="22%" cy="18%" r="65%">
      <stop offset="0" stop-color="${blue0}" stop-opacity=".45"/>
      <stop offset="1" stop-color="${blue0}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="88%" cy="90%" r="55%">
      <stop offset="0" stop-color="${magenta}" stop-opacity=".22"/>
      <stop offset="1" stop-color="${magenta}" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#000" flood-opacity=".5"/>
    </filter>
    <clipPath id="w1"><rect x="180" y="110" width="1100" height="720" rx="8"/></clipPath>
    <clipPath id="w2"><rect x="1010" y="400" width="760" height="480" rx="8"/></clipPath>
  </defs>

  <!-- fundo -->
  <rect width="1920" height="1080" fill="${bg_dark}"/>
  <rect width="1920" height="1080" fill="url(#glow1)"/>
  <rect width="1920" height="1080" fill="url(#glow2)"/>

  <!-- janela 1: gerenciador de arquivos -->
  <g filter="url(#shadow)">
    <rect x="180" y="110" width="1100" height="720" rx="8" fill="${bg}"/>
  </g>
  <g clip-path="url(#w1)">
    <rect x="180" y="110" width="1100" height="92" fill="${bg_dark}"/>
    <text x="730" y="135" font-size="15" fill="${fg}" text-anchor="middle">Arkmos Night</text>
    <g stroke="${fg}" stroke-width="2" stroke-linecap="round" fill="none">
      <path d="M1180 129 h12"/>
      <rect x="1211" y="123" width="12" height="12" rx="1"/>
      <path d="M1244 123 l12 12 M1256 123 l-12 12"/>
    </g>
    <!-- barra de ferramentas -->
    <g stroke="${fg_dark}" stroke-width="2" stroke-linecap="round" fill="none">
      <path d="M210 175 l-8 -7 8 -7 M240 175 l8 -7 -8 -7"/>
    </g>
    <rect x="280" y="155" width="600" height="30" rx="4" fill="${bg}" stroke="${bg_hl}"/>
    <text x="296" y="175" font-size="14" fill="${fg_dark}">Pessoal  ›  Projetos  ›  arkmos-night-kde</text>
    <rect x="1080" y="155" width="180" height="30" rx="4" fill="${bg}" stroke="${bg_hl}"/>
    <text x="1096" y="175" font-size="14" fill="${comment}">Pesquisar…</text>

    <!-- lateral -->
    <rect x="180" y="202" width="240" height="628" fill="${bg}"/>
    <text x="200" y="232" font-size="12" fill="${dark5}" font-weight="bold">LOCAIS</text>
    $sidebar
    <!-- lista -->
    <rect x="420" y="202" width="860" height="580" fill="${bg_dark}"/>
    <rect x="420" y="202" width="860" height="34" fill="${bg}"/>
    <text x="456" y="224" font-size="13" fill="${dark5}">Nome</text>
    <text x="900" y="224" font-size="13" fill="${dark5}">Tamanho</text>
    <text x="1060" y="224" font-size="13" fill="${dark5}">Modificado</text>
    $rows
    <!-- barra de status -->
    <rect x="420" y="782" width="860" height="48" fill="${bg}"/>
    <text x="440" y="811" font-size="13" fill="${fg_dark}">7 itens, 2 pastas</text>
    <rect x="980" y="804" width="200" height="4" rx="2" fill="${bg_hl}"/>
    <rect x="980" y="804" width="120" height="4" rx="2" fill="${blue}"/>
    <circle cx="1100" cy="806" r="8" fill="${fg}" stroke="${blue}" stroke-width="2"/>
    <rect x="1200" y="794" width="60" height="24" rx="4" fill="${bg_hl}"/>
    <text x="1230" y="811" font-size="13" fill="${fg}" text-anchor="middle">Ok</text>
  </g>

  <!-- janela 2: terminal -->
  <g filter="url(#shadow)">
    <rect x="1010" y="400" width="760" height="480" rx="8" fill="${bg}"/>
  </g>
  <g clip-path="url(#w2)">
    <rect x="1010" y="400" width="760" height="38" fill="${bg_dark}"/>
    <text x="1390" y="425" font-size="15" fill="${fg}" text-anchor="middle">Konsole</text>
    <g stroke="${fg}" stroke-width="2" stroke-linecap="round" fill="none">
      <path d="M1670 419 h12"/>
      <rect x="1701" y="413" width="12" height="12" rx="1"/>
      <path d="M1734 413 l12 12 M1746 413 l-12 12"/>
    </g>
    <g font-family="Hack, JetBrains Mono, Noto Sans Mono, monospace" font-size="17" xml:space="preserve">
      <text x="1036" y="480"><tspan fill="${magenta}">❯</tspan><tspan fill="${fg}"> arkmos-night --cores</tspan></text>
      $swatches
      <text x="1036" y="640"><tspan fill="${magenta}">❯</tspan><tspan fill="${fg}"> git log --oneline</tspan></text>
      <text x="1036" y="672"><tspan fill="${yellow}">3f9c2a1</tspan><tspan fill="${cyan}"> (HEAD → main)</tspan><tspan fill="${fg}"> Arkmos Night: tema global</tspan></text>
      <text x="1036" y="702"><tspan fill="${yellow}">8b1e07d</tspan><tspan fill="${fg}"> Cursor Bibata Modern Ice</tspan></text>
      <text x="1036" y="732"><tspan fill="${yellow}">c47d5e9</tspan><tspan fill="${fg}"> Paleta Tokyo Night</tspan></text>
      <text x="1036" y="780"><tspan fill="${green}">✓</tspan><tspan fill="${fg_dark}"> instalado em </tspan><tspan fill="${blue}">~/.local/share</tspan></text>
      <text x="1036" y="828"><tspan fill="${magenta}">❯</tspan><tspan fill="${fg}"> </tspan><tspan fill="${fg}">▌</tspan></text>
    </g>
  </g>

  <!-- painel flutuante -->
  <g filter="url(#shadow)">
    <rect x="610" y="1004" width="700" height="52" rx="10" fill="${bg_dark}" stroke="${bg_hl}"/>
  </g>
  <rect x="626" y="1014" width="32" height="32" rx="8" fill="${blue}"/>
  <path d="M634 1038 l8 -16 8 16 M637 1032 h10" stroke="${bg_dark}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  $tasks
  <text x="1290" y="1028" font-size="14" fill="${fg}" text-anchor="end">14:32</text>
  <text x="1290" y="1046" font-size="11" fill="${dark5}" text-anchor="end">11/11/2026</text>
</svg>
""")


def preview_svg():
    sidebar = []
    places = ["Pessoal", "Área de trabalho", "Documentos", "Downloads", "Imagens", "Projetos", "Lixeira"]
    for i, name in enumerate(places):
        y = 250 + i * 40
        if name == "Projetos":
            sidebar.append(f'<rect x="188" y="{y}" width="224" height="34" rx="4" fill="{P["blue"]}"/>')
            color, icon = P["bg_dark"], P["bg_dark"]
        else:
            color, icon = P["fg"], P["blue"]
        sidebar.append(f'<rect x="202" y="{y + 9}" width="16" height="14" rx="2" fill="{icon}"/>')
        sidebar.append(f'<text x="230" y="{y + 22}" font-size="14" fill="{color}">{name}</text>')

    files = [
        ("color-schemes", "pasta", "11/11 14:20", True),
        ("plasma", "pasta", "11/11 14:20", True),
        ("konsole", "pasta", "11/11 14:20", True),
        ("tools", "pasta", "11/11 14:18", True),
        ("install.sh", "4,1 KiB", "11/11 14:25", False),
        ("README.md", "5,6 KiB", "11/11 14:30", False),
        ("LICENSE", "1,1 KiB", "11/11 14:10", False),
    ]
    rows = []
    for i, (name, size, date, folder) in enumerate(files):
        y = 236 + i * 38
        if i % 2:
            rows.append(f'<rect x="420" y="{y}" width="860" height="38" fill="{P["bg"]}" opacity=".6"/>')
        if name == "plasma":
            rows.append(f'<rect x="426" y="{y + 2}" width="848" height="34" rx="4" fill="{P["blue"]}" fill-opacity=".18" stroke="{P["blue"]}"/>')
        icon = P["blue"] if folder else P["fg_gutter"]
        rows.append(f'<rect x="440" y="{y + 11}" width="16" height="16" rx="2" fill="{icon}"/>')
        rows.append(f'<text x="468" y="{y + 24}" font-size="14" fill="{P["fg"]}">{name}</text>')
        rows.append(f'<text x="900" y="{y + 24}" font-size="14" fill="{P["dark5"]}">{size}</text>')
        rows.append(f'<text x="1060" y="{y + 24}" font-size="14" fill="{P["dark5"]}">{date}</text>')

    normal = [P["black"], P["red"], P["green"], P["yellow"], P["blue"], P["magenta"], P["cyan"], P["fg_dark"]]
    bright = [P["terminal_black"], P["br_red"], P["br_green"], P["br_yellow"], P["br_blue"], P["br_magenta"], P["br_cyan"], P["fg"]]
    swatches = []
    for row, colors in enumerate((normal, bright)):
        for i, c in enumerate(colors):
            swatches.append(f'<rect x="{1036 + i * 86}" y="{500 + row * 52}" width="78" height="42" rx="4" fill="{c}"/>')

    tasks = []
    for i, c in enumerate([P["fg_dark"], P["magenta"], P["green"], P["orange"], P["cyan"]]):
        x = 690 + i * 52
        tasks.append(f'<rect x="{x}" y="{1014}" width="32" height="32" rx="8" fill="{c}" fill-opacity=".85"/>')
        if i == 1:
            tasks.append(f'<rect x="{x + 6}" y="1050" width="20" height="3" rx="1.5" fill="{P["blue"]}"/>')

    return PREVIEW.substitute(
        P, sidebar="\n    ".join(sidebar), rows="\n    ".join(rows),
        swatches="\n      ".join(swatches), tasks="\n  ".join(tasks),
    )


def render_previews():
    magick = shutil.which("magick")
    if not magick:
        print("   (sem ImageMagick: prévias em PNG/JPG não foram geradas)")
        return
    svg = ROOT / "docs/preview.svg"
    png = ROOT / "docs/preview.png"
    previews = ROOT / "plasma/look-and-feel" / LNF_ID / "contents/previews"
    previews.mkdir(parents=True, exist_ok=True)
    subprocess.run([magick, "-background", "none", str(svg), str(png)], check=True)
    subprocess.run([magick, str(png), "-quality", "90", str(previews / "fullscreenpreview.jpg")], check=True)
    subprocess.run([magick, str(png), "-resize", "640x360", str(previews / "preview.png")], check=True)
    for p in (png, previews / "fullscreenpreview.jpg", previews / "preview.png"):
        print("  ", p.relative_to(ROOT))


def main():
    print("Gerando arquivos:")
    scheme = color_scheme()
    write("color-schemes/ArkmosNight.colors", scheme)
    write("plasma/desktoptheme/arkmos-night/colors", scheme)
    write("konsole/ArkmosNight.colorscheme", konsole())
    write("docs/preview.svg", preview_svg())
    render_previews()


if __name__ == "__main__":
    main()
