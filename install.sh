#!/usr/bin/env bash
#
# Instala o Arkmos Night para o usuário atual, em ~/.local/share. Não usa sudo.
#
#   ./install.sh               instala o tema e o cursor
#   ./install.sh --apply       instala e já aplica o tema global
#   ./install.sh --no-cursor   não baixa o cursor Bibata Modern Ice
#
# O cursor vem do release oficial do Bibata, com versão e SHA256 fixados (os
# mesmos do Arkmos): se o arquivo servido mudar, a instalação para.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"

LNF_ID="com.github.alexrogaleski.arkmosnight"
PLASMA_ID="arkmos-night"

CURSOR="Bibata-Modern-Ice"
BIBATA_VERSION="2.0.7"
BIBATA_SHA256="a68cae60c4dc706350e194ebc91c5fe48bc7bc9d59e119555834a2a7ee5078ef"

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

echo "==> Esquema de cores"
install -Dm644 "$REPO/color-schemes/ArkmosNight.colors" "$DATA/color-schemes/ArkmosNight.colors"

echo "==> Estilo do Plasma"
copy_dir "$REPO/plasma/desktoptheme/$PLASMA_ID" "$DATA/plasma/desktoptheme/$PLASMA_ID"

echo "==> Tema global"
copy_dir "$REPO/plasma/look-and-feel/$LNF_ID" "$DATA/plasma/look-and-feel/$LNF_ID"

echo "==> Cores do Konsole"
install -Dm644 "$REPO/konsole/ArkmosNight.colorscheme" "$DATA/konsole/ArkmosNight.colorscheme"

if (( cursor )); then
    if [[ -f "$DATA/icons/$CURSOR/index.theme" || -f "/usr/share/icons/$CURSOR/index.theme" ]]; then
        echo "==> Cursor $CURSOR já instalado"
    else
        echo "==> Cursor $CURSOR $BIBATA_VERSION"
        work="$(mktemp -d)"
        trap 'rm -rf "$work"' EXIT
        curl -fsSL --retry 5 --retry-delay 10 --retry-all-errors --connect-timeout 20 \
            -o "$work/$CURSOR.tar.xz" \
            "https://github.com/ful1e5/Bibata_Cursor/releases/download/v${BIBATA_VERSION}/${CURSOR}.tar.xz"

        got="$(sha256sum "$work/$CURSOR.tar.xz" | cut -d' ' -f1)"
        if [[ "$got" != "$BIBATA_SHA256" ]]; then
            echo "ERRO: checksum do cursor não confere." >&2
            echo "  esperado: $BIBATA_SHA256" >&2
            echo "  obtido:   $got" >&2
            exit 1
        fi

        mkdir -p "$DATA/icons"
        tar -xJf "$work/$CURSOR.tar.xz" -C "$DATA/icons" "$CURSOR/"
        test -e "$DATA/icons/$CURSOR/cursors/left_ptr"
        echo "    $(find "$DATA/icons/$CURSOR/cursors" -mindepth 1 | wc -l) cursores instalados"
    fi
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
