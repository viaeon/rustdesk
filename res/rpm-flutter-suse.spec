Name:       remote
Version:    1.4.2
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://viaeon.com
Vendor:     remote
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/remote" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/remote"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/remote.service -t "%{buildroot}/usr/share/remote/files"
install -Dm 644 $HBB/res/remote.desktop -t "%{buildroot}/usr/share/remote/files"
install -Dm 644 $HBB/res/remote-link.desktop -t "%{buildroot}/usr/share/remote/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/remote.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/remote.svg"

%files
/usr/share/remote/*
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
ln -sf /usr/share/remote/remote /usr/bin/remote
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
    rm /usr/bin/remote || true
    rmdir /usr/lib/remote || true
    rmdir /usr/local/remote || true
    rmdir /usr/share/remote || true
    rm /usr/share/applications/remote.desktop || true
    rm /usr/share/applications/remote-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/remote || true
    rmdir /usr/local/remote || true
  ;;
esac
