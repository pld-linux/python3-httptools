#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Python binding for the nodejs HTTP parser
Summary(pl.UTF-8):	Wiązanie Pythona do parsera HTTP z nodejs
Name:		python3-httptools
Version:	0.6.1
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/httptools/
Source0:	https://files.pythonhosted.org/packages/source/h/httptools/httptools-%{version}.tar.gz
# Source0-md5:	cb8a0c39723c10bdcf8c13d364d60b7c
Patch0:		httptools-tests-cr.patch
URL:		https://pypi.org/project/httptools/
BuildRequires:	http-parser-devel >= 2.9.4
BuildRequires:	llhttp-devel >= 8.1.1
BuildRequires:	python3-Cython >= 0.29.24
BuildRequires:	python3-Cython < 0.30
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	http-parser >= 2.9.4
Requires:	llhttp >= 8.1.1
Requires:	python3-modules >= 1:3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
httptools is a Python binding for the nodejs HTTP parser.

%description -l pl.UTF-8
httptools to wiązanie Pythona do parsera HTTP z nodejs.

%prep
%setup -q -n httptools-%{version}
%patch -P 0 -p1

%build
%py3_build build_ext \
	--use-system-http-parser \
	--use-system-llhttp

%if %{with tests}
# change dir to hide httptools source dir
cd build-3
ln -sf ../tests tests

LC_ALL=C.UTF-8 \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
PYTHONPATH=$(echo $(pwd)/lib.linux-*) \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%dir %{py3_sitedir}/httptools
%{py3_sitedir}/httptools/*.py
%{py3_sitedir}/httptools/__pycache__
%dir %{py3_sitedir}/httptools/parser
%attr(755,root,root) %{py3_sitedir}/httptools/parser/*.cpython-*.so
%{py3_sitedir}/httptools/parser/*.py
%{py3_sitedir}/httptools/parser/__pycache__
%{py3_sitedir}/httptools-%{version}-py*.egg-info
