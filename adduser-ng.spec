Summary:	AddUser-NG for UNIX
Summary(pl):	AddUser-NG dla systemów UNIX
Name:		adduser-ng
Version:	0.1.1
Release:	0.0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://teon.org/projects/AddUser-NG/download/release-%{version}/source/%{name}_%{version}-1.tar.gz
# Source0-md5:	fcc20b96e4556c0a7c06b19337ec8e54
Patch0:		%{name}-Makefile.patch
URL:		http://adduser.linux.pl
Requires:	perl-Config-IniFiles
Requires:	perl-Getopt-Mixed
Requires:	perl-XML-Simple
Requires:	perl-Term-ReadLine-Perl
Requires:	perl-base >= 1:5.8.0
Requires:	shadow
Obsoletes:	adduser
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define          _libdir         /usr/share/perl5/AddUser

%description
AddUser-NG stands for AddUser Next Generation. It's meant to be a
replacement for adduser script. Most of all it's useful for system
administrators, which create a lot of users' accounts with the same
characteristics. It's written in perl with flexibility and modularity
kept in mind. Major advantages:

    - built-in plugins for user and groups administration,
    - set of different User Interfaces.

%description -l pl
AddUser-NG oznacza AddUser Next Generation, czyli nastêpna generacja
skryptu adduser. S³u¿y on do zak³adania kont u¿ytkownikom w systemach
unixowych. Przede wszystkim u¿yteczny dla administratorów, którzy
tworz± du¿o kont o powtarzaj±cych siê w³a¶ciwo¶ciach. Jest tak¿e
napisany w perlu, ale zosta³ zaprojektowany aby by³ bardziej
elastyczny, posiada³ wiêksze mo¿liwo¶ci konfiguracji oraz by³
modularny:

    - posiada wtyczki do administracji u¿ytkownikami oraz grupami,
    - posiada ró¿ne interfejsy u¿ytkownika (UI),
    - posiada dobr± dokumentacjê (równie¿ na temat jak pisaæ w³asne
      wtyczki).

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__make} \
        CC="%{__cc}" \
        CFLAGS="%{rpmcflags}" \
	DESTDIR=$RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/{UI,plugins},%{_sysconfdir}/%{name}/groups,%{_datadir}/%{name}/plugins}

install adduser $RPM_BUILD_ROOT%{_bindir}
install adduser-ng/adduser-ng.conf-dist $RPM_BUILD_ROOT%{_sysconfdir}/adduser-ng/adduser-ng.conf
install adduser-ng/groups/adduser $RPM_BUILD_ROOT%{_sysconfdir}/adduser-ng/groups
install lib/AddUser/*.pm $RPM_BUILD_ROOT%{_libdir}
install lib/AddUser/UI/* $RPM_BUILD_ROOT%{_libdir}/UI
install lib/AddUser/plugins/* $RPM_BUILD_ROOT%{_libdir}/plugins
install lib/AddUser/plugins/* $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins
install Docs/plugins/* $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Docs/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}
%dir %{_sysconfdir}/adduser-ng
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/adduser-ng/adduser-ng.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/adduser-ng/groups/adduser
%{_datadir}/%{name}
