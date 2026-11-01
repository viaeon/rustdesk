Name:       remote
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/remote/
mkdir -p %{buildroot}/usr/share/remote/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/remote %{buildroot}/usr/bin/remote
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/remote/libsciter-gtk.so
install $HBB/res/remote.service %{buildroot}/usr/share/remote/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/remote.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/remote.svg
install $HBB/res/remote.desktop %{buildroot}/usr/share/remote/files/
install $HBB/res/remote-link.desktop %{buildroot}/usr/share/remote/files/

%files
/usr/bin/remote
/usr/share/remote/libsciter-gtk.so
/usr/share/remote/files/remote.service
/usr/share/icons/hicolor/256x256/apps/remote.png
/usr/share/icons/hicolor/scalable/apps/remote.svg
/usr/share/remote/files/remote.desktop
/usr/share/remote/files/remote-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop rustdesk || true
  ;;
esac

%post
cp /usr/share/remote/files/remote.service /etc/systemd/system/remote.service
cp /usr/share/remote/files/remote.desktop /usr/share/applications/
cp /usr/share/remote/files/remote-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable rustdesk
systemctl start rustdesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop rustdesk || true
    systemctl disable rustdesk || true
    rm /etc/systemd/system/remote.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/remote.desktop || true
    rm /usr/share/applications/remote-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
