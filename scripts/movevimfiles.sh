#!/bin/bash
sudo rm /usr/local/share/vim/vim81/syntax/qtml.vim
sudo cp ./vim/qtml.vim /usr/local/share/vim/vim81/syntax/qtml.vim

rm ~/.vim/syntax/qtml.vim
cp ./vim/qtml.vim ~/.vim/syntax/qtml.vim
