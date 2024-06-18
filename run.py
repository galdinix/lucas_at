import pathlib
import sys
file = pathlib.Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from miniProjeto3.src.main import*
data = main()