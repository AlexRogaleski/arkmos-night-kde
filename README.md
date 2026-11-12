# Arkmos Night

Tema global escuro para o KDE Plasma 6, com a paleta do [Tokyo Night](https://github.com/folke/tokyonight.nvim) e o cursor [Bibata Modern Ice](https://github.com/ful1e5/Bibata_Cursor), o mesmo do [Arkmos](https://github.com/AlexRogaleski/arkmos).

![Prévia do Arkmos Night](docs/preview.png)

<sub>A imagem é uma ilustração da paleta, não uma captura de tela.</sub>

## O que vem no tema

| Parte | O que é |
|---|---|
| Esquema de cores | `Arkmos Night`: janelas e barras `#1a1b26`, listas `#16161e`, texto `#c0caf5`, seleção azul `#7aa2f7`, linhas bem discretas entre os painéis |
| Estilo do Plasma | `Arkmos Night`: painel, popups e widgets com as cores do tema |
| Tema global | Junta tudo e também define o cursor e a tela de abertura |
| Tela de abertura | O nome sobre o fundo do Tokyo Night, com uma barra de progresso |
| Cursores | Bibata Modern Ice (branco, o padrão do tema) e Bibata Modern Classic (preto), versão 2.0.7, baixados do release oficial com SHA256 conferido |
| Konsole | Esquema `Arkmos Night` com as 16 cores do terminal do Tokyo Night |

Os desenhos (formatos de botões, painel e decoração das janelas) são os do Breeze, que já vem no Plasma. O estilo do Plasma tem só o arquivo de cores; o que falta, o Plasma pega do Breeze, como faz o próprio Breeze Dark. Assim nenhum arquivo do Breeze é copiado para cá e as atualizações do Plasma continuam valendo.

## Instalação

Precisa do Plasma 6. Tudo vai para `~/.local/share`, sem `sudo`, e funciona em sistemas imutáveis como Bazzite e Fedora Kinoite.

```sh
git clone https://github.com/AlexRogaleski/arkmos-night-kde.git
cd arkmos-night-kde
./install.sh --apply
```

| Opção | Efeito |
|---|---|
| (nenhuma) | Instala, mas não aplica |
| `--apply` | Instala e aplica o tema global |
| `--no-cursor` | Não baixa os cursores |

Sem `--apply`, escolha o tema em **Configurações do sistema → Cores e temas → Tema global → Arkmos Night**. Aplicar o tema não mexe no seu painel nem nos widgets, a menos que você marque a opção de layout da área de trabalho nessa tela.

### Cor de destaque

Se você escolheu uma cor de destaque em **Cores e temas → Cores**, ela passa por cima do azul do tema. O `install.sh` avisa quando isso acontece. Para usar a cor do tema, marque **Do esquema de cores** nessa tela.

### Konsole

O Konsole não segue o tema global. Para usar as cores, vá em **Configurações → Editar perfil atual → Aparência** e escolha **Arkmos Night**.

### Cursor

O tema global usa o Bibata Modern Ice, branco. Para o preto, escolha **Bibata-Modern-Classic** em **Configurações do sistema → Cores e temas → Cursores**.


O Bibata tem os tamanhos 16, 20, 22, 24, 28, 32, 40, 48 e acima. Com outro tamanho, o KDE usa o mais próximo, e o cursor pode ficar um pouco menos nítido. O tamanho se escolhe na mesma tela.

Os cursores ficam em `~/.local/share/icons`, onde os apps Flatpak procuram, e o `install.sh` cria um link para cada um em `~/.icons`, porque a tela de cursores das Configurações só procura lá. Sem o link, o cursor funciona, mas não aparece na lista.

## Remoção

```sh
./uninstall.sh
```

O que estiver em uso volta para o Breeze Dark antes de ser apagado. Os cursores ficam instalados, porque outros temas podem usar; para tirar, apague as pastas `Bibata-Modern-Ice` e `Bibata-Modern-Classic` em `~/.local/share/icons` e os links com os mesmos nomes em `~/.icons`.

## Mudando as cores

A paleta fica só em `tools/build.py`. Altere lá e gere os arquivos de novo:

```sh
python3 tools/build.py
./install.sh --apply
```

O script gera o esquema de cores, as cores do Plasma, o esquema do Konsole e as prévias. As prévias precisam do ImageMagick (`magick`).

### Linhas entre os painéis

As bordas e os separadores das janelas (entre a lateral e a lista do Dolphin, por exemplo) não têm cor própria no esquema: o Breeze mistura um pouco da cor do texto no fundo. A proporção fica em `FRAME_CONTRAST`, no `tools/build.py`. O tema usa `0.03`: a linha fica em `#1f202c`, quase a cor do fundo, e as áreas se separam mais pelos dois tons de fundo do que pela linha, mas os campos de texto mantêm a borda. Use `0` para sumir com as linhas, `0.1` para linhas discretas, `0.2` para o padrão do KDE ou um valor maior para linhas mais marcadas. O valor é decimal e vai com ponto (`0.03`), não com vírgula. Apps que já estavam abertos podem precisar ser reabertos para mostrar a mudança.

## Paleta

| Uso | Cor |
|---|---|
| Fundo das janelas, barras de título e de ferramentas, painel | `#1a1b26` |
| Listas, campos de texto | `#16161e` |
| Botões | `#292e42` |
| Texto | `#c0caf5` |
| Texto apagado | `#737aa2` |
| Seleção, foco, links | `#7aa2f7` |
| Links visitados | `#bb9af7` |
| Erro | `#f7768e` |
| Aviso | `#e0af68` |
| Sucesso | `#9ece6a` |

## Créditos

- Paleta: [Tokyo Night](https://github.com/enkia/tokyo-night-vscode-theme), de enkia, na versão de [folke/tokyonight.nvim](https://github.com/folke/tokyonight.nvim).
- Cursores: [Bibata](https://github.com/ful1e5/Bibata_Cursor), de ful1e5 (GPL-3.0). São baixados na instalação; não são distribuídos neste repositório.
- Desenhos de interface: Breeze, do KDE Visual Design Group, que já vem com o Plasma.

## Licença

MIT. Veja [LICENSE](LICENSE).
