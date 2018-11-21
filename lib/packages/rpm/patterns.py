DEFAULT_DIR="/usr/share/man/man7"

SPEC="""Name:       man-intrinsics
Version:    %(version)s
Release:    1
Summary:    The list of x86 instrinsics
License:    unknown
Group:      Documentation
BuildArch:  noarch

%%description
%(description)s

%%prep
exit 0

%%build
exit 0

%%install
mkdir -p %%{buildroot}%(installdir)s
cp -R . %%{buildroot}%(installdir)s

%%files
%%defattr(444, root, root)
%(files)s
"""
