DESCRIPTION = "Simple OTA Client"

LICENSE = "MIT"

LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://ota-client.py"

S = "${WORKDIR}"

RDEPENDS:${PN} += " \
    python3-core \
    python3-requests \
    wget \
    opkg \
"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/ota-client.py ${D}${bindir}/ota-client
    install -d ${D}${sysconfdir}/ota-client
}
