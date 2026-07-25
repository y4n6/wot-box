# -*- coding: utf-8 -*-
import io
import os
import shutil
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGINAL_DIR = os.path.join(ROOT, 'original')
ATLAS_WOTMOD_PATH = os.path.join(ORIGINAL_DIR, 's0urce.box.combat.eff.atlas.wotmod')
BUILD_DIR = os.path.join(ROOT, '.build')
ATLAS_EXTRACT_DIR = os.path.join(BUILD_DIR, 'extracted_atlas')
ATLAS_MANIFEST_PATH = os.path.join(BUILD_DIR, 'atlas_manifest.txt')


def reset_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def ensure_parent(path):
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent)


def extract_wotmod(wotmod_path, extract_dir):
    reset_dir(extract_dir)
    with zipfile.ZipFile(wotmod_path, 'r') as zf:
        zf.extractall(extract_dir)


def extract_atlas_wotmod():
    extract_wotmod(ATLAS_WOTMOD_PATH, ATLAS_EXTRACT_DIR)
    with zipfile.ZipFile(ATLAS_WOTMOD_PATH, 'r') as zf:
        ensure_parent(ATLAS_MANIFEST_PATH)
        with io.open(ATLAS_MANIFEST_PATH, 'w', encoding='utf-8') as manifest:
            for info in zf.infolist():
                manifest.write(u'%s\t%s\n' % (info.filename, info.file_size))
    print('Atlas manifest: %s' % os.path.relpath(ATLAS_MANIFEST_PATH, ROOT))
    print('Atlas extracted to: %s' % os.path.relpath(ATLAS_EXTRACT_DIR, ROOT))


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else 'atlas'
    if target == 'atlas':
        if not os.path.exists(ATLAS_WOTMOD_PATH):
            raise SystemExit('Missing atlas input: %s' % ATLAS_WOTMOD_PATH)
        extract_atlas_wotmod()
        return

    raise SystemExit('Usage: decompile_wotmod.py [atlas]')


if __name__ == '__main__':
    main()
