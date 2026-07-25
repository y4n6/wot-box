# -*- coding: utf-8 -*-
# 编译集成后的 Python 源码，并枚举进入包内的文件。
# @author ytyang
import os
import py_compile

from buildlib.config import ATLAS_ENTRIES, COMPILED_DIR, INTEGRATED_DIR
from buildlib.fs_utils import ensure_parent, normalize_arcname, reset_dir


def compile_sources():
    """将集成源码树中的每个 Python 源文件编译为对应的 .pyc。"""
    reset_dir(COMPILED_DIR)
    compiled_count = 0
    for base, _dirs, files in os.walk(INTEGRATED_DIR):
        for name in files:
            if not name.endswith('.py'):
                continue
            source_path = os.path.join(base, name)
            relative = os.path.relpath(source_path, INTEGRATED_DIR)
            target_path = os.path.join(COMPILED_DIR, os.path.splitext(relative)[0] + '.pyc')
            ensure_parent(target_path)
            py_compile.compile(source_path, cfile=target_path, doraise=True)
            compiled_count += 1
    return compiled_count


def iter_compiled_files():
    """按本地路径和包内路径成对枚举已编译的 Python 模块。"""
    for base, _dirs, files in os.walk(COMPILED_DIR):
        for name in files:
            path = os.path.join(base, name)
            arcname = normalize_arcname(os.path.relpath(path, COMPILED_DIR))
            yield path, arcname


def iter_static_package_files():
    """从集成源码树中枚举非 Python 包资源。"""
    ignored_paths = set(entry[0] for entry in ATLAS_ENTRIES if entry[1] is not None)
    for base, _dirs, files in os.walk(INTEGRATED_DIR):
        for name in files:
            if name.endswith('.py'):
                continue
            path = os.path.join(base, name)
            arcname = normalize_arcname(os.path.relpath(path, INTEGRATED_DIR))
            if not arcname.startswith('res/'):
                continue
            if arcname in ignored_paths:
                continue
            yield path, arcname