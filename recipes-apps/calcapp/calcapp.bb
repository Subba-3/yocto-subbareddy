DESCRIPTION = "Calculator App"

LICENSE = "MIT"

LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://calcapp.py"

S = "${WORKDIR}"
PV ="3.0"
RDEPENDS:${PN} += "python3-core"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/calcapp.py ${D}${bindir}/calcapp
}
