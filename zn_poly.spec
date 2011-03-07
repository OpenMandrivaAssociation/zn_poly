%define name		zn_poly
%define version		0.9
%define devname		%mklibname -d %{name}

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPLv2 or GPLv3
Summary:	Polynomial arithmetic in Z/nZ[x]
Version:	%{version}
Release:	%mkrel 8
Source:		http://cims.nyu.edu/~harvey/zn_poly/releases/%{name}-%{version}.tar.gz
URL:		http://cims.nyu.edu/~harvey/zn_poly/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	gmp-devel
BuildRequires:	ntl-devel

Patch0:		zn_poly-0.9.patch

%description
zn_poly is a C library for polynomial arithmetic in Z/nZ[x],
where n is any modulus that fits into an unsigned long. 

%package	-n %{devname}
Group:		Development/C
Summary:	Polynomial arithmetic in Z/nZ[x]
Obsoletes:	%mklibname -d -s %name
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

%clean
rm -rf %{buildroot}

%files		-n %{devname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*
%doc doc/REFERENCES
