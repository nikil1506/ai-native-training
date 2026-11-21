import sys

from .web import serve

serve(int(sys.argv[1]) if len(sys.argv) > 1 else 8765)
