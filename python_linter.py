import sys
from autopep8 import main

if __name__ == "__main__":
    for file in sys.argv[1:]:
        main(['-v', '-i', '--aggressive', '--aggressive', file])
