from tkinter import Tk, Button, Label, Entry
from typing import Optional, Union, Callable
from configparser import ConfigParser
from pydantic import validate_call
from threading import Thread
import time

from widget_grid_settings import WidgetGridSettings
from _types import AnyWidget

class NotFoundWidget(Exception): ...

ElementList = list[WidgetGridSettings]
Listeners = dict[str, dict[str, list[Callable]]]

class Window(Tk):
    ACCEPTED_WIDGETS_WITH_STYLES: list[AnyWidget] = [ Button, Label, Entry ]
    VALIDATE_CONFIG = dict(arbitrary_types_allowed = True)

    running = True
    styles_config = {}
    listeners: Listeners = {}

    @validate_call(config = VALIDATE_CONFIG)
    def __init__(
        self,
        screenName: Optional[str] = None,
        baseName: Optional[str] = None,
        className: str = "Window",
        useTk: bool = True,
        sync: bool = False,
        use: Optional[str] = None
    ) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.update_thread = Thread(target=self._update)
        self.after(500, lambda: self.update_thread.start())
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self) -> None:
        self.running = False
        self.update_thread.join()
        self.destroy()

    @validate_call(config = VALIDATE_CONFIG)
    def add_event_listener(self, widget_id: str, event: str, event_handler: Callable) -> None:
        if widget_id not in self.listeners:
            self.listeners[widget_id] = {}

        if event not in self.listeners[widget_id]:
            self.listeners[widget_id][event] = []

        self.listeners[widget_id][event].append(event_handler)

    @validate_call(config = VALIDATE_CONFIG)
    def fire_event(self, widget_id: str, event: str, *args, **kwargs) -> None:
        if widget_id in self.listeners and event in self.listeners[widget_id]:
            for handler in self.listeners[widget_id][event]:
                handler(*args, **kwargs)

    @validate_call(config = VALIDATE_CONFIG)
    def _set_widget_style(self, widget: AnyWidget, style: dict) -> None:
        widget.configure(**style)

    @validate_call(config = VALIDATE_CONFIG)
    def _read_file(
        self,
        file_path: str,
        encoding: str = "utf-8"
    ) -> str:
        with open(file_path, encoding = encoding) as file:
            content = file.read()
        
        return content
    
    def _parse_string_config(self, styles_text: str) -> dict:
        config = ConfigParser(
            allow_no_value = False,
            comment_prefixes = [ "//" ],
            strict = False
        )

        config.read_string(styles_text)

        sections = {}

        for section in config.sections():
            if "." in section: continue

            section_data = self._parse_section(config, section)
            sections[section] = section_data

        return sections

    def _parse_section(self, config: ConfigParser, section: dict) -> dict:
        data = {}

        for option, value in config.items(section):
            if value.startswith("[") and value.endswith("]"):
                data[option] = self._parse_list(value)

            elif value.startswith("(") and value.endswith(")"):
                data[option] = self._parse_tuple(value)

            else:
                data[option] = self._convert_value(value)

        sub_sections = {}

        separator = "."

        for sub_section in config.sections():
            if sub_section.startswith(section + separator):
                sub_section_name_start_index = len(section) + len(separator)
                sub_section_name_end_index = len(sub_section)
                sub_section_name = sub_section[sub_section_name_start_index : sub_section_name_end_index]
                sub_section_data = self._parse_section(config, sub_section)
                sub_sections[sub_section_name] = sub_section_data

        if sub_sections:
            data.update(sub_sections)

        return data

    @validate_call(config = VALIDATE_CONFIG)
    def _convert_value(self, value: str) -> Union[str, int, float, bool, None]:
        for converter in (int, float, self._to_bool):
            try:
                return converter(value)
            except ValueError:
                pass
        
        return value

    @validate_call(config = VALIDATE_CONFIG)
    def _parse_list(self, value: str) -> list[Union[str, int, float, bool, None]]:
        elements = value[1:-1].split(",")
        return [ self._convert_value(elem.strip()) for elem in elements ]

    @validate_call(config = VALIDATE_CONFIG)
    def _parse_tuple(self, value: str) -> tuple[Union[str, int, float, bool, None]]:
        elements = value[1:-1].split(",")
        return tuple(self._convert_value(elem.strip()) for elem in elements)

    @validate_call(config = VALIDATE_CONFIG)
    def _to_bool(self, value: str) -> bool:
        value = value.lower().strip()
        
        if value in [ "true", "false" ]:
            return value.lower() == "true"

        raise ValueError(f"Invalid boolean value '{value}'")

    @validate_call(config = VALIDATE_CONFIG)
    def use_styles_config(self, styles_config: dict) -> None:
        self.styles_config.update(styles_config)

        for widget_cls in self.ACCEPTED_WIDGETS_WITH_STYLES:
            widget_key = widget_cls.__name__

            if widget_key in styles_config.keys():
                styles = styles_config[widget_key]

                for widget in self.children.values():
                    if isinstance(widget, widget_cls):
                        self._set_widget_style(widget, styles)

    @validate_call(config = VALIDATE_CONFIG)
    def use_styles(self, styles_text: str) -> None:
        styles_config = self._parse_string_config(styles_text)
        self.use_styles_config(styles_config)

    @validate_call(config = VALIDATE_CONFIG)
    def use_styles_file(self, file_path: str) -> None:
        styles_text = self._read_file(file_path)
        self.use_styles(styles_text)

    def _update_styles(self) -> None:
        self.use_styles_config(self.styles_config)

    def _update_event_listeners(self) -> None:
        print(self.listeners)

        for widget_id, events in self.listeners.items():
            widget = self.get_widget_by_id(widget_id)

            if widget is None:
                continue

            for event, handlers in events.items():
                for handler in handlers:
                    widget.bind(event, handler)


    def _update(self) -> None:
        while self.running:
            self._update_styles()
            self._update_event_listeners()

            time.sleep(.5)

    @validate_call(config = VALIDATE_CONFIG)
    def get_widget_by_id(self, widget_id: str) -> Optional[AnyWidget]:
        for widget in self.children.values():
            if getattr(widget, "id", None) == widget_id:
                return widget

        return None

    @validate_call(config = VALIDATE_CONFIG)
    def use_widgets_config(self, widgets_config: dict) -> None:
        widgets_grid_settings = []

        print(widgets_config)

        for widget_id, widget_config in widgets_config.items():
            widget_type = widget_config.pop("type")
            widget_layout = widget_config.pop("layout")
            widget_class = self._get_widget_class(widget_type)
            widget = widget_class(self, **widget_config)
            widget.id = widget_id

            widget_grid_settings = WidgetGridSettings(
                widget = widget,
                **widget_layout
            )

            widgets_grid_settings.append(widget_grid_settings)

        self.apply_custom_layout(widgets_grid_settings)

    @validate_call(config = VALIDATE_CONFIG)
    def use_widgets(self, widgets_text: str) -> None:
        widgets_config = self._parse_string_config(widgets_text)
        self.use_widgets_config(widgets_config)

    @validate_call(config = VALIDATE_CONFIG)
    def use_widgets_file(self, file_path: str) -> None:
        widgets_text = self._read_file(file_path)
        self.use_widgets(widgets_text)

    @validate_call(config = VALIDATE_CONFIG)
    def apply_custom_layout(self, elements: ElementList) -> None:
        for widget_info in elements:
            widget = widget_info.pop("widget")
            widget.grid(**widget_info)

    @validate_call(config=VALIDATE_CONFIG)
    def _get_widget_class(self, widget_type: str) -> AnyWidget:
        widget_cls_names = [widget_cls.__name__ for widget_cls in self.ACCEPTED_WIDGETS_WITH_STYLES]

        if widget_type in widget_cls_names:
            widget_cls_index = widget_cls_names.index(widget_type)
            widget_cls = self.ACCEPTED_WIDGETS_WITH_STYLES[widget_cls_index]
            return widget_cls

        raise NotFoundWidget(f"Widget class not found for type: {widget_type}")

    # def mainloop(self, n: int = 0) -> None:
    #     self._update_styles()
    #     return super().mainloop(n)


def main() -> None:
    window = Window()

    window.title("Config Parser Example")
    window.geometry("400x250")

    window.use_styles_file("styles.ini")
    window.use_widgets_file("widgets.ini")

    # window.apply_custom_layout([
    #     WidgetGridSettings(
    #         widget = Button(
    #             master = window,
    #             text = "Bosta"
    #         ),
    #         row = 0,
    #         column = 0,
    #     ),
    #     WidgetGridSettings(
    #         widget = Label(
    #             master = window,
    #             text="Key: "
    #         ),
    #         row = 1,
    #         column = 0,
    #     ),
    #     WidgetGridSettings(
    #         widget =  Entry(master = window),
    #         row = 0,
    #         column = 1,
    #     )
    # ])

    def handle_button_01_click(event) -> None:
        print(event)
        print("clicado")

    window.add_event_listener("button_01", "<Button-1>", handle_button_01_click)

    window.mainloop()

if __name__ == "__main__":
    main()