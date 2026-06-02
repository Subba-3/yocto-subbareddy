DESCRIPTION = "Realtime CPU Memory Monitor"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"
SRC_URI = "file://sysmonitor.py"
S = "${WORKDIR}"
RDEPENDS:${PN} += "python3-core"
do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/sysmonitor.py ${D}${bindir}/sysmonitor
}
