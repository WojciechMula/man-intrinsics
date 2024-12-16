from .deb import DebSupport


def create_files(options, datasource):
    deb = DebSupport(options, datasource)
    deb.create()
