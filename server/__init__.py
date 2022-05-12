import sys
from pathlib import PurePath

BASE_DIR = PurePath(__file__).parent.parent

sys.path.append(str(BASE_DIR.joinpath("server")))
