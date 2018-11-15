import sys
from lib.guide.loader import load as load_guide
from lib.uops.loader  import load as load_uops
from lib.man.generate import Generator

def main():
    path1 = sys.argv[1]
    path2 = sys.argv[2]
    targetdir = sys.argv[3]

    print "Loading instructions from %s" % path1
    db = load_guide(path1)

    def silent(s):
        pass

    print "Loading architecture details from %s" % path2
    arch_db = load_uops(path2, silent)

    print "Generating man pages in %s" % targetdir
    gen = Generator(db, arch_db)
    gen.generate(targetdir)


if __name__ == '__main__':
    main()
