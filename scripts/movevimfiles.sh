#!/bin/bash
sudo rm /usr/share/vim/vim80/syntax/doubledown.vim
sudo cp ./vim/doubledown.vim /usr/share/vim/vim80/syntax/doubledown.vim

rm ~/.vim/syntax/doubledown.vim
cp ./vim/doubledown.vim ~/.vim/syntax/doubledown.vim
