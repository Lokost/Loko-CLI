# coding: utf-8

from time import sleep
from selenium import webdriver
from json import load, dump
from selenium.webdriver.common.by import By
from os.path import exists, isfile
from os import mkdir, getenv
from wppbot.table_tratment import MessagesTable
from random import choice
from urllib.parse import quote


class WPPBot:
    bot_folder = f"{getenv('APPDATA')}\\loko_cli\\lokowppbot"

    def __create_bot_folder(self):
        print("Checking the existence of the bot folder...", end="\r")
        if not exists(self.bot_folder):
            print("Creating bot folder", end="\r")
            mkdir(self.bot_folder)
            print("Bot folder created!")

        else:
            print("Bot folder already exists!")

    def __get_settings(self):
        print("Checking the existence of the settings file...", end="\r")
        if not exists(f"{self.bot_folder}\\settings.json"):
            print("Creating settings file", end="\r")
            with open(
                f"{self.bot_folder}\\settings.json", "w", encoding="utf-8"
            ) as settings_file:
                self.settings = (
                    {
                        "browser": "chrome",
                        "wait_time": 5,
                        "keep_browser": True,
                        "default_columns": ["Nome", "Email", "Telefone"],
                    },
                )
                dump(
                    self.settings,
                    settings_file,
                )
            print("Settings file created!")

        else:
            print("loading settings file...", end="\r")
            with open(
                f"{self.bot_folder}\\settings.json",
                "r",
                encoding="utf-8",
            ) as file:
                self.settings = load(file)
                print("Settings file loaded!")

    ## Bot Functions ##
    def __get_messages(self):
        if not exists(f"{self.bot_folder}\\messages.json"):
            print("Creating messages file", end="\r")
            with open(
                f"{self.bot_folder}\\messages.json", "w", encoding="utf-8"
            ) as messages_file:
                self.messages = {}
                dump(
                    self.messages,
                    messages_file,
                )
            print("Messages file created!")

        else:
            self.messages = load(open(f"{self.bot_folder}\\messages.json"))
            print("Messages file loaded!")

    def __gen_messages(self, data=[], type=""):
        message = choice(self.messages[type]).format(*data)
        return quote(message)

    def __message_parser(self, message):
        return quote(message)

    def __set_browser(self):
        print("Setting browser...", end="\r")
        match (self.settings["browser"]):
            case "chrome":
                service = webdriver.ChromeService(
                    executable_path="wppbot/webdrivers/chromedriver.exe"
                )
                self.browser = webdriver.Chrome(service=service)
            case "firefox":
                service = webdriver.FirefoxService(
                    executable_path="wppbot/webdrivers/geckodriver.exe"
                )
                self.browser = webdriver.Firefox(service=service)
            case "edge":
                service = webdriver.EdgeService(
                    executable_path="wppbot/webdrivers/msedgedriver.exe"
                )
                self.browser = webdriver.Edge(service=service)
            case "opera":
                service = webdriver.OperaService(
                    executable_path="wppbot/webdrivers/operadriver.exe"
                )
                self.browser = webdriver.Opera(service=service)
            case _:
                print("Browser not found!")
                exit(1)

    def __open_browser(self):
        print("Opening browser...", end="\r")
        self.browser.get("https://web.whatsapp.com/")
        print("Waiting the whatsapp authentication...", end="\r")
        while not self.browser.find_element(By.ID, "side"):
            sleep(1)
        print("Browser Ready!")

    def __send_message(self, message, number):
        link = f"https://web.whatsapp.com/send?phone={number}&text={message}"
        self.browser.get(link)

        while not self.browser.find_element(By.ID, "side"):
            sleep(1)

        worked = False
        for i in range(5):
            print(f"Attempt {i + 1}/5", end="\r")
            try:
                self.browser.find_element(
                    By.XPATH,
                    '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span',
                ).click()
                worked = True
                break
            except Exception as e:
                print(f"Error: {e}", end="\r")
                sleep(1)

        return worked
    
    def send_messages(self, table_path, message_file = "", auto_message=False):
        message: str
        table: list[list]

        if isfile(table_path):
            try:
                self.tableManager = MessagesTable(
                    table_path = table_path,
                    table_columns= self.settings["default_columns"]
                )
                table = self.tableManager.getTable
                print("Table loaded!")

            except ValueError as e:
                print(f"Invalid File: {e}")

        else:
            print("Needs be a Excel or CSV file!")
            exit(1)
        
        if not auto_message:
            if isfile(message_file):
                with open(message_file, "r", encoding="utf-8") as file:
                    message = file.read()
                    print("Message loaded!")
        
        print("Setting the browser...", end="\r")
        self.__set_browser()
        print("Opening the browser...", end="\r")
        self.__open_browser()

        print("Sending messages...", end="\r")
        for row in table.index:
            try:
                number = str(int(table.loc[row, "Telefone"]))
            except ValueError:
                number = str(table.loc[row, "Telefone"])

            print(f"{row}/{len(table.index)}\nSending message to {number}...", end="\r")

            if self.__send_message(
                message=self.__message_parser(message), number=number
            ):
                print("Message sent!", end="\r")
            else: 
                print("Message not sent!", end="\r")
            
            sleep(self.settings["wait_time"] - 1.5)
        print("Finished!")

    def __init__(self):
        self.__create_bot_folder()
        self.__get_settings()

    ## Table Management ##
    def create_table(self):
        self.tableManager = MessagesTable(self.settings["columns"])


# Fim
# @Copyright Gabriel Gomes/Lokost Games 2023
