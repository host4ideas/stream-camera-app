import flet as ft
from src.components.camera_image import CameraImage
from src.components.filter_selector import FilterSelector


class App(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.filter_selector = FilterSelector()
        self.img_camera = CameraImage(
            current_filter=self.filter_selector.current_filter)

    def build(self):
        return (
            ft.Row(
                [
                    ft.IconButton(ft.icons.STOP_CIRCLE,
                                  on_click=lambda e: self.img_camera.stop_streaming()),
                    ft.Column(
                        [
                            self.img_camera,
                            self.filter_selector
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.IconButton(ft.icons.PLAY_CIRCLE,
                                  on_click=lambda e: self.img_camera.start_streaming()),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
