import flet as ft
from webcam_stream import WebcamStream
from real_time_processor import RealTimeProcessor
from typing import Any
import numpy.typing as npt
from utils.utils import array_to_base64, Filter


class App:
    def __init__(self, page: ft.Page):
        self.page = page

        # initializing and starting multi-threaded webcam capture input stream
        # stream_id = 0 is for primary camera
        self.webcam_stream = WebcamStream(stream_id=0)
        # self.webcam_stream.start()

        self.real_time_processor = RealTimeProcessor(
            on_frame_change=self.handle_frame_change,
            webcam_stream=self.webcam_stream)
        # self.real_time_processor.start()

        # Save Filters enum names to list to be able to iterate over them (for next / prev functionality)
        self.available_filters = list(
            map(lambda x: x.name, Filter._member_map_.values()))
        # Save current filter index over the filters list to know where you are
        self.current_filter_index = 0

        self.page.title = "Flet counter example"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # Text field to show selected filter
        self.current_filter_text = ft.Text(
            value='Actual background filter:\n' +
            self.available_filters[self.current_filter_index],
            text_align=ft.TextAlign.CENTER)

        # Default black image
        self.camera_img_default = "R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs="

        # Declare Image component to show camera capture
        self.img_camera = ft.Image(
            width=300,
            height=300,
            fit=ft.ImageFit.CONTAIN,
            src_base64=self.camera_img_default
        )

        # Start app
        self.main()

    def handle_frame_change(self, frame: npt.NDArray[Any]):
        self.img_camera.src_base64 = array_to_base64(frame)
        self.page.update()

    def main(self):
        def next_filter(e):
            # Check if the next index doesn't exceed the number of available filters
            if self.current_filter_index + 1 < len(self.available_filters):
                self.current_filter_index += 1

            # Update processing filter
            # self.real_time_processor.set_current_bg_filter(
            #     Filter[self.available_filters[self.current_filter_index]])

            # Update filter mode text
            self.current_filter_text.value = f'Actual background filter:\n{self.available_filters[self.current_filter_index]}'
            self.page.update()

        def prev_filter(e):
            # Check if the next index is higher than the number of available filters
            if self.current_filter_index - 1 >= 0:
                self.current_filter_index -= 1

            # Update processing filter
            # self.real_time_processor.set_current_bg_filter(
            #    Filter[self.available_filters[self.current_filter_index]])

            # Update filter mode text
            self.current_filter_text.value = 'Actual background filter:\n {}'.format(
                self.available_filters[self.current_filter_index])
            self.page.update()

        def stop_streaming(e):
            self.real_time_processor.stop()
            # Default camera's image to black
            self.img_camera.src_base64 = self.camera_img_default
            # Update filter to process
            # self.real_time_processor.set_current_bg_filter(
            #     Filter[self.available_filters[self.current_filter_index]])
            self.page.update()

        def start_streaming(e):
            self.real_time_processor.start()
            self.page.update()

        self.page.add(
            ft.Row(
                [
                    ft.IconButton(ft.icons.STOP_CIRCLE,
                                  on_click=stop_streaming),
                    ft.Column(
                        [
                            self.img_camera,
                            ft.Row([
                                ft.IconButton(ft.icons.SKIP_PREVIOUS,
                                              on_click=prev_filter),
                                self.current_filter_text,
                                ft.IconButton(ft.icons.SKIP_NEXT,
                                              on_click=next_filter),
                            ])
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.IconButton(ft.icons.PLAY_CIRCLE,
                                  on_click=start_streaming),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )


ft.app(target=App)
