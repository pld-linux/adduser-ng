Summary:	AddUser-NG for UNIX
Summary(pl.UTF-8):	AddUser-NG dla systemów UNIX
Name:		adduser-ng
Version:	0.1.2
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://ftp.adduser.linux.pl/release-%{version}/source/%{name}_%{version}.tar.gz
# Source0-md5:	038932880d52c1655d9d9da57068b2da
Patch0:		%{name}-Makefile.patch
URL:		http://adduser.linux.pl
BuildRequires:	rpm-perlprov
Requires:	perl-Config-IniFiles
Requires:	perl-Getopt-Mixed
Requires:	perl-Term-ReadLine-Perl
Requires:	perl-XML-Simple
Requires:	perl-base >= 1:5.8.0
Requires:	shadow
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AddUser-NG stands for AddUser Next Generation. It's meant to be a
replacement for adduser script. Most of all it's useful for system
administrators, which create a lot of users' accounts with the same
characteristics. It's written in perl with flexibility and modularity
kept in mind. Major advantages:
- built-in plugins for user and groups administration,
- set of different User Interfaces,
- good documentation including plugins writting howto.

%description -l pl.UTF-8
AddUser-NG oznacza AddUser Next Generation, czyli następna generacja
skryptu adduser. Służy on do zakładania kont użytkownikom w systemach
uniksowych. Przede wszystkim użyteczny dla administratorów, którzy
tworzą dużo kont o powtarzających się właściwościach. Jest także
napisany w perlu, ale został zaprojektowany aby był bardziej
elastyczny, posiadał większe możliwości konfiguracji oraz był
modularny:
- posiada wtyczki do administracji użytkownikami oraz grupami,
- posiada różne interfejsy użytkownika (UI),
- posiada dobrą dokumentację (również na temat jak pisać własne
  wtyczki).

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	DESTDIR=$RPM_BUILD_ROOT

touch Makefile.PL
%{__perl} -MExtUtils::MakeMaker -e 'WriteMakefile(NAME=>"AddUser")' \
	INSTALLDIRS=vendor
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/%{name}/groups,%{_datadir}/%{name}/plugins}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install adduser $RPM_BUILD_ROOT%{_bindir}
install adduser-ng/adduser-ng.conf-dist $RPM_BUILD_ROOT%{_sysconfdir}/adduser-ng/adduser-ng.conf
install adduser-ng/groups/adduser $RPM_BUILD_ROOT%{_sysconfdir}/adduser-ng/groups
install lib/AddUser/plugins/* $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins
install Docs/plugins/* $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Docs/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{perl_vendorlib}/AddUser
%dir %{_sysconfdir}/adduser-ng
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/adduser-ng/adduser-ng.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/adduser-ng/groups/adduser
%{_datadir}/%{name}
%{_mandir}/man3/*
