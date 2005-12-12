%include	/usr/lib/rpm/macros.perl
Summary:	AddUser-NG for UNIX
Summary(pl):	AddUser-NG dla system�w UNIX
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

%description -l pl
AddUser-NG oznacza AddUser Next Generation, czyli nast�pna generacja
skryptu adduser. S�u�y on do zak�adania kont u�ytkownikom w systemach
uniksowych. Przede wszystkim u�yteczny dla administrator�w, kt�rzy
tworz� du�o kont o powtarzaj�cych si� w�a�ciwo�ciach. Jest tak�e
napisany w perlu, ale zosta� zaprojektowany aby by� bardziej
elastyczny, posiada� wi�ksze mo�liwo�ci konfiguracji oraz by�
modularny:
- posiada wtyczki do administracji u�ytkownikami oraz grupami,
- posiada r�ne interfejsy u�ytkownika (UI),
- posiada dobr� dokumentacj� (r�wnie� na temat jak pisa� w�asne
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
