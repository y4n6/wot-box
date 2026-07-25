# -*- coding: utf-8 -*-
import io
import os
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGINAL_DIR = os.path.join(ROOT, 'original')
MAIN_WOTMOD_PATH = os.path.join(ORIGINAL_DIR, 's0urce.box.combat.eff.wotmod')
ATLAS_WOTMOD_PATH = os.path.join(ORIGINAL_DIR, 's0urce.box.combat.eff.atlas.wotmod')
BUILD_DIR = os.path.join(ROOT, 'build')
EXTRACT_DIR = os.path.join(BUILD_DIR, 'extracted')
ATLAS_EXTRACT_DIR = os.path.join(BUILD_DIR, 'extracted_atlas')
ATLAS_MANIFEST_PATH = os.path.join(BUILD_DIR, 'atlas_manifest.txt')
SRC_DIR = os.path.join(ROOT, 'src')
PY314 = r'D:\02.registered programs\Python314\python.exe'
UNCOMPYLE6 = r'D:\02.registered programs\Python314\Scripts\uncompyle6.exe'


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


def extract_main_wotmod():
    reset_dir(EXTRACT_DIR)
    with zipfile.ZipFile(MAIN_WOTMOD_PATH, 'r') as zf:
        zf.extractall(EXTRACT_DIR)


def extract_atlas_wotmod():
    extract_wotmod(ATLAS_WOTMOD_PATH, ATLAS_EXTRACT_DIR)
    with zipfile.ZipFile(ATLAS_WOTMOD_PATH, 'r') as zf:
        ensure_parent(ATLAS_MANIFEST_PATH)
        with io.open(ATLAS_MANIFEST_PATH, 'w', encoding='utf-8') as manifest:
            for info in zf.infolist():
                manifest.write(u'%s\t%s\n' % (info.filename, info.file_size))
    print('Atlas manifest: %s' % os.path.relpath(ATLAS_MANIFEST_PATH, ROOT))
    print('Atlas extracted to: %s' % os.path.relpath(ATLAS_EXTRACT_DIR, ROOT))


def collect_pyc_files():
    pyc_files = []
    for base, _dirs, files in os.walk(EXTRACT_DIR):
        for name in files:
            if name.endswith('.pyc'):
                pyc_files.append(os.path.join(base, name))
    return sorted(pyc_files)


def decompile_file(pyc_path):
    relative = os.path.relpath(pyc_path, EXTRACT_DIR)
    target = os.path.join(SRC_DIR, os.path.splitext(relative)[0] + '.py')
    ensure_parent(target)
    command = [
        UNCOMPYLE6,
        '-o',
        os.path.dirname(target),
        pyc_path,
    ]
    completed = subprocess.run(command, capture_output=True, text=True)
    return relative, target, completed.returncode, completed.stdout, completed.stderr


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else 'main'
    if target == 'atlas':
        if not os.path.exists(ATLAS_WOTMOD_PATH):
            raise SystemExit('Missing atlas input: %s' % ATLAS_WOTMOD_PATH)
        extract_atlas_wotmod()
        return

    if target != 'main':
        raise SystemExit('Usage: decompile_wotmod.py [main|atlas]')

    if not os.path.exists(MAIN_WOTMOD_PATH):
        raise SystemExit('Missing input: %s' % MAIN_WOTMOD_PATH)
    if not os.path.exists(PY314):
        raise SystemExit('Missing Python 3 runtime: %s' % PY314)
    if not os.path.exists(UNCOMPYLE6):
        raise SystemExit('Missing uncompyle6 executable: %s' % UNCOMPYLE6)

    extract_main_wotmod()
    pyc_files = collect_pyc_files()
    if not pyc_files:
        raise SystemExit('No .pyc files found in %s' % EXTRACT_DIR)

    failures = []
    for pyc_path in pyc_files:
        relative, target, code, out, err = decompile_file(pyc_path)
        print('decompile:', relative, '->', os.path.relpath(target, ROOT))
        if code != 0:
            failures.append((relative, code, out, err))

    if failures:
        print('\nFAILED MODULES: %d' % len(failures))
        for relative, code, out, err in failures:
            print('--- %s (exit=%s) ---' % (relative, code))
            if out:
                print(out)
            if err:
                print(err)
        raise SystemExit(1)

    print('\nDone. Decompiled %d modules.' % len(pyc_files))


if __name__ == '__main__':
    main()
