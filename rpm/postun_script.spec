uninstall_package() {
  PIP=/opt/stackstorm/st2/bin/pip
  echo y | ${PIP} uninstall st2-enterprise-rbac-backend 1>/dev/null || :
}

disable_rbac() {
  crudini --set /etc/st2/st2.conf rbac enable 'False'
  crudini --del /etc/st2/st2.conf rbac backend
}

if [ $1 -eq 0 ]; then
  uninstall_package
  disable_rbac
fi
