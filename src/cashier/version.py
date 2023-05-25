"""Library version."""
import pkg_resources


def get_version() -> str:
    """To return the global version constant.

    Returns:
        Global software version.
    """
    return pkg_resources.get_distribution("cashier").version
