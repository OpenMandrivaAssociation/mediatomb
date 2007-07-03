# Spec file taken from upstream, thanks. -AdamW 2007/06

%define name mediatomb 
%define version 0.9.1
%define release %mkrel 1

Version: %{version}
Summary: UPnP AV MediaServer 
Name: %{name}
Release: %{release}
License: GPL
Group: Networking/Remote access
Source0: http://downloads.sourceforge.net/mediatomb/%{name}-%{version}.tar.gz
Source1: mediatomb.logrotate
# Adds parallel init info to init.d script - AdamW 2007/06
Patch0: mediatomb-0.9.1-initinfo.patch
# Patches it to use our new config directory - AdamW 2007/06
Patch1: mediatomb-0.9.1-config.patch
URL: http://mediatomb.cc
Buildroot: %{_tmppath}/%{name}-%{version}-buildroot 
BuildRequires: sqlite3-devel
BuildRequires: libmagic-devel
BuildRequires: js-devel
BuildRequires: libid3-devel
BuildRequires: taglib-devel
BuildRequires: libexif-devel

BuildRequires: file

%description
MediaTomb - UPnP AV Mediaserver for Linux.

%prep 
%setup -q
%patch0 -p1 -b .init
%patch1 -p1 -b .config

%build
# configure script doesn't know where we keep the libjs headers - AdamW 2007/06
export JS_SEARCH_HEADERS=/usr/include/js-1.5 
%configure

%make

%install
rm -rf $RPM_BUILD_ROOT

install -D -m0755 scripts/mediatomb-service-fedora %{buildroot}%{_initrddir}/%{name}
install -D -m0755 config/mediatomb-conf-fedora %{buildroot}%{_sysconfdir}/%{name}.conf

%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_logdir}
touch $RPM_BUILD_ROOT%{_logdir}/%{name}
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre

# Create a user
%_pre_useradd %{name} %{_localstatedir}/%{name} /bin/false

%post
%_post_service %{name}

# Create initial log file so that logrotate doesn't complain
if [ $1 = 1 ]; then
   %create_ghostfile %{_logdir}/%{name} root root 644
fi

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%defattr(-,root,root)
%doc README README.UTF_8 AUTHORS ChangeLog COPYING INSTALL doc/doxygen.conf
%doc doc/scripting.txt doc/scripting_utf8.txt
%{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_initrddir}/%{name}
%defattr(-,%{name},%{name})
%config(noreplace) %{_sysconfdir}/%{name}.conf
%ghost %{_logdir}/%{name}
