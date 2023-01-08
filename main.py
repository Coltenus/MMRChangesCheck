import threading
import time

import data_operations
import flet as ft


class Window:
    isDone = True

    def __init__(self):
        self.field1 = ft.TextField(hint_text="Player's id (required)", width=200)
        self.field2 = ft.TextField(hint_text="Nickname", width=200)
        self.dropdown = ft.Dropdown(hint_text="Matches (required)", width=200, options=[
            ft.dropdown.Option(10),
            ft.dropdown.Option(25),
            ft.dropdown.Option(50),
        ])
        self.startEl = ft.Row([
            self.field1,
            self.field2,
            self.dropdown,
            ft.ElevatedButton("Add", on_click=self.add_row),
            ft.ElevatedButton("Clear", on_click=self.clear_rows)
        ])
        self.table = ft.DataTable(columns=[
            ft.DataColumn(ft.Text("Nickname", width=200)),
            ft.DataColumn(ft.Text("MMR changes", width=100)),
            ft.DataColumn(ft.Text("Matches count", width=100)),
        ], rows=[])
        self.page: ft.Page = None
        ft.app(target=self.update)

    def update(self, page: ft.Page):
        self.page = page
        self.page.title = "MMR changes check"
        self.page.window_resizable = False
        self.page.window_width = 800
        self.page.window_height = 600
        self.table.width = self.page.window_width
        self.page.add(self.startEl)
        self.page.add(self.table)

    def add_button(self, e):
        threading.Thread(target=self.add_row, args=[self, e])

    def add_row(self, e):
        if self.isDone and self.field1.value != "" and self.dropdown.value is not None:
            self.isDone = False
            id_p = self.field1.value
            if self.field2.value != "":
                name = self.field2.value
            else:
                name = self.field1.value
            matches = self.dropdown.value
            mmr = data_operations.GetWinrateData(int(id_p), int(matches))
            row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(name, width=200)),
                ft.DataCell(ft.Text(mmr, width=100)),
                ft.DataCell(ft.Text(matches, width=100)),
            ])
            self.page.remove(self.table)
            rows = [row]
            rows.extend(self.table.rows)
            self.table.rows = rows
            self.page.add(self.table)
            time.sleep(10)
            self.isDone = True

    def clear_rows(self, e):
        self.page.remove(self.table)
        self.table.rows = []
        self.page.add(self.table)


if __name__ == '__main__':
    app = Window()
