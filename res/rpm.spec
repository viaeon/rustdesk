Name:       remote
Version:    1.4.2
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://viaeon.com
Vendor:     remote
Requires:   gtk3 libxcb libxdo libXfixes alsa-lib libva2 pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3

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
install $HBB/res/rustdesk.service %{buildroot}/usr/share/remote/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/remote.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/remote.svg
install $HBB/res/rustdesk.desktop %{buildroot}/usr/share/remote/files/
install $HBB/res/rustdesk-link.desktop %{buildroot}/usr/share/remote/files/

%files
/usr/bin/remote
/usr/share/remote/libsciter-gtk.so
/usr/share/remote/files/rustdesk.service
/usr/share/icons/hicolor/256x256/apps/remote.png
/usr/share/icons/hicolor/scalable/apps/remote.svg
/usr/share/remote/files/rustdesk.desktop
/usr/share/remote/files/rustdesk-link.desktop
/usr/share/remote/files/__pycache__/*

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
cp /usr/share/remote/files/rustdesk.service /etc/systemd/system/rustdesk.service
cp /usr/share/remote/files/rustdesk.desktop /usr/share/applications/
cp /usr/share/remote/files/rustdesk-link.desktop /usr/share/applications/
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
    rm /etc/systemd/system/rustdesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/rustdesk.desktop || true
    rm /usr/share/applications/rustdesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
