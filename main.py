import flet as ft
from app import App


def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(App())


ft.app(target=main)
