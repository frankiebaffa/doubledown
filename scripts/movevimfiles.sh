#!/bin/bash
sudo rm /usr/share/vim/vim80/syntax/marktwo.vim
sudo cp ./vim/marktwo.vim /usr/share/vim/vim80/syntax/marktwo.vim

rm ~/.vim/syntax/marktwo.vim
cp ./vim/marktwo.vim ~/.vim/syntax/marktwo.vim
