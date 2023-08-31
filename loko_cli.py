# coding: utf-8

import os
import sys
import argparse
import configparser
import logging

from wppbot.wppbot import WPPBot


class LokoCLI:
    CLI_VERSION = "Loko CLI 0.0.1"
    INI_FILE = "loko.ini"
    user_folder = f"{os.getenv('APPDATA')}\\loko_cli"

    def __create_user_folder(self):
        if not os.path.exists(self.user_folder):
            os.mkdir(self.user_folder)

    def __load_ini_file(self, filename):
        full_path = os.path.abspath(os.path.join(".", filename))
        path_config_file = (
            full_path
            if os.path.isfile(full_path)
            else os.path.abspath(
                os.path.join(os.path.dirname(sys.executable), filename)
            )
        )
        self.config = configparser.ConfigParser()
        if self.config.read(path_config_file):
            return True
        else:
            logging.basicConfig(
                level=logging.ERROR,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
            logging.error(
                f"Isn't possible load the settings file: \n{path_config_file}"
            )
            return False

    def __init__(self):
        self.__create_user_folder()
        if self.__load_ini_file(self.INI_FILE):
            self.__run()

    def __run(self):
        self.parser = argparse.ArgumentParser(
            prog="loko-cli",
            description="CLI de automações do Lokost",
            epilog="Desenvolvido por Lokost Games",
            usage="%(prog)s [options]",
        )

        self.parser.version = self.CLI_VERSION

        self.parser.add_argument(
            "-v", "--version", action="version", help="Retorna a versão atual do CLI"
        )

        subparsers = self.parser.add_subparsers(help="Loko Actions")
        self.__wppbot(subparsers)

        parse_args = self.parser.parse_args()

        if parse_args:
            try:
                if parse_args.createtable:
                    self.wppbot = WPPBot()
                    print("Criar tabela com colunas padrães")
                    self.wppbot.tableManager.create_table(
                        parse_args.createtable, self.wppbot.settings["columns"]
                    )

                if parse_args.send:
                    self.wppbot = WPPBot()
                    print("Iniciar envio de mensagens")
                    self.wppbot.send_messages(
                        table_path= parse_args.path,
                        message_file=parse_args.filemessage,
                        auto_message=parse_args.automessage,
                    )

                if parse_args.config:
                    print("Configurações do bot wpp")

            except Exception as e:
                print(f"Invalid argument: {e}")

    def __wppbot(self, subparsers):
        self.wppbot_parser = subparsers.add_parser("wppbot", help="WPPBot")
        self.wppbot_parser.add_argument(
            "-c",
            "--config",
            help="change a setting of the bot, being the browser, wait time, keep browser and default columns",
            type=str,
            required=False,
        )

        self.wppbot_parser.add_argument(
            "-ct",
            "--create-table",
            dest="createtable",
            help="Create a table with the default columns",
            type=str,
            required=False,
        )

        self.wppbot_parser.add_argument(
            "-s", "--send", help="Start sending the messages", action="store_true"
        )

        self.wppbot_parser.add_argument(
            "-p",
            "--path",
            help="Path to the file with the contacts",
            type=str,
            required=True,
        )

        self.wppbot_parser.add_argument(
            "-am",
            "--auto-message",
            dest="automessage",
            help="The messages will pick the messages into the JSON file",
            action="store_true",
        )

        self.wppbot_parser.add_argument(
            "-fm", "--filemessage",
            help="Path to the file with the message",
            type=str,
            required=False,
        )


# Fim
# @Copyright Gabriel Gomes/Lokost Games 2023
