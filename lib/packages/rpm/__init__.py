from .rpm import RpmSupport


def create_spec_file(options, datasource, generated_files):
    rpm = RpmSupport(options, datasource, generated_files)
    rpm.create()
