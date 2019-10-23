#!/bin/bash
sudo rm /usr/share/vim/vim80/syntax/qtml.vim
sudo cp ./vim/qtml.vim /usr/share/vim/vim80/syntax/qtml.vim

rm ~/.vim/syntax/qtml.vim
cp ./vim/qtml.vim ~/.vim/syntax/qtml.vim
