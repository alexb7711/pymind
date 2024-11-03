########################################################################################################################
# __version_info__ format:
#     (major, minor, patch, dev/alpha/beta/rc/final, #)
#     (1, 1, 2, 'dev', 0) => "1.1.2.dev0"
#     (1, 1, 2, 'alpha', 1) => "1.1.2a1"
#     (1, 2, 0, 'beta', 2) => "1.2b2"
#     (1, 2, 0, 'rc', 4) => "1.2rc4"
#     (1, 2, 0, 'final', 0) => "1.2"
########################################################################################################################

########################################################################################################################
# Functions
########################################################################################################################


##======================================================================================================================
#
def _get_version(version_info):
    "Returns a PEP 440-compliant version number from `version_info`."
    assert len(version_info) == 5
    assert version_info[3] in ("dev", "alpha", "beta", "rc", "final")

    parts = 2 if version_info[2] == 0 else 3
    v = ".".join(map(str, version_info[:parts]))

    if version_info[3] == "dev":
        v += ".dev" + str(version_info[4])
    elif version_info[3] != "final":
        mapping = {"alpha": "a", "beta": "b", "rc": "rc"}
        v += mapping[version_info[3]]

    return v


########################################################################################################################
# Global Variables
########################################################################################################################

__version_info__ = (0, 0, 0, "dev", 0)
__version__ = _get_version(__version_info__)
