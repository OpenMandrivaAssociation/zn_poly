%define old_devname	%mklibname -d %{name}

Name:           zn_poly
Version:        0.9.2
Release:        1
Summary:        C library for polynomial arithmetic
# see COPYING to see, which file has which license
License:        (GPLv2 or GPLv3) and GPLv2+ and LGPLv2+
URL:            http://cims.nyu.edu/~harvey/code/zn_poly/
Source0:        https://gitlab.com/sagemath/zn_poly/-/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.rpmlintrc
BuildRequires:  gmp-devel
BuildRequires:  ntl-devel
%ifnarch %{ix86}
Requires: python
%endif

#Patch0:		zn_poly-0.9.patch

%description
zn_poly is a C library for polynomial arithmetic in Z/nZ[x], where n is
any modulus that fits into an unsigned long. 

%package	devel
Summary:	Polynomial arithmetic in Z/nZ[x]
Requires:       %{name} = %{EVRD}
%rename %{old_devname}

%description	devel
zn_poly is a C library for polynomial arithmetic in Z/nZ[x], where n is
any modulus that fits into an unsigned long. 

This package contains the development files.

%prep
%setup -q
#patch0	-p1
find . -name "*.py" |xargs 2to3 -w

%build
# this script actually just calls makemakefile.py, and it doesn't like
# options it doesn't know about.
sed -i	-e 's|^ntl_include_dir.*|ntl_include_dir = options.ntl_prefix + "/NTL/include"|'	\
	-e 's|" % prefix|" % ("%{buildroot}" + prefix)|'	\
	-e 's|/lib"|/%{_lib}"|'					\
	makemakefile.py
/bin/sh ./configure --prefix=%{_prefix} --cflags="%{optflags} -fPIC"

%make_build libzn_poly-%{version}.so

%install
%make_install

%check
make test
./test/test all

%files
%doc COPYING gpl-?.0.txt
%doc demo/bernoulli/bernoulli.c doc/REFERENCES
%{_libdir}/libzn_poly-%{version}.so

%files devel
%{_includedir}/*
%{_libdir}/libzn_poly-0.9.so


