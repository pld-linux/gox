%define		pkgname		gox
Summary:	Simple Go Cross Compilation
Name:		gox
Version:	0.3.0
Release:	0.2
License:	MPLv2.0
Group:		Development
Source0:	https://github.com/mitchellh/gox/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2a05d9e53772c11a683a06a557ad0002
URL:		https://github.com/mitchellh/gox
BuildRequires:	golang >= 1.1
#BuildRequires:	golang(github.com/mitchellh/iochan)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		import_path	github.com/mitchellh/%{pkgname}

%description
Gox is a simple, no-frills tool for Go cross compilation that behaves
a lot like standard go build. Gox will parallelize builds for multiple
platforms. Gox will also build the cross-compilation toolchain for
you.

%prep
%setup -q

install -d src/$(dirname %{import_path})
ln -s ../../.. src/%{import_path}

install -d bin

%build
# set the GOPATH so that internal dependencies are automatically downloaded to the correct location
export GOPATH=$(pwd)

# set the GOBIN so compiled files go into the builddir
export GOBIN=$(pwd)/bin

go get -v github.com/mitchellh/iochan

%gobuild -o bin/%{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p bin/gox $RPM_BUILD_ROOT%{_bindir}/gox

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gox
