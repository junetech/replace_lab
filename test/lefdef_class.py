class Macro:
    is_fixed: bool

    def __init__(self, name: str, dx: int, dy: int):
        self.name = name
        self.dx = dx
        self.dy = dy
        self.pin_dict: dict[tuple[float, float], str] = {}

    def pin_exists(self, x_offset: float, y_offset: float) -> bool:
        return (x_offset, y_offset) in self.pin_dict

    def add_pin(self, x_offset: float, y_offset: float, pin_name: str):
        self.pin_dict[(x_offset, y_offset)] = pin_name


class Component:
    lx: float
    ly: float

    def __init__(self, name: str, macro_name: str, place_status: str):
        self.name = name
        self.macro_name = macro_name
        self.place_status = place_status
