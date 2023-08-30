# coding: utf-8

import os
import sys
import argparse
import configparser
import logging


class LokoCLI:
    CLI_VERSION = "Loko CLI 0.0.1"
    INI_FILE = "loko.ini"
    user_folder = f"{os.getenv('APPDATA')}/loko_cli"

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
                f"Não foi possível carregar o arquivo de configuração: \n{path_config_file}"
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

        parse_args = self.parser.parse_args()

        if parse_args.version:
            print(self.CLI_VERSION)


# Fim
# @Copyright Gabriel Gomes/Lokost Games 2023
