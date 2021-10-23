# grab https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage

# mkdir {name}.AppDir
# mkdir {name}.AppDir/usr
# mkdir {name}.AppDir/usr/bin

# cp {binary} {name}.AppDir/usr/bin/

# cp {icon.png} {name}.AppDir/

# cat > {name}.AppDir/{name}.desktop << EOF
[Desktop Entry]
Name={name}
Exec={binary}
Icon={icon.png} (no extension?)
Type=Application
Categories=???
EOF

# cat > {name}.AppDir/AppRun << EOF
#!/bin/sh

THIS_DIR="$(dirname "$(readlink -f "${0}")")"
exec "${HERE}/usr/bin/{binary}"
EOF

# chmod 555 {name}.AppDir/AppRun


# ARCH=x86_64 appimagetool {name}.AppDir/

