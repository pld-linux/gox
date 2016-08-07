Summary:	Simple Go Cross Compilation
Name:		gox
Version:	0.2.0
Release:	0.1
License:	MPLv2.0
Group:		Development
Source0:	https://github.com/mitchellh/gox/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a34e1bdec4bce04afa9643a9dadac113
URL:		https://github.com/mitchellh/gox
BuildRequires:	golang >= 1.1
#BuildRequires:	golang(github.com/mitchellh/iochan)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gox is a simple, no-frills tool for Go cross compilation that behaves
a lot like standard go build. Gox will parallelize builds for multiple
platforms. Gox will also build the cross-compilation toolchain for
you.

%prep
# For building go binaries we must install the tarballed git repo into the
# appropriate src directory
mkdir -p src/github.com/mitchellh/
cd src/github.com/mitchellh/
tar xzf %{SOURCE0}
cd -
mv src/github.com/mitchellh/%{name}-%{version}\
  src/github.com/mitchellh/%{name}

# Symlink the go lib build dependencies to the build directory
%define gopath %{_libdir}/golang
%define buildgosrc src
mkdir -p %{buildgosrc}/github.com/mitchellh
ln -sv %{gopath}/src/github.com/mitchellh/* %{buildgosrc}/github.com/mitchellh/

%build
# set the GOPATH so that internal dependencies are automatically downloaded to
# the correct location
%define packer_gopath %{_builddir}/%{name}-%{version}
export GOPATH=%{packer_gopath}

# set the GOBIN so compiled files go into the builddir
mkdir -p %{packer_gopath}/bin
export GOBIN=%{packer_gopath}/bin

# Checkout the specific tag in git for the version we are building
cd %{packer_gopath}
go get github.com/mitchellh/gox

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
cp -p %{packer_gopath}/bin/gox $RPM_BUILD_ROOT%{_bindir}/gox

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gox
