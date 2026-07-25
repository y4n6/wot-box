# -*- coding: utf-8 -*-
import os
import py_compile
import shutil
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, 'src')
BUILD_DIR = os.path.join(ROOT, 'build')
COMPILED_DIR = os.path.join(BUILD_DIR, 'compiled')
RELEASE_DIR = os.path.join(ROOT, 'release')
RELEASE_NAME = 's0urce.box.combat.eff.wotmod'


def reset_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def ensure_parent(path):
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent)


def compile_sources():
    reset_dir(COMPILED_DIR)
    compiled_count = 0
    for base, _dirs, files in os.walk(SRC_DIR):
        for name in files:
            if not name.endswith('.py'):
                continue
            source_path = os.path.join(base, name)
            relative = os.path.relpath(source_path, SRC_DIR)
            target_path = os.path.join(COMPILED_DIR, os.path.splitext(relative)[0] + '.pyc')
            ensure_parent(target_path)
            py_compile.compile(source_path, cfile=target_path, doraise=True)
            compiled_count += 1
    return compiled_count


def package_wotmod():
    if not os.path.exists(RELEASE_DIR):
        os.makedirs(RELEASE_DIR)
    output_path = os.path.join(RELEASE_DIR, RELEASE_NAME)
    if os.path.exists(output_path):
        os.remove(output_path)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_STORED) as zf:
        for base, _dirs, files in os.walk(COMPILED_DIR):
            for name in files:
                path = os.path.join(base, name)
                arcname = os.path.relpath(path, COMPILED_DIR)
                zf.write(path, arcname)
    return output_path


def main():
    if not os.path.exists(SRC_DIR):
        raise SystemExit('Missing source directory: %s' % SRC_DIR)
    compiled_count = compile_sources()
    output_path = package_wotmod()
    print('Compiled modules:', compiled_count)
    print('Release output:', output_path)


if __name__ == '__main__':
    main()
