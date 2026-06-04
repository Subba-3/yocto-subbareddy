DESCRIPTION = "WiFi Setup Application for RPi4 Yocto"

LICENSE = "MIT"

LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://wifiapp.sh"

S = "${WORKDIR}"

RDEPENDS:${PN} += " \
    iw \
    wpa-supplicant \
    iproute2 \
    busybox \
"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/wifiapp.sh ${D}${bindir}/wifiapp
}
