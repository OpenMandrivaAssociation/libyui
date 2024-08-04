%define major 16
%define oldlibname %mklibname yui 15
%define libname %mklibname yui
%define develname %mklibname -d yui

%define libname_ncurses %mklibname yui-ncurses
%define oldlibname_ncurses %mklibname yui 15-ncurses
%define develname_ncurses %mklibname -d yui-ncurses

%define libname_qt %mklibname yui-qt
%define oldlibname_qt %mklibname yui 15-qt
%define develname_qt %mklibname -d yui-qt

%global _disable_ld_no_undefined 1
%bcond_without bootstrap

%global optflags %{optflags} -DLIBSOLV_SOLVABLE_PREPEND_DEP

Name:		libyui
Version:	4.6.2
Release:	1
Summary:	User interface abstraction layer
Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/libyui/libyui
Source0:	https://github.com/libyui/libyui/archive/refs/tags/%{version}.tar.gz
Patch0:		libyui-4.6.0-c++20.patch

BuildRequires:	cmake
BuildRequires:	make
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	ghostscript
BuildRequires:	boost-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(jsoncpp)
BuildRequires:	pkgconfig(libmicrohttpd)
%if %{without bootstrap}
# Yes, this is ugly... But with libyui-bindings
# living inside libyui and libyui-mga living outside,
# the way to get a proper build is
#	- build libyui with libyui-bindings without MGA extensions
#	- build libyui-mga against it
#	- build libyui again so libyui-bindings can link to libyui-mga
BuildRequires:	%{develname} = %{version}
BuildRequires:	%{develname_ncurses} = %{version}
BuildRequires:	%{develname_qt} = %{version}
BuildRequires:	pkgconfig(libyui-mga)
%endif

# For ncurses
BuildRequires:	pkgconfig(ncursesw)

# For Qt
BuildRequires:	qmake5
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Svg)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(Qt5X11Extras)
BuildRequires:	pkgconfig(libgvc)

# For libyui-qt-pkg and libyui-ncurses-pkg
BuildRequires:	cmake(zypp)

# For libyui-bindings
BuildRequires:	swig
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(ruby)
BuildRequires:	pkgconfig(mono)
BuildRequires:	perl-devel

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
%rename		%{oldlibname}

%description -n %{libname}
This package contains the library needed to run programs
dynamically linked with libyui.

%files -n %{libname}
%{_libdir}/libyui.so.%{major}*
%dir %{_libdir}/yui
%{_libdir}/yui/libyui-rest-api.so.%{major}*

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
%{_libdir}/libyui.so
%{_libdir}/yui/libyui-rest-api.so
%{_libdir}/pkgconfig/libyui.pc
%dir %{_includedir}/yui
%{_includedir}/yui/*.h
%{_includedir}/yui/rest-api
%dir %{_datadir}/libyui
%{_datadir}/libyui/buildtools
%doc %{_docdir}/packages/libyui%{major}/examples/*
%doc %{_docdir}/packages/libyui%{major}/doc/html/
#----------------------------------------------------------

%package -n %{libname_ncurses}
Summary:	Ncurses (text based) frontend for the libyui UI library
Group:		System/Libraries
%rename		%{oldlibname_ncurses}

%description -n %{libname_ncurses}
This package contains the library needed to run programs
dynamically linked with libyui.

%files -n %{libname_ncurses}
%{_libdir}/yui/libyui-ncurses.so*
%{_libdir}/yui/libyui-ncurses-pkg.so*
%{_libdir}/yui/libyui-ncurses-rest-api.so*

#----------------------------------------------------------

%package -n %{develname_ncurses}
Summary:	libYUI, YaST2 User Interface Engine - ncurses specific header files
Group:		Development/C++
Requires:	%{libname_ncurses} >= %{version}
Requires:	%{develname} >= %{version}
Requires:	boost-devel

%description -n %{develname_ncurses}
This is the development package for libyui user interface engine
that provides the abstraction from graphical user interfaces (Qt, Gtk)
and text based user interfaces (ncurses).

This package contains files needed only for the ncurses interface

%files -n %{develname_ncurses}
%{_includedir}/yui/ncurses
%{_includedir}/yui/ncurses-pkg
%{_includedir}/yui/ncurses-rest-api
%{_libdir}/pkgconfig/libyui-ncurses.pc
#----------------------------------------------------------

%package -n %{name}-ncurses-tools
Summary:	Tools for working with the libyui ncurses frontend
Group:		System/Libraries
Requires:	screen

%description -n %{name}-ncurses-tools
Character based (ncurses) user interface component for libYUI.
libyui-terminal - useful for testing on headless machines

%files -n %{name}-ncurses-tools
%{_bindir}/libyui-terminal
#----------------------------------------------------------

%package -n %{libname_qt}
Summary:	Qt frontend for the libyui UI library
Group:		System/Libraries
%rename		%{oldlibname_qt}

%description -n %{libname_qt}
This package contains the library needed to run programs
dynamically linked with libyui.

%files -n %{libname_qt}
%{_libdir}/yui/libyui-qt.so*
%{_libdir}/yui/libyui-qt-pkg.so*
%{_libdir}/yui/libyui-qt-rest-api.so*
%{_libdir}/yui/libyui-qt-graph.so*

#----------------------------------------------------------

%package -n %{develname_qt}
Summary:	libYUI, YaST2 User Interface Engine - Qt specific header files
Group:		Development/C++
Requires:	%{libname_qt} >= %{version}
Requires:	%{develname} >= %{version}
Requires:	boost-devel

%description -n %{develname_qt}
This is the development package for libyui user interface engine
that provides the abstraction from graphical user interfaces (Qt, Gtk)
and text based user interfaces (ncurses).

This package contains files needed only for the Qt interface

%files -n %{develname_qt}
%{_includedir}/yui/qt
%{_includedir}/yui/qt-pkg
%{_includedir}/yui/qt-rest-api
%{_includedir}/yui/qt-graph
%{_libdir}/pkgconfig/libyui-qt.pc

#----------------------------------------------------------
%package -n python-yui
Summary:	Python interface to libyui
Group:		Development/Perl
Requires:	%{libname} = %{EVRD}
%rename python-libyui

%description -n python-yui
Python interface to libyui

%files -n python-yui
%{python_sitearch}/_yui.so
%{python_sitearch}/yui.py

#----------------------------------------------------------
%package -n perl-yui
Summary:	Perl interface to libyui
Group:		Development/Perl
Requires:	%{libname} = %{EVRD}

%description -n perl-yui
Perl interface to libyui

%files -n perl-yui
%{_libdir}/perl5/vendor_perl/yui.so
%{_datadir}/perl5/vendor_perl/yui.pm

#----------------------------------------------------------
%package -n mono-yui
Summary:	C# interface to libyui
Group:		Development/C#
Requires:	%{libname} = %{EVRD}

%description -n mono-yui
C# interface to libyui

%files -n mono-yui
%{_prefix}/lib/mono/yui

#----------------------------------------------------------
%package -n ruby-yui
Summary:	Ruby interface to libyui
Group:		Development/C#
Requires:	%{libname} = %{EVRD}

%description -n ruby-yui
Ruby interface to libyui

%files -n ruby-yui
%{_libdir}/ruby/vendor_ruby/_yui.so

#----------------------------------------------------------
%prep
%autosetup -p1

%build
for i in libyui libyui-rest-api libyui-qt libyui-qt-graph libyui-qt-pkg libyui-qt-rest-api libyui-ncurses libyui-ncurses-pkg libyui-ncurses-rest-api libyui-bindings; do
	cd $i
	if echo $i |grep -q pkg; then
		# libzypp headers don't like clang
		export CC=gcc
		export CXX=g++
	else
		unset CC || :
		unset CXX || :
	fi
	# We're using Unix Makefiles rather than ninja because of
	# "interesting" hacks in libyui-bindings that work only in
	# Makefiles
	%cmake \
		-DWERROR:BOOL=OFF \
		-DBUILD_DOC:BOOL=ON \
%if %{without bootstrap}
		-DWITH_MGA:BOOL=ON \
%endif
		-G "Unix Makefiles"

	%make_build

	[ "$i" != "libyui-bindings" ] && %make_build doc
	cd ../..
done

%install
install -m0755 -d %{buildroot}/%{_libdir}/yui
mkdir -p %{buildroot}%{_docdir}/packages/libyui%{major}/doc/html
for i in libyui libyui-rest-api libyui-qt libyui-qt-graph libyui-qt-pkg libyui-qt-rest-api libyui-ncurses libyui-ncurses-pkg libyui-ncurses-rest-api libyui-bindings; do
	cd $i
	%make_install -C build
	[ -d build/doc/html ] && cp -R  build/doc/html/ %{buildroot}%{_docdir}/packages/libyui%{major}/doc/
	cd ..
done
