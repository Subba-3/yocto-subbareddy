DESCRIPTION = "Subbareddy Custom Embedded OS"

LICENSE = "MIT"

inherit core-image
IMAGE_INSTALL += " \
    packagegroup-core-boot \
    kernel-modules \
    openssh \
    usbutils \
    python3 \
    python3-requests \
    wget \
    opkg \
    wifiapp \
    sysinfoapp \
    ota-client \
    iw \
    wpa-supplicant \
    dhcpcd \
    iproute2 \
    rfkill \
    linux-firmware \
    linux-firmware-rpidistro-bcm43455 \
"

IMAGE_INSTALL[vardepsexclude] += "NO_RECOMMENDATIONS"
