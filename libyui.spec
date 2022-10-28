%define major 15
%define libname %mklibname yui %{major}
%define develname %mklibname -d yui

Name:		libyui
Version:	4.3.3
Release:	1
Summary:	User interface abstraction layer
Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/libyui/libyui
Source0:	https://github.com/libyui/libyui/archive/%{name}-%{version}.tar.xz

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	ghostscript
BuildRequires:	boost-devel
BuildRequires:	libtool


%description
libYUI is a library written entirely in C++ to provide an abstraction layer
for Qt, GTK and ncurses UI frameworks. This means that a single code in YUI
can be used to produce outputs using any of the 3 UI frameworks listed above.
This library was (and still is) used to create the YaST2 User Interface. 

#----------------------------------------------------------

%package -n %{libname}
Summary:	%{summary}
Group:		System/Libraries
Provides:	%{name} = %{EVRD}
Obsoletes:	%{name} < 2.21.1-2
Conflicts:	%{name} < 2.21.1-2

%description -n %{libname}
This package contains the library needed to run programs
dynamically linked with libyui.

%files -n %{libname}
#%%dir %{_libdir}/yui
%dir %{_datadir}/libyui
%{_libdir}/lib*.so.%{major}*

#----------------------------------------------------------

%package -n %{develname}
Summary:	libYUI, YaST2 User Interface Engine - header files
Group:		Development/C++
Requires:	%{name} >= %{version}
Requires:	boost-devel
Provides:	%{name}-devel = %{EVRD}
Provides:	yui-devel = %{EVRD}
Obsoletes:	%{name}-devel < 2.21.1-2
Conflicts:	%{name}-devel < 2.21.1-2

%description -n %{develname}
This is the development package for libyui user interface engine
that provides the abstraction from graphical user interfaces (Qt, Gtk)
and text based user interfaces (ncurses).

%files -n %{develname}
%dir %{_docdir}/packages/libyui%{major}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/yui
#%%{_libdir}/cmake/libyui
%{_datadir}/libyui/buildtools
%doc %{_docdir}/packages/libyui%{major}/examples/*
%doc %{_docdir}/packages/libyui%{major}/doc/html/
#----------------------------------------------------------

%prep
%autosetup -p1

%build

%cmake \
	-DWERROR=off \
	-DCMAKE_BUILD_TYPE=RELWITHDEBINFO \
	-DBUILD_DOC=on \
	-G Ninja

%ninja_build

%ninja_build doc

%install
%ninja_install -C build
install -m0755 -d %{buildroot}/%{_libdir}/yui
mkdir -p %{buildroot}%{_docdir}/packages/libyui%{major}/doc/html
cp -R  build/doc/html/ %{buildroot}%{_docdir}/packages/libyui%{major}/doc/
