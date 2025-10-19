#!/bin/bash -e

wget "https://github.com/KenT2/python-games/tarball/master" -O python_games.tar$

ln -sf pip3 /usr/bin/pip-3.2

install -v -o USERNAME -g pi -d ~/python_games
tar xvf python_games.tar.gz -C ~/python_games --strip-components=1
chown USERNAME:pi ~/python_games -Rv
chmod +x ~/python_games/launcher.sh

install -v -o USERNAME -g pi -d "~/Documents"
install -v -o USERNAME -g pi -d "~/Documents/BlueJ Projects"
install -v -o USERNAME -g pi -d "~/Documents/Greenfoot Projects"
install -v -o USERNAME -g pi -d "~/Documents/Scratch Projects"
mkdir -p /usr/share/doc/BlueJ/
mkdir -p /usr/share/doc/Greenfoot/
mkdir -p /usr/share/scratch/Projects/Demos/
rsync -a --chown=USERNAME:pi /usr/share/doc/BlueJ/ "~/Documents/BlueJ Projects"
rsync -a --chown=USERNAME:pi /usr/share/doc/Greenfoot/ "~/Documents/Greenfoot Projects"
rsync -a --chown=USERNAME:pi /usr/share/scratch/Projects/Demos/ "~/Documents/Scratch Projects"

#Alacarte fixes
install -v -o USERNAME -g pi -d "~/.local"
install -v -o USERNAME -g pi -d "~/.local/share"
install -v -o USERNAME -g pi -d "~/.local/share/applications"
install -v -o USERNAME -g pi -d "~/.local/share/desktop-directories"