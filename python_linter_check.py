import sys
from glob import glob
from pylint.lint import Run

if __name__ == "__main__":
    Run(sys.argv[1:])

