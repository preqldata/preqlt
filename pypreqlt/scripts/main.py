from click import command, Path, argument, option, File
from preql.dialect.enums import Dialects  # noqa
from pathlib import Path as PathlibPath  # noqa
import os
from sys import path as sys_path

# handles development cases
nb_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys_path.insert(0, nb_path)

from pypreqlt.dbt.generate_dbt import generate_model  # noqa
from pypreqlt.dbt.run_dbt import run_path  # noqa
from pypreqlt.dbt.config import DBTConfig  # noqa


def print_tabulate(q, tabulate):
    result = q.fetchall()
    print(tabulate(result, headers=q.keys(), tablefmt="psql"))


@command("gen-dbt")
@argument("preql", type=File("r"))
@argument("dbt_path", type=Path(exists=True))
# @argument("write_path", type=Path(exists=True))
@argument("dialect", type=str)
@option("--run", is_flag=True, type=bool, default=False)
@option("--debug", type=bool, default=False)
def main(preql: File, dbt_path, dialect: str, debug: bool, run: bool):

    edialect = Dialects(dialect)
    if os.path.exists(preql.name):
        inputp = PathlibPath(preql.name)
        namespace = inputp.stem
    else:
        inputp = None
        namespace = None
    config = DBTConfig(root=PathlibPath(dbt_path), namespace=namespace)

    #
    generate_model(
        preql.read(), inputp, dialect=edialect, config=config  # type: ignore
    )
    if run:
        run_path(dbt_path)


if __name__ == "__main__":
    main()