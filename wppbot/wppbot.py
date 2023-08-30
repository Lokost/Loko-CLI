# coding: utf-8
from selenium import webdriver
from json import load, dump
from selenium.webdriver.common.by import By
from os.path import exists
from os import mkdir, getenv

class WPPBot:
    bot_folder = f'{getenv("APPDATA")}/loko_cli/lokowppbot'
    
    def __create_bot_folder(self):
        if not exists(self.bot_folder):
            mkdir(self.bot_folder)

    def get_messages(self):
        pass


    def __gen_messages(self):
        pass

#Fim
# @Copyright Gabriel Gomes/Lokost Games 2023
