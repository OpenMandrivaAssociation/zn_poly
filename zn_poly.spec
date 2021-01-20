%define _disable_lto 1
%global debug_package %{nil}

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
 
%build
python makemakefile.py --prefix=/usr --cflags="$CFLAGS -fPIC" --cxxflags="$CXXFLAGS" --ldflags="$LDFLAGS" > makefile
  make
  make libzn_poly.so
 
%install
# install manually, because makefile does not honor DESTDIR
mkdir -p %{buildroot}%{_includedir}/zn_poly/
mkdir -p %{buildroot}%{_libdir}
cp -pv include/*.h %{buildroot}%{_includedir}/zn_poly/
cp -pv libzn_poly.a %{buildroot}%{_libdir}
cp -pv libzn_poly-%{version}.so %{buildroot}%{_libdir}
ln -s libzn_poly-%{version}.so %{buildroot}%{_libdir}/libzn_poly-0.9.so
ln -s libzn_poly-0.9.so %{buildroot}%{_libdir}/libzn_poly.so

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


