import flet as ft
from src.utils.utils import Filter


class FilterSelector(ft.UserControl):
    def __init__(self):
        super().__init__()

        # Save Filters enum names to list to be able to iterate over them (for next / prev functionality)
        self.available_filters = list(
            map(lambda x: x.name, Filter._member_map_.values()))
        # Save current filter index over the filters list to know where you are
        self.current_filter_index = 0
        self.current_filter = Filter[self.available_filters[self.current_filter_index]]

        # Text field to show selected filter
        self.current_filter_text = ft.Text(
            value='Actual background filter:\n' +
            self.available_filters[self.current_filter_index],
            text_align=ft.TextAlign.CENTER)

    def update_filter(self):
        # Update filter mode text
        self.current_filter_text.value = 'Actual background filter:\n {}'.format(
            self.available_filters[self.current_filter_index])
        self.current_filter = Filter[self.available_filters[self.current_filter_index]]
        self.update()

    def next_filter(self):
        # Check if the next index doesn't exceed the number of available filters
        if self.current_filter_index + 1 < len(self.available_filters):
            self.current_filter_index += 1
            self.update_filter()

    def prev_filter(self):
        # Check if the next index is higher than the number of available filters
        if self.current_filter_index - 1 >= 0:
            self.current_filter_index -= 1
            self.update_filter()

    def build(self):
        return (
            ft.Row([
                ft.IconButton(ft.icons.SKIP_PREVIOUS,
                              on_click=lambda e: self.prev_filter()),
                self.current_filter_text,
                ft.IconButton(ft.icons.SKIP_NEXT,
                              on_click=lambda e: self.next_filter()),
            ])
        )
