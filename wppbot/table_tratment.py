# coding: utf-8

import pandas as pd
from os.path import isfile


class MessagesTable:
    def __init__(self, table_columns, table_path: str = ""):
        if isfile(table_path) and table_path.endswith(
            (
                ".xls",
                ".xlsx",
                ".csv",
            )
        ):
            self.table_path = table_path
            self.table = (
                pd.read_excel(table_path)
                if table_path.endswith(
                    (
                        ".xls",
                        ".xlsx",
                    )
                )
                else pd.read_csv(table_path)
            )
            self.table.columns = table_columns

        else:
            print("Any table opened, try put the path next time!")
            raise ValueError("Needs be a Excel or CSV file")

    @property
    def getTable(self):
        return self.table

    def create_table(self, table_path: str, table_columns):
        if table_path.startswith(
            (
                "C:/",
                "C:\\",
                "D:/",
                "D:\\",
                "E:/",
                "E:\\",
                "F:\\",
                "F:/",
            )
        ):
            table_path = table_path.replace("\\", "/")

        print("Creating a new table in: ", table_path)
        self.table = pd.DataFrame(columns=table_columns)
        self.table.to_excel(table_path, index=False)
        print("Table created!")


# Fim
# @Copyright Gabriel Gomes/Lokost Games 2023
