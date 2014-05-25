# TODO:
# - build kernel + modules
# - move /etc/default to /etc/sysconfig
Summary:	Single System Image operating system for clusters
Summary(pl.UTF-8):	System operacyjny o pojedynczym obrazie dla klastrów
Name:		kerrighed
Version:	3.0.0
Release:	0.1
License:	GPL v2 (kernel), LGPL v2.1 (libraries)
Group:		Applications
Source0:	http://gforge.inria.fr/frs/download.php/27161/%{name}-%{version}.tar.gz
# Source0-md5:	1fa72bdc458bf47a355f167e01ff6baf
URL:		http://www.kerrighed.org/
BuildRequires:	libxslt-progs
BuildRequires:	python >= 1:2.5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kerrighed is a Single System Image operating system for clusters. It
offers the view of a unique SMP machine on top of a cluster of
standard PCs.

Kerrighed is implemented as an extension to Linux operating system (a
set of Linux modules and a small patch to the kernel).

Kerrighed main features are:
 - Customizable Cluster Wide Process Scheduler.
 - Cluster Wide Shared Memory.
 - Process Checkpointing.
 - Cluster Wide Unix Process Interface.
 - Customizable Single System Image Features.

%description -l pl.UTF-8
Kerrighed to system operacyjny o pojedynczym obrazie dla klastrów.
Zapewnia widok pojedynczej maszyny SMP, opartej na klastrze zwykłych
komputerów PC.

Kerrighed jest zaimplementowany jako rozszerzenie systemu operacyjnego
Linux (zestaw modułów Linuksa oraz mała łata na jądro).

Główne cechy klastra Kerrighed to:
 - konfigurowalny planista procesów dla całego klastra
 - pamięć współdzielona dla całego klastra
 - zamrażanie procesów
 - interfejs do zarządzania procesami uniksowymi na całym klastrze
 - konfigurowalne właściwości pojedynczego obrazu systemu

%package libs
Summary:	Kerrighed cluster libraries
Summary(pl.UTF-8):	Biblioteki klastra Kerrighed
Group:		Libraries

%description libs
Kerrighed cluster libraries.

%description libs -l pl.UTF-8
Biblioteki klastra Kerrighed.

%package devel
Summary:	Header files for Kerrighed libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Kerrighed
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Kerrighed libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Kerrighed.

%package static
Summary:	Static Kerrighed cluster libraries
Summary(pl.UTF-8):	Statyczne biblioteki klastra Kerrighed
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Kerrighed cluster libraries.

%description static -l pl.UTF-8
Statyczne biblioteki klastra Kerrighed.

%package -n python-kerrighed
Summary:	Python interface to Kerrighed library
Summary(pl.UTF-8):	Interfejs Pythona do biblioteki Kerrighed
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-kerrighed
Python interface to Kerrighed library.

%description -n python-kerrighed -l pl.UTF-8
Interfejs Pythona do biblioteki Kerrighed.

%package tools
Summary:	Kerrighed cluster management tools
Summary(pl.UTF-8):	Narzędzia do zarządzania klastrem Kerrighed
Group:		Applications/System
Requires:	%{name}-libs = %{version}-%{release}

%description tools
Kerrighed cluster management tools.

%description tools -l pl.UTF-8
Narzędzia do zarządzania klastrem Kerrighed.

%package -n bash-completion-kerrighed
Summary:	Bash completion for Kerrighed commands
Summary(pl.UTF-8):	Bashowe dopełnianie poleceń klastra Kerrighed
Group:		Applications/Shells
Requires:	%{name}-tools = %{version}-%{release}
Requires:	bash-completion

%description -n bash-completion-kerrighed
Bash completion for Kerrighed commands.

%description -n bash-completion-kerrighed -l pl.UTF-8
Bashowe dopełnianie poleceń klastra Kerrighed.

%prep
%setup -q

%build
%configure \
	--disable-kernel \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# PLDify paths
install -d $RPM_BUILD_ROOT/etc/rc.d
%{__mv} $RPM_BUILD_ROOT/etc/init.d $RPM_BUILD_ROOT/etc/rc.d

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files libs
%doc AUTHORS ChangeLog README
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkerrighed.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkerrighed.so.2
%attr(755,root,root) %{_libdir}/libkrgcb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkrgcb.so.1
%attr(755,root,root) %{_libdir}/libkrgcheckpoint.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkrgcheckpoint.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkerrighed.so
%attr(755,root,root) %{_libdir}/libkrgcb.so
%attr(755,root,root) %{_libdir}/libkrgcheckpoint.so
%{_includedir}/kerrighed
%{_pkgconfigdir}/kerrighed.pc
%{_pkgconfigdir}/krgcb.pc
%{_pkgconfigdir}/krgcheckpoint.pc
%{_mandir}/man2/krgcapset.2*
%{_mandir}/man2/migrate.2*
%{_mandir}/man2/migrate_self.2*

%files static
%defattr(644,root,root,755)
%{_libdir}/libkerrighed.a
%{_libdir}/libkrgcb.a
%{_libdir}/libkrgcheckpoint.a

%files -n python-kerrighed
%defattr(644,root,root,755)
%{py_sitescriptdir}/kerrighed.py[co]

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/checkpoint
%attr(755,root,root) %{_bindir}/ipccheckpoint
%attr(755,root,root) %{_bindir}/ipcrestart
%attr(755,root,root) %{_bindir}/krgcapset
%attr(755,root,root) %{_bindir}/krgcr-run
%attr(755,root,root) %{_bindir}/migrate
%attr(755,root,root) %{_bindir}/restart
%attr(755,root,root) %{_sbindir}/krg_legacy_scheduler
%attr(755,root,root) %{_sbindir}/krgadm
%attr(755,root,root) %{_sbindir}/krgboot
%attr(755,root,root) %{_sbindir}/krgboot_helper
%attr(755,root,root) %{_sbindir}/krginit
%attr(755,root,root) %{_sbindir}/krginit_helper
%attr(754,root,root) /etc/rc.d/init.d/kerrighed
%attr(754,root,root) /etc/rc.d/init.d/kerrighed-host
# TODO: /etc/sysconfig
%config(noreplace) %verify(not md5 mtime size) /etc/default/kerrighed
%config(noreplace) %verify(not md5 mtime size) /etc/default/kerrighed-host
%dir %{_sysconfdir}/kerrighed
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kerrighed/krginit_helper.conf
%{_mandir}/man1/checkpoint.1*
%{_mandir}/man1/ipccheckpoint.1*
%{_mandir}/man1/ipcrestart.1*
%{_mandir}/man1/krgadm.1*
%{_mandir}/man1/krgcapset.1*
%{_mandir}/man1/krgcr-run.1*
%{_mandir}/man1/migrate.1*
%{_mandir}/man1/restart.1*
%{_mandir}/man7/kerrighed.7*
%{_mandir}/man7/kerrighed_capabilities.7*

%files -n bash-completion-kerrighed
%defattr(644,root,root,755)
/etc/bash_completion.d/kerrighed
