# Spec file taken from upstream, thanks. -AdamW 2007/06

%define svn	0
%define rel	3
%if %svn
%define	release		0.%{svn}.%{rel}
%define distname	%{name}-%{svn}.tar.xz
%define dirname		%{name}
%else
%define release		%{rel}
%define distname	%{name}-%{version}.tar.gz
%define dirname		%{name}-%{version}
%endif

Name:		mediatomb
Summary:	UPnP AV MediaServer
Version:	0.12.1
Release:	%{release}
License:	GPLv2
Group:		Networking/Remote access
URL:		http://mediatomb.cc
Source0:	http://downloads.sourceforge.net/mediatomb/%{distname}
Source1:	mediatomb.logrotate
# Adds parallel init info to init.d script - AdamW 2007/06
Patch0:		mediatomb-0.11.0-initinfo.patch
Patch1:		mediatomb-0.12.1-gcc46.patch
Patch2:		mediatomb-0.12.1-gcc47.patch
Patch3:		mediatomb-0.12.1-mozjs185.patch
Patch4:		mediatomb-0.12.1.tonewjs.patch
Patch5:		mediatomb-0.12.1-jsparse.patch
Patch6:		mediatomb-0.12.1-libmp4v2.patch
Patch7:		libav_0.7_support.patch
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	magic-devel
BuildRequires:	libid3-devel
BuildRequires:	libmp4v2-devel
BuildRequires:	pkgconfig(taglib)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	ffmpeg-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	file
BuildRequires:	js-devel

%description
MediaTomb - UPnP AV Mediaserver for Linux.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
autoreconf -fi
%configure2_5x \
	--enable-taglib \
	--enable-libjs \
	--with-js-h=%{_includedir}/js \
	--enable-external-transcoding \
	--enable-protocolinfo-extension

%make

%install
install -D -m 0755 scripts/mediatomb-service-fedora %{buildroot}%{_initrddir}/%{name}
install -D -m 0755 config/mediatomb-conf-fedora %{buildroot}%{_sysconfdir}/%{name}.conf

%makeinstall_std

mkdir -p %{buildroot}%{_logdir}
touch %{buildroot}%{_logdir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}/etc/logrotate.d/%{name}

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

