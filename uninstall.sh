#!/usr/bin/env bash
#
# Remove o Arkmos Night de ~/.local/share. O que estiver em uso volta para o
# Breeze Dark antes de ser apagado.
#
# O cursor Bibata Modern Ice fica instalado, porque outros temas podem usá-lo.

set -euo pipefail

DATA="${XDG_DATA_HOME:-$HOME/.local/share}"

LNF_ID="com.github.alexrogaleski.arkmosnight"
PLASMA_ID="arkmos-night"

read_kde() { kreadconfig6 --file "$1" --group "$2" --key "$3" 2>/dev/null || true; }

if [[ "$(read_kde kdeglobals KDE LookAndFeelPackage)" == "$LNF_ID" ]]; then
    echo "==> Voltando para o tema global Breeze Dark"
    plasma-apply-lookandfeel --apply org.kde.breezedark.desktop
fi
if [[ "$(read_kde kdeglobals General ColorScheme)" == "ArkmosNight" ]]; then
    echo "==> Voltando para o esquema de cores Breeze Dark"
    plasma-apply-colorscheme BreezeDark
fi
if [[ "$(read_kde plasmarc Theme name)" == "$PLASMA_ID" ]]; then
    echo "==> Voltando para o estilo do Plasma Breeze"
    plasma-apply-desktoptheme default
fi

echo "==> Removendo arquivos"
rm -rf "$DATA/plasma/look-and-feel/$LNF_ID" "$DATA/plasma/desktoptheme/$PLASMA_ID"
rm -f "$DATA/color-schemes/ArkmosNight.colors" "$DATA/konsole/ArkmosNight.colorscheme"

echo
echo "Pronto. O cursor continua em $DATA/icons/Bibata-Modern-Ice; apague essa pasta se não for usar."
