DESCRIPTION = "Subbareddy Custom Embedded OS"

LICENSE = "MIT"

inherit core-image
IMAGE_INSTALL += " \
    packagegroup-core-boot \
    kernel-modules \
    openssh \
    python3 \
    wget \
    opkg \
    wifiapp \
    sysinfoapp \
    ota-client \
    iw \
    wpa-supplicant \
    dhcpcd \
    iproute2 \
    linux-firmware \
"

IMAGE_INSTALL[vardepsexclude] += "NO_RECOMMENDATIONS"
