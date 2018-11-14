import sys
from loader import load
from generate import Generator

def main():
    path = sys.argv[1]
    targetdir = sys.argv[2]

    print "Loading %s" % path
    db = load(path)

    print "Generating man pages in %s" % targetdir
    gen = Generator(db)
    gen.generate(targetdir)


if __name__ == '__main__':
    main()
