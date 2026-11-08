"""Resolve local sourcebook locations without changing committed provenance."""
import os
from pathlib import Path, PureWindowsPath

LEGACY_ROOTS = (r'I:\Sourcebooks', r'D:\Backup\I-drive\Sourcebooks')


def sourcebooks_root(explicit=None):
    value = explicit or os.environ.get('NEW_PATH_SOURCEBOOKS')
    if value:
        return Path(value).expanduser().resolve()
    return None


def local_path(value):
    # Windows-relative provenance must also work on POSIX hosts.
    return Path(str(value).replace('\\', '/'))


def resolve_source(value, root=None):
    """Remap only known Sourcebooks prefixes; explicit roots never fall back."""
    root = sourcebooks_root(root)
    win = PureWindowsPath(str(value))
    if root:
        for old in LEGACY_ROOTS:
            try:
                relative = win.relative_to(PureWindowsPath(old))
            except ValueError:
                continue
            return root.joinpath(*relative.parts)
    return local_path(value) if not win.drive else Path(value)
