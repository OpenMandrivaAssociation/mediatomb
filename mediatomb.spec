# Spec file taken from upstream, thanks. -AdamW 2007/06

%define svn	0
%define rel	1
%if %svn
%define	release		%mkrel 0.%{svn}.%{rel}
%define distname	%{name}-%{svn}.tar.xz
%define dirname		%{name}
%else
%define release		%mkrel %{rel}
%define distname	%{name}-%{version}.tar.gz
%define dirname		%{name}-%{version}
%endif

Name:		mediatomb
Summary:	UPnP AV MediaServer 
Version:	0.12.1
Release:	%{release}
License:	GPLv2
Group:		Networking/Remote access
Source0:	http://downloads.sourceforge.net/mediatomb/%{distname}
Source1:	mediatomb.logrotate
# Adds parallel init info to init.d script - AdamW 2007/06
Patch0:		mediatomb-0.11.0-initinfo.patch
Patch1:		mediatomb-0.12.1-gcc-4.7.patch
Patch2:		https://launchpadlibrarian.net/71985647/libav_0.7_support.patch
URL:		http://mediatomb.cc
BuildRequires:	sqlite3-devel
BuildRequires:	magic-devel
BuildRequires:	libid3-devel
BuildRequires:	taglib-devel
BuildRequires:	libexif-devel
BuildRequires:	curl-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	expat-devel
BuildRequires:	file
BuildRequires:	pkgconfig(libjs) >= 1.70

%description
MediaTomb - UPnP AV Mediaserver for Linux.

%prep 
%setup -q
%patch0 -p1 -b .init~
%patch1 -p1 -b .gcc47~
%patch2 -p1 -b .libav07~

%build
%if %svn
autoreconf -i
%endif

# configure script doesn't know where we keep the libjs headers - AdamW 2007/06
export JS_SEARCH_HEADERS=/usr/include/js-1.70 

%configure2_5x --enable-taglib --enable-external-transcoding --enable-protocolinfo-extension
%make

%install
rm -rf %{buildroot}

install -D -m 0755 scripts/mediatomb-service-fedora %{buildroot}%{_initrddir}/%{name}
install -D -m 0755 config/mediatomb-conf-fedora %{buildroot}%{_sysconfdir}/%{name}.conf

%makeinstall_std

mkdir -p %{buildroot}%{_logdir}
touch %{buildroot}%{_logdir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}/etc/logrotate.d/%{name}

%clean
rm -rf %{buildroot}

%pre
# Create a user
%_pre_useradd %{name} %{_localstatedir}/lib/%{name} /bin/false

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
%doc README README.UTF_8 AUTHORS ChangeLog INSTALL doc/doxygen.conf
%doc doc/scripting.txt doc/scripting_utf8.txt
%{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_initrddir}/%{name}
%defattr(-,%{name},%{name})
%config(noreplace) %{_sysconfdir}/%{name}.conf
%ghost %{_logdir}/%{name}
