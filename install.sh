#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p ~/.local/bin
chmod +x "$DIR/echoterm.py"
ln -sf "$DIR/echoterm.py" ~/.local/bin/echoterm
echo "installed -> ~/.local/bin/echoterm"
