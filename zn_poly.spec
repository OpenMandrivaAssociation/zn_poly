%define devname		%mklibname -d %{name}

Summary:	Polynomial arithmetic in Z/nZ[x]
Name:		zn_poly
Version:	0.9
Release:	9
Group:		Sciences/Mathematics
License:	GPLv2 or GPLv3
Source:		http://cims.nyu.edu/~harvey/zn_poly/releases/%{name}-%{version}.tar.gz
URL:		http://cims.nyu.edu/~harvey/zn_poly/

BuildRequires:	gmp-devel
BuildRequires:	ntl-devel

Patch0:		zn_poly-0.9.patch

%description
zn_poly is a C library for polynomial arithmetic in Z/nZ[x],
where n is any modulus that fits into an unsigned long. 

%package	-n %{devname}
Group:		Development/C
Summary:	Polynomial arithmetic in Z/nZ[x]
Provides:	zn_poly-devel = %{version}-%{release}

%description	-n %{devname}
zn_poly is a C library for polynomial arithmetic in Z/nZ[x],
where n is any modulus that fits into an unsigned long. 

%prep
%setup -q
%patch0	-p1

%build
# this script actually just calls makemakefile.py, and it doesn't like
# options it doesn't know about.
sed -i	-e 's|^ntl_include_dir.*|ntl_include_dir = options.ntl_prefix + "/NTL/include"|'	\
	-e 's|" % prefix|" % ("%{buildroot}" + prefix)|'	\
	-e 's|/lib"|/%{_lib}"|'					\
	makemakefile.py
/bin/sh ./configure --prefix=%{_prefix} --cflags="%{optflags} -fPIC"

make libzn_poly-%{version}.so

%install
make install

%files -n %{devname}
%doc doc/REFERENCES
%{_includedir}/*
%{_libdir}/*.so


