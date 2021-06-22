class VersionBumpError(OSError):
    """Raised when there is an existing package version in the remote registry matching the version at build time."""
    pass
