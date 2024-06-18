import pathlib
import sys

import miniProjeto3.src
import miniProjeto3.src.main
file = pathlib.Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
import miniProjeto3
data = miniProjeto3.src.main()