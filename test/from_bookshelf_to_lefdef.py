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
    # default density target
    # density_target = 0.5
    # default bin size = 10 circuit row height x 10 circuit row height
    # bin_row_factor = 10

    # from .aux read filenames
    filename_list: list[str] = []
    with open(aux_path) as file:
        row = file.readline()
        filename_list = row.split()
    scl_path = PurePath(aux_path.parents[0], filename_list[6])
    node_path = PurePath(aux_path.parents[0], filename_list[2])
    pl_path = PurePath(aux_path.parents[0], filename_list[5])
    nets_path = PurePath(aux_path.parents[0], filename_list[3])

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

    region = read_row_input(scl_path, default_row_height)
    object_db = read_node_input(node_path)
    read_placement_input(pl_path, object_db)
    nets = read_net_input(nets_path)

    pd_data = PhysDesignData()
    pd_data.region = region
    pd_data.object_db = object_db
    pd_data.nets = nets

    return pd_data


def write_to_lefdef(pd_data: PhysDesignData):
    return True


def main(aux_path: str):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    # Logging to a .log file
    handler = logging.FileHandler("log_parser.log", encoding="utf-8")
    root_logger.addHandler(handler)
    # show log messages on terminal as well
    root_logger.addHandler(logging.StreamHandler(sys.stdout))

    global START_DT
    logging.info(f"{__name__} program start @ {START_DT}"[:-3])

    pd_data = read_bookshelf(PurePath(aux_path))
    write_to_lefdef(pd_data)


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
