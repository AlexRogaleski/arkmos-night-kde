#!/usr/bin/env bash
#
# Instala o Arkmos Night para o usuário atual, em ~/.local/share. Não usa sudo.
#
#   ./install.sh               instala o tema e os cursores
#   ./install.sh --apply       instala e já aplica o tema global
#   ./install.sh --no-cursor   não baixa os cursores Bibata
#
# Os cursores vêm do release oficial do Bibata, com versão e SHA256 fixados:
# se o arquivo servido mudar, a instalação para.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"

LNF_ID="com.github.alexrogaleski.arkmosnight"
PLASMA_ID="arkmos-night"

# O release do Bibata não publica checksum. O do Ice é o mesmo fixado no Arkmos
# (calculado em 2026-09-24); o do Classic foi calculado no download de
# 2026-11-11. O Ice é o cursor do tema global; o Classic fica disponível para
# escolher em Configurações do sistema → Cursores.
BIBATA_VERSION="2.0.7"
CURSORS=(
    "Bibata-Modern-Ice      a68cae60c4dc706350e194ebc91c5fe48bc7bc9d59e119555834a2a7ee5078ef"  # branco
    "Bibata-Modern-Classic  7d3495864e5bbef02f5e77de760b2905903b63c71495a78ef6306d19a3b556d8"  # preto
)

apply=0
cursor=1
for arg in "$@"; do
    case "$arg" in
        --apply) apply=1 ;;
        --no-cursor) cursor=0 ;;
        -h|--help) sed -n '3,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "Opção desconhecida: $arg (veja --help)" >&2; exit 2 ;;
    esac
done

# Substitui a pasta inteira, para não sobrar arquivo de uma versão antiga.
copy_dir() {
    rm -rf "$2"
    mkdir -p "$(dirname "$2")"
    cp -r "$1" "$2"
}

install_cursor() {
    local name="$1" sha="$2" got
    if [[ -f "$DATA/icons/$name/index.theme" || -f "/usr/share/icons/$name/index.theme" ]]; then
        echo "==> Cursor $name já instalado"
    else
        echo "==> Cursor $name $BIBATA_VERSION"
        curl -fsSL --retry 5 --retry-delay 10 --retry-all-errors --connect-timeout 20 \
            -o "$work/$name.tar.xz" \
            "https://github.com/ful1e5/Bibata_Cursor/releases/download/v${BIBATA_VERSION}/${name}.tar.xz"

        got="$(sha256sum "$work/$name.tar.xz" | cut -d' ' -f1)"
        if [[ "$got" != "$sha" ]]; then
            echo "ERRO: checksum do cursor $name não confere." >&2
            echo "  esperado: $sha" >&2
            echo "  obtido:   $got" >&2
            exit 1
        fi

        mkdir -p "$DATA/icons"
        tar -xJf "$work/$name.tar.xz" -C "$DATA/icons" "$name/"
        test -e "$DATA/icons/$name/cursors/left_ptr"
        echo "    $(find "$DATA/icons/$name/cursors" -mindepth 1 | wc -l) cursores instalados"
    fi

    # A pasta fica em ~/.local/share/icons, que é onde os apps Flatpak procuram.
    # A tela de cursores das Configurações do sistema (e o
    # plasma-apply-cursortheme) não procura lá, só em ~/.icons: sem este link o
    # cursor funciona, mas não aparece na lista para escolher.
    if [[ -d "$DATA/icons/$name" && ! -e "$HOME/.icons/$name" ]]; then
        mkdir -p "$HOME/.icons"
        ln -s "$DATA/icons/$name" "$HOME/.icons/$name"
    fi
}

echo "==> Esquema de cores"
install -Dm644 "$REPO/color-schemes/ArkmosNight.colors" "$DATA/color-schemes/ArkmosNight.colors"

echo "==> Estilo do Plasma"
copy_dir "$REPO/plasma/desktoptheme/$PLASMA_ID" "$DATA/plasma/desktoptheme/$PLASMA_ID"

echo "==> Tema global"
copy_dir "$REPO/plasma/look-and-feel/$LNF_ID" "$DATA/plasma/look-and-feel/$LNF_ID"

echo "==> Cores do Konsole"
install -Dm644 "$REPO/konsole/ArkmosNight.colorscheme" "$DATA/konsole/ArkmosNight.colorscheme"

if (( cursor )); then
    work="$(mktemp -d)"
    trap 'rm -rf "$work"' EXIT
    for entry in "${CURSORS[@]}"; do
        read -r name sha <<<"$entry"
        install_cursor "$name" "$sha"
    done
fi

if (( apply )); then
    echo "==> Aplicando o tema global"
    plasma-apply-lookandfeel --apply "$LNF_ID"
else
    echo
    echo "Pronto. Para aplicar: Configurações do sistema → Cores e temas → Tema global → Arkmos Night"
    echo "ou rode: plasma-apply-lookandfeel --apply $LNF_ID"
fi

# Uma cor de destaque personalizada passa por cima do esquema de cores.
accent="$(kreadconfig6 --file kdeglobals --group General --key AccentColor 2>/dev/null || true)"
if [[ -n "$accent" ]]; then
    echo
    echo "Aviso: há uma cor de destaque personalizada ($accent) que substitui o azul do tema."
    echo "Para usar a do tema: Cores e temas → Cores → Cor de destaque → Do esquema de cores."
fi
