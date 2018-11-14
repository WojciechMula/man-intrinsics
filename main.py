import sys
from lib.guide.loader import load
from lib.man.generate import Generator

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
