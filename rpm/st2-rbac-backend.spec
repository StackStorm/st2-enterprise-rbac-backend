%define pkg_version %(python setup.py --version 2>/dev/null)
%define version %(echo "${PKG_VERSION:-%{pkg_version}}")
#define epoch %(_epoch=`echo %{version} | grep -q dev || echo 1`; echo "${_epoch:-0}")
%define release %(echo "${PKG_RELEASE:-1}")
%define st2dir /opt/stackstorm
%define st2wheels %{st2dir}/share/wheels
%define pip %{st2dir}/st2/bin/pip

Name:           st2-rbac-backend
Version:        %{version}
%if 0%{?epoch}
Epoch: %{epoch}
%endif
Release:        %{release}
License:        StackStorm Enterprise EULA
Summary:        LDAP auth backend for st2
URL:            https://stackstorm.com/
Source0:        st2-enterprise-auth-backend-ldap

Requires: st2 openldap

%define _builddir %(pwd)
%define _rpmdir %(pwd)/build

%description
  RBAC Backend for StackStorm Enterprise Edition

%prep
  rm -rf %{buildroot}
  mkdir -p %{buildroot}

%post
  %include rpm/postinst_script.spec

%build
  make

%install
  %make_install

%clean
  rm -rf %{buildroot}

%post
  %{pip} install --find-links %{st2wheels} --no-index --quiet --upgrade st2-enterprise-rbac-backend

%postun
  if [ $1 -eq 0 ]; then
    echo y | %{pip} uninstall st2-enterprise-rbac-backend 1>/dev/null || :
  fi

%files
  %doc rpm/LICENSE
  %{st2wheels}/*
