Name:       man-intrinsics
Version:    1
Release:    1
Summary:    Most simple RPM package
License:    FIXME
BuildArch:  noarch
#BuildRoot:  %{_builddir}

%description
This is my first RPM package, which does nothing.

%prep
exit 0

%build
exit 0

%install
mkdir -p %{buildroot}/usr/share/man/man7
cp -R files %{buildroot}/usr/share/man/man7
exit 0

%files
