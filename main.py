import flet as ft
from webcam_stream import WebcamStream
from real_time_processing import RealTimeProcessing

# initializing and starting multi-threaded webcam capture input stream
# stream_id = 0 is for primary camera
webcam_stream = WebcamStream(stream_id=0)
webcam_stream.start()

real_time_processor = RealTimeProcessing(webcam_stream=webcam_stream)
real_time_processor.start()

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(
        value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    img = ft.Image(
        src=f"/icons/icon-512.png",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                img,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


ft.app(target=main)
