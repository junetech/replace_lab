import math
from pathlib import PurePath


class Region:
    def __init__(self):
        # stores row_y_low value for each row.
        self.RowDB: list[int] = []
        # starting X coordinate of each row
        self.RowDBstartX: list[int] = []
        # ending X coordinate of each row. RowDBs share the same index
        self.RowDBendX: list[int] = []

        # line in *.def:
        # DIEAREA ( lx ly ) ( hx hy )
        self.lx = 999999
        self.ly = 999999
        self.hx = -99999
        self.hy = -99999

        self.total_row_area = 0

    def num_rows(self) -> int:
        return len(self.RowDB)

    def set_new_row(self, row_y: int, row_x: int, row_num_sites: int):
        self.RowDB.append(row_y)
        self.RowDBstartX.append(row_x)
        self.RowDBendX.append(row_x + row_num_sites)

    def add_row_area(self, row_num_sites: int, row_height: int):
        self.total_row_area += row_num_sites * row_height

    def update_area_coordinates(
        self, row_x: int, row_num_sites: int, row_y: int, row_height: int
    ):
        if self.lx > row_x:
            self.lx = row_x
        if self.hx < row_x + row_num_sites:
            self.hx = row_x + row_num_sites
        if self.ly > row_y:
            self.ly = row_y
        if self.hy < row_y + row_height:
            self.hy = row_y + row_height


def read_row_input(scl_file: PurePath, default_row_height: int) -> Region:
    """reads row input file and returns an instance of class Region

    Args:
        scl_file (PurePath): *.scl
        default_row_height (_type_): all row height values must be equal

    Raises:
        ValueError: when a sequence of consecutive row headers is invalid

    Returns:
        Region
    """
    file = open(scl_file, "r")
    line_idx = 0
    region = Region()

    row_height = default_row_height
    num_processed_rows = 0

    for line in file:
        line_idx += 1
        _line = line.strip()  # remove front & end whitespaces
        words = _line.split()  # split the row by whitespace

        # comment: added to skip empty lines (just as reading node files)
        if not _line:
            continue
        # skip initial metadata lines
        if words[0] in ["#", "UCLA"]:
            continue
        if words[0] == "NumRows":
            num_rows_from_file = int(words[2])
            # TODO: from print to log.info
            print(f"NumRows: {num_rows_from_file} rows are defined")
            continue

        # CoreRow data process
        if words[0] == "CoreRow":
            # Coordinate row
            line = file.readline()
            line_idx += 1
            _line = line.strip()
            words = _line.split()
            if words[0] != "Coordinate":
                err_str = "CoreRow Processing: Coordinate keyword not found"
                err_str += f" at line {line_idx}\n"
                raise ValueError(err_str)
            row_y = int(words[2])

            # Height row
            line = file.readline()
            line_idx += 1
            _line = line.strip()
            words = _line.split()
            if words[0] != "Height":
                err_str = "CoreRow Processing: Height keyword not found"
                err_str += f" at line {line_idx}\n"
                raise ValueError(err_str)
            row_height = int(words[2])
            if row_height != default_row_height:
                err_str = f"Row Height mismatch: {default_row_height} !="
                err_str += f" {row_height} at line {line_idx}\n"
                raise ValueError(err_str)

            # Sitewidth row
            line = file.readline()
            line_idx += 1
            _line = line.strip()
            words = _line.split()
            if words[0] != "Sitewidth":
                err_str = "CoreRow Processing: Sitewidth keyword not found"
                err_str += f" at line {line_idx}\n"
                raise ValueError(err_str)
            # site_width = words[2]

            # Sitespacing row
            line = file.readline()
            line_idx += 1
            _line = line.strip()
            words = _line.split()
            if words[0] != "Sitespacing":
                err_str = "CoreRow Processing: Sitespacing keyword not found"
                err_str += f" at line {line_idx}\n"
                raise ValueError(err_str)
            # comment: error in original file: site_width
            # site_spacing = words[2]

            # Siteorient row
            line = file.readline()
            line_idx += 1
            _line = line.strip()
            words = _line.split()
            if words[0] != "Siteorient":
                err_str = "CoreRow Processing: Siteorient keyword not found"
                err_str += f" at line {line_idx}\n"
                raise ValueError(err_str)
            # site_orient = words[2]

            # Sitesymmetry row
            line = file.readline()
            line_idx += 1
            _line = line.strip()
            words = _line.split()
            if words[0] != "Sitesymmetry":
                err_str = "CoreRow Processing: Sitesymmetry keyword not found"
                err_str += f" at line {line_idx}\n"
                raise ValueError(err_str)
            # comment: error in original file: site_width
            # site_symm = words[2]

            # SubrowOrigin row
            line = file.readline()
            line_idx += 1
            _line = line.strip()
            words = _line.split()
            if words[0] != "SubrowOrigin":
                err_str = "CoreRow Processing: SubrowOrigin keyword not found"
                err_str += f" at line {line_idx}\n"
                raise ValueError(err_str)
            row_x = int(words[2])
            row_num_sites = int(words[5])

            # End row
            line = file.readline()
            line_idx += 1
            _line = line.strip()
            words = _line.split()
            if words[0] != "End":
                err_str = "CoreRow Processing: End keyword not found"
                err_str += f" at line {line_idx}\n"
                raise ValueError(err_str)

            # add row info
            region.set_new_row(row_y, row_x, row_num_sites)
            region.add_row_area(row_num_sites, row_height)

            # update region size coordinates
            region.update_area_coordinates(row_x, row_num_sites, row_y, row_height)

            num_processed_rows += 1

    file.close()
    print(f"Total {num_processed_rows} rows are processed.")
    print(f"\tImageWindow=({region.lx} {region.ly} {region.hx} {region.hy})")
    print(f"\tTotal Row Area={region.total_row_area}")
    return region


class Bin:
    def __init__(self, lx: int, hx: int, ly: int, hy: int, cap: int):
        self.lx = lx
        self.hx = hx
        self.ly = ly
        self.hy = hy
        self.cap = cap
        self.m_usage = 0  # MUSAGE
        self.f_usage = 0  # FUSAGE

    def four_corners(self) -> tuple[int, int, int, int]:
        """
        Returns:
            tuple[int, int, int, int]: lx, ly, hx, hy
        """
        return self.lx, self.ly, self.hx, self.hy


class CMap:
    def __init__(self, x_dim: int, y_dim: int, x_unit: int, y_unit: int):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.x_unit = x_unit
        self.y_unit = y_unit
        self.bins: list[Bin] = []

    def num_entry(self) -> int:
        return len(self.bins)

    def add_bin(self, bin: Bin):
        self.bins.append(bin)


def make_c_map(region: Region, default_row_height: int, bin_row_factor: int) -> CMap:
    window_width = region.hx - region.lx
    window_height = region.hy - region.ly

    x_unit = y_unit = default_row_height * bin_row_factor
    x_dim = math.ceil(window_width / x_unit)
    y_dim = math.ceil(window_height / y_unit)
    c_map = CMap(x_dim, y_dim, x_unit, y_unit)

    debug_summed_bin_cap = 0
    start_y = region.ly
    for j in range(y_dim):
        start_x = region.lx
        for i in range(x_dim):
            # index = j * x_dim + i

            bin_lx = start_x + i * x_unit
            bin_ly = start_y
            bin_hx = bin_lx + x_unit
            bin_hy = bin_ly + y_unit

            # last column bins
            if i == x_dim - 1 and bin_hx > region.hx:
                bin_hx = region.hx
            # last row bins
            if j == y_dim - 1 and bin_hy > region.hy:
                bin_hy = region.hy

            # calculate bin cap based on row definition
            bin_cap = 0
            for row_idx in range(region.num_rows()):
                row_lx = region.RowDBstartX[row_idx]
                row_hx = region.RowDBendX[row_idx]
                row_ly = region.RowDB[row_idx]
                row_hy = row_ly + default_row_height

                if row_ly > bin_hy:
                    break
                # no overlapping area between this row and bin under consideration
                # comment: second condition is redundant
                if (
                    row_hy < bin_ly
                    or row_ly > bin_hy
                    or row_hx < bin_lx
                    or row_lx > bin_hx
                ):
                    continue

                # get intersection between row & bin
                common_lx = max(row_lx, bin_lx)
                common_hx = min(row_hx, bin_hx)
                common_ly = max(row_ly, bin_ly)
                common_hy = min(row_hy, bin_hy)
                common_area = (common_hx - common_lx) * (common_hy - common_ly)
                bin_cap += common_area

            # cover_area = (bin_hx - bin_lx) * (bin_hy - bin_ly)

            bin = Bin(bin_lx, bin_hx, bin_ly, bin_hy, bin_cap)
            c_map.add_bin(bin)
            debug_summed_bin_cap += bin.cap
        start_y += y_unit

    # Debugging purpose: Just make sure sigma(bin area) == placement area
    debug_place_area = window_width * window_height
    if debug_place_area != region.total_row_area:
        # comment: error in original file: summed_bin_cap
        err_str = f"Summed_bin_cap_: {debug_summed_bin_cap}"
        err_str += f" != Total Row_Area: {region.total_row_area}"
        raise ValueError(err_str)

    print(f"CMAP Dim: {c_map.x_dim} x {c_map.y_dim}")
    print(f"BinSize: {c_map.x_unit} x {c_map.y_unit}\tTotal {c_map.num_entry()} bins.")
    return c_map


class Node:
    is_fixed: bool

    def __init__(self, name: str, dx: int, dy: int, lx: int, ly: int, node_type: str):
        self.name = name
        self.dx = dx  # x size
        self.dy = dy  # y size
        self.lx = lx  # lx location
        self.ly = ly  # ly location
        self.node_type = node_type  # terminal or movable


class ObjectDB:
    def __init__(self):
        self.nodes: dict[str, Node] = {}  # ($name, $record) = each %ObjectDB

        self.num_terminal = 0
        self.total_movable_area = 0
        # comment: added
        self.total_fixed_area = 0

    def num_entry(self) -> int:
        return len(self.nodes)

    def add_node(self, node: Node):
        self.nodes[node.name] = node

    def set_node_loc(self, name: str, loc_x: int, loc_y: int):
        self.nodes[name].lx = loc_x
        self.nodes[name].ly = loc_y


def read_node_input(node_file: PurePath) -> ObjectDB:
    """reads node input file and returns an instance of class ObjectDB

    Args:
        node_file (PurePath): *.nodes

    Raises:
        ValueError: When NumTerminals is not next to NumNodes row

    Returns:
        ObjectDB
    """
    file = open(node_file, "r")
    line_idx = 0
    object_db = ObjectDB()

    num_obj = 0

    for line in file:
        line_idx += 1
        _line = line.strip()  # remove front & end whitespaces
        words = _line.split()  # split the row by whitespace

        # skip empty lines
        if not _line:
            continue
        # skip initial metadata lines
        if words[0] in ["#", "UCLA"]:
            continue

        # NumNodes row
        if words[0] == "NumNodes":
            num_obj_from_file = int(words[2])
            # NumTerminals row
            line = file.readline()
            line_idx += 1
            _line = line.strip()
            words = _line.split()
            if words[0] != "NumTerminals":
                err_str = "*.nodes Processing: NumTerminals keyword not found"
                err_str += f" at line {line_idx}\n"
                raise ValueError(err_str)
            num_term_from_file = int(words[2])
            # TODO: from print to log.info
            print(f"NumNodes: {num_obj_from_file}\tNumTerminals: {num_term_from_file}")
            continue

        # comment: node ID, x, y, terminal boolean rows
        name, dx, dy = words[0], int(words[1]), int(words[2])
        move_type: str
        # comment: words[3] in original raises IndexError in python
        if words[-1] == "terminal":
            move_type = "terminal"
            object_db.num_terminal += 1
            # comment: added
            object_db.total_fixed_area += dx * dy
        else:
            move_type = "movable"
            object_db.total_movable_area += dx * dy
        lx, ly = 0, 0

        # add node info
        record = Node(name, dx, dy, lx, ly, move_type)
        record.is_fixed = move_type == "terminal"
        object_db.add_node(record)

        num_obj += 1

    file.close()
    num_entry = object_db.num_entry()
    print("Node file processing is done.")
    print(f"\tTotal {num_obj} objects ({object_db.num_terminal} terminals)")
    print(f"\tTotal {num_entry} entries in ObjectDB")
    print(f"\tTotal movable area: {object_db.total_movable_area}")
    # comment: added
    print(f"\tTotal fixed area: {object_db.total_fixed_area}")
    return object_db


def read_placement_input(pl_path: PurePath, object_db: ObjectDB):
    """reads placement input file and changes the location information of the object_db.

    Args:
        pl_path (PurePath): *.pl
        object_db (ObjectDB)

    Raises:
        ValueError: When an undefined node name exists in *.pl
        ValueError: When a terminal node is not fixed in *.pl
    """
    file = open(pl_path, "r")
    line_idx = 0
    # object_db = ObjectDB()

    num_obj = 0
    num_terminal = 0

    for line in file:
        line_idx += 1
        _line = line.strip()  # remove front & end whitespaces
        words = _line.split()  # split the row by whitespace

        # skip empty lines
        if not _line:
            continue
        # skip initial metadata lines
        if words[0] in ["#", "UCLA"]:
            continue

        # comment: node ID, x, y, terminal boolean rows
        name, loc_x, loc_y = words[0], int(words[1]), int(words[2])
        if name not in object_db.nodes:
            err_str = f"Undefined object {name} appear in Solution PL file."
            raise ValueError(err_str)

        # comment: added terminal boolean check
        if object_db.nodes[name].is_fixed:
            if words[-1] != "/FIXED":
                err_str = f"Object {name} is terminal in *.scl file,"
                err_str += f" but not fixed in {pl_path}."
                raise ValueError(err_str)
            num_terminal += 1

        # add node info
        object_db.set_node_loc(name, loc_x, loc_y)
        num_obj += 1

    file.close()
    print("Solution PL file processing is done.")
    print(f"\tTotal {num_obj} objects ({num_terminal} terminals)")


class Pin:
    def __init__(
        self,
        cell_name: str,
        is_input: bool,
        x_offset: float,
        y_offset: float,
    ):
        self.cell_name = cell_name
        self.is_input = is_input
        self.offset = (x_offset, y_offset)


class Net:
    def __init__(self, net_name: str, degree: int):
        self.net_name: str = net_name
        self.degree: int = degree
        self.pin_names: list[str] = []


class Nets:
    def __init__(self):
        self.pin_name_list: list[str] = []
        self.pin_dict: dict[str, Pin] = {}
        self.cell_ipin_name_dict: dict[str, list[str]] = {}
        self.cell_opin_name_dict: dict[str, list[str]] = {}
        self.net_name_list: list[str] = []
        self.net_dict: dict[str, Net] = {}

    def new_pin_name(self, cell_name: str, is_input: bool):
        if is_input:
            return f"{cell_name}I{len(self.cell_ipin_name_dict[cell_name])}"
        else:
            return f"{cell_name}O{len(self.cell_opin_name_dict[cell_name])}"

    def add_pin(
        self, cell_name: str, io: str, x_offset: float, y_offset: float
    ) -> list[str]:
        pin_names: list[str] = []
        if io == "I":
            pin_names.append(self.add_input_pin(cell_name, x_offset, y_offset))
        elif io == "O":
            pin_names.append(self.add_output_pin(cell_name, x_offset, y_offset))
        elif io == "B":
            pin_names.append(self.add_input_pin(cell_name, x_offset, y_offset))
            pin_names.append(self.add_output_pin(cell_name, x_offset, y_offset))
        else:
            raise ValueError("Pin type should be 'I' or 'O' or 'B'")
        return pin_names

    def add_input_pin(self, cell_name: str, x_offset: float, y_offset: float) -> str:
        # Try finding the pin at the offset coordinate
        if cell_name in self.cell_ipin_name_dict:
            for pin_name in self.cell_ipin_name_dict[cell_name]:
                if self.pin_dict[pin_name].offset == (x_offset, y_offset):
                    return pin_name
        else:
            self.cell_ipin_name_dict[cell_name] = []
        # If there is none, make a new pin
        new_pin = Pin(cell_name, True, x_offset, y_offset)
        new_pin_name = self.new_pin_name(cell_name, True)
        self.pin_name_list.append(new_pin_name)
        self.pin_dict[new_pin_name] = new_pin
        self.cell_ipin_name_dict[cell_name].append(new_pin_name)

        return new_pin_name

    def add_output_pin(self, cell_name: str, x_offset: float, y_offset: float) -> str:
        # Try finding the pin at the offset coordinate
        if cell_name in self.cell_opin_name_dict:
            for pin_name in self.cell_opin_name_dict[cell_name]:
                if self.pin_dict[pin_name].offset == (x_offset, y_offset):
                    return pin_name
        else:
            self.cell_opin_name_dict[cell_name] = []
        # If there is none, make a new pin
        new_pin = Pin(cell_name, False, x_offset, y_offset)
        new_pin_name = self.new_pin_name(cell_name, False)
        self.pin_name_list.append(new_pin_name)
        self.pin_dict[new_pin_name] = new_pin
        self.cell_opin_name_dict[cell_name].append(new_pin_name)

        return new_pin_name

    def add_net(self, net_name: str, net_degree: int):
        self.net_name_list.append(net_name)
        new_net = Net(net_name, net_degree)
        self.net_dict[net_name] = new_net

    def assign_pin(self, pin_name: str, net_name: str):
        self.net_dict[net_name].pin_names.append(pin_name)

    def get_input_pins(self, cell_name: str) -> list[str]:
        if cell_name not in self.cell_ipin_name_dict:
            return []
        return self.cell_ipin_name_dict[cell_name]

    def get_output_pins(self, cell_name: str) -> list[str]:
        if cell_name not in self.cell_opin_name_dict:
            return []
        return self.cell_opin_name_dict[cell_name]


def read_net_input(nets_path: PurePath) -> Nets:
    """reads placement input file and changes the location information of the object_db.

    Args:
        pl_path (PurePath): *.pl
        object_db (ObjectDB)

    Raises:
        ValueError: When an undefined node name exists in *.pl
        ValueError: When a terminal node is not fixed in *.pl
    """
    file = open(nets_path, "r")
    line_idx = 0
    nets = Nets()

    num_nets, current_net = 0, 0
    num_pins, current_pin = 0, 0

    for line in file:
        line_idx += 1
        _line = line.strip()  # remove front & end whitespaces
        words = _line.split()  # split the row by whitespace

        # skip empty lines
        if not _line:
            continue
        # skip initial metadata lines
        if words[0] in ["#", "UCLA"]:
            continue
        if line.startswith("NumNets"):
            num_nets = int(line.split()[2])
            continue
        if line.startswith("NumPins"):
            num_pins = int(line.split()[2])
            continue

        match len(line.split()):
            case 4:
                current_net += 1
                _, _, net_degree_str, net_name = line.split()
                nets.add_net(net_name, eval(net_degree_str))
            case 5:
                current_pin += 1
                cell_name, io, _, x_offset_str, y_offset_str = line.split()
                try:
                    pin_names = nets.add_pin(
                        cell_name, io, eval(x_offset_str), eval(y_offset_str)
                    )
                    for name in pin_names:
                        nets.assign_pin(name, net_name)
                except ValueError:
                    print(line.split())
                    raise UserWarning
            case None:
                break

    file.close()
    print("Nets file processing is done.")
    _str = f"The number of nets recorded in file {num_nets} is wrong; there are {current_net} nets"
    if num_nets != current_net:
        print(Warning(_str))
    _str = f"The number of pins recorded in file {num_pins} is wrong; there are {current_pin} pins"
    if num_pins != current_pin:
        print(Warning(_str))

    return nets


class PhysDesignData:
    region: Region
    object_db: ObjectDB
    nets: Nets
