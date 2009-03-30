%define name		zn_poly
%define version		0.9
%define devstatic	%mklibname -d -s %{name}

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	Polynomial arithmetic in Z/nZ[x]
Version:	%{version}
Release:	%mkrel 1
Source:		http://cims.nyu.edu/~harvey/zn_poly/releases/%{name}-%{version}.tar.gz
URL:		http://cims.nyu.edu/~harvey/zn_poly/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	gmp-devel
BuildRequires:	ntl-devel

%description
zn_poly is a C library for polynomial arithmetic in Z/nZ[x],
where n is any modulus that fits into an unsigned long. 

%package	-n %{devstatic}
Group:		Development/C
Summary:	Polynomial arithmetic in Z/nZ[x]

%description	-n %{devstatic}
zn_poly is a C library for polynomial arithmetic in Z/nZ[x],
where n is any modulus that fits into an unsigned long. 

%prep
%setup -q

%build
# this script actually just calls makemakefile.py, and it doesn't like
# options it doesn't know about.
sed -i	-e 's|^ntl_include_dir.*|ntl_include_dir = options.ntl_prefix + "/NTL/include"|'	\
	-e 's|" % prefix|" % ("%{buildroot}" + prefix)|'	\
	makemakefile.py
/bin/sh ./configure --prefix=%{_prefix} --cflags="%{optflags}"

make

%install
make install

%clean
rm -rf %{buildroot}

%files		-n %{devstatic}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*
%doc doc/REFERENCES
