# -*- coding: utf-8 -*-
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS_SRC_DIR = os.path.join(ROOT, 'src', 'atlas')
BUILD_DIR = os.path.join(ROOT, '.build')
ATLAS_MANIFEST_PATH = os.path.join(BUILD_DIR, 'atlas_manifest.txt')


def ensure_parent(path):
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent)


def normalize_arcname(path):
    return path.replace('\\', '/')


def iter_atlas_files():
    for base, _dirs, files in os.walk(ATLAS_SRC_DIR):
        for name in files:
            path = os.path.join(base, name)
            arcname = normalize_arcname(os.path.relpath(path, ATLAS_SRC_DIR))
            yield path, arcname


def write_atlas_manifest():
    if not os.path.exists(ATLAS_SRC_DIR):
        raise SystemExit('Missing atlas source directory: %s' % ATLAS_SRC_DIR)
    ensure_parent(ATLAS_MANIFEST_PATH)
    with io.open(ATLAS_MANIFEST_PATH, 'w', encoding='utf-8') as manifest:
        for path, arcname in sorted(iter_atlas_files(), key=lambda item: item[1]):
            manifest.write(u'%s\t%s\n' % (arcname, os.path.getsize(path)))
    print('Atlas manifest: %s' % os.path.relpath(ATLAS_MANIFEST_PATH, ROOT))
    print('Atlas source: %s' % os.path.relpath(ATLAS_SRC_DIR, ROOT))


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else 'atlas'
    if target == 'atlas':
        write_atlas_manifest()
        return

    raise SystemExit('Usage: decompile_wotmod.py [atlas]')


if __name__ == '__main__':
    main()
