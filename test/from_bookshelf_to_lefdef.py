import datetime
import logging
import sys
from pathlib import PurePath

from bookshelf_class import (
    PhysDesignData,
    read_net_input,
    read_node_input,
    read_placement_input,
    read_row_input,
)


def read_bookshelf(aux_path: PurePath) -> PhysDesignData:
    """Read Bookshelf format data
    reference: check_density_target.pl from ISPD 2006

    Args:
        aux_path (PurePath): path to *.aux file

    Returns:
        PhysDesignData
    """
    # DO NOT CHANGE. All circuit row height is 12
    default_row_height = 12
    default_site_width = 1
    # default density target
    # density_target = 0.5
    # default bin size = 10 circuit row height x 10 circuit row height
    # bin_row_factor = 10

    # from .aux read filenames
    filename_list: list[str] = []
    with open(aux_path) as file:
        row = file.readline()
        filename_list = row.split()
    scl_path = PurePath(aux_path.parent, filename_list[6])
    node_path = PurePath(aux_path.parent, filename_list[2])
    pl_path = PurePath(aux_path.parent, filename_list[5])
    nets_path = PurePath(aux_path.parent, filename_list[3])

    # 병렬화 시도했으나, 오히려 더 느림
    # from concurrent.futures import ProcessPoolExecutor
    # func_list = [read_net_input, read_node_input, read_row_input]
    # args_list = [[nets_path], [node_path], [scl_path, default_row_height]]
    # futures = []
    # results = []

    # with ProcessPoolExecutor(max_workers=3) as executor:
    #     for func, args in zip(func_list, args_list):
    #         futures.append(executor.submit(func, *args))
    #     for future in futures:
    #         results.append(future.result())

    # nets, object_db, region = results

    # read_placement_input(pl_path, object_db)

    region = read_row_input(scl_path, default_row_height, default_site_width)
    object_db = read_node_input(node_path)
    read_placement_input(pl_path, object_db)
    nets = read_net_input(nets_path)

    pd_data = PhysDesignData()
    pd_data.region = region
    pd_data.object_db = object_db
    pd_data.nets = nets

    return pd_data


def write_to_lefdef(pd_data: PhysDesignData, aux_path: PurePath):
    output_dir, output_filename = aux_path.parent, aux_path.stem + "_lefdef"
    half_pin_dimension = 0.1

    # write LEF
    lef_path = PurePath(output_dir, output_filename + ".lef")
    product_version = 5.8
    # Units
    database_microns = 100
    with open(lef_path, "w") as file:
        # LEF/DEF product version
        file.write(f"VERSION {product_version} ;\n")
        b_str = f"UNITS\n  DATABASE MICRONS {database_microns} ;\nEND UNITS\n\n"
        file.write(b_str)
        # MACRO
        for cell_name, cell in pd_data.object_db.nodes.items():
            b_str = f"MACRO {cell_name}\n  CLASS CORE ;\n"
            b_str += "  SITE core ;\n"
            b_str += f"  SIZE {cell.dx} BY {cell.dy} ;\n"
            # pin
            for pin_name in pd_data.nets.get_pins(cell_name):
                pin = pd_data.nets.pin_dict[pin_name]
                direction = pin.io
                x_offset, y_offset = pin.offset

                b_str += f"  PIN {pin_name}\n"
                match direction:
                    case "I":
                        b_str += "    DIRECTION INPUT ;\n"
                    case "O":
                        b_str += "    DIRECTION OUTPUT ;\n"
                    case "B":
                        b_str += "    DIRECTION INOUT ;\n"

                b_str += "    PORT\n      LAYER metal1 ;\n"
                lx, ly = x_offset - half_pin_dimension, y_offset - half_pin_dimension
                hx, hy = x_offset + half_pin_dimension, y_offset + half_pin_dimension
                b_str += f"        RECT ( {lx} {ly} ) ( {hx} {hy} ) ;\n"
                b_str += f"  END {pin_name}\n"
            b_str += f"END {cell_name}\n\n"
            file.write(b_str)
        # SITE
        b_str = "SITE defaultS\n"
        size_str = f"{pd_data.region.default_site_dim[0]} BY {pd_data.region.default_site_dim[1]}"
        b_str += f"  CLASS CORE ;\n  SIZE {size_str} ;\n"
        b_str += "END defaultS\n"
        file.write(b_str)
        # EoF
        file.write("END LIBRARY\n")
    return True


def main(aux_path_str: str):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    # Logging to a .log file
    handler = logging.FileHandler("log_parser.log", encoding="utf-8")
    root_logger.addHandler(handler)
    # show log messages on terminal as well
    root_logger.addHandler(logging.StreamHandler(sys.stdout))

    global START_DT
    logging.info(f"{__name__} program start @ {START_DT}"[:-3])

    aux_path = PurePath(aux_path_str)
    pd_data = read_bookshelf(aux_path)
    write_to_lefdef(pd_data, aux_path)


if __name__ == "__main__":
    START_DT = datetime.datetime.now()
    if len(sys.argv) != 2:
        print("*.aux file for Bookshelf format data is required")
        sys.exit(0)
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print("*.aux file for Bookshelf format data is required")
        sys.exit(0)
    main(sys.argv[1])
    END_DT = datetime.datetime.now()
    elapsed_d = END_DT - START_DT
    logging.info(
        f"{__name__} program end @ {END_DT}"[:-3] + f"; took total {elapsed_d}"[:-3]
    )
