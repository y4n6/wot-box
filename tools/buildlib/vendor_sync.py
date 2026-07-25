# -*- coding: utf-8 -*-
# 将第三方公开源码同步到集成构建目录。
# @author ytyang
import os
import shutil
import subprocess

from buildlib.config import (
    DISPERSION_RETICLE_REF,
    DISPERSION_RETICLE_REF_MARKER_PATH,
    DISPERSION_RETICLE_REPO_URL,
    DISPERSION_RETICLE_SOURCE_DIR,
    DISPERSION_RETICLE_SWF_SOURCE_PATH,
    DISPERSION_RETICLE_SWF_TARGET_PATH,
    DISPERSION_RETICLE_VENDOR_DIR,
    INTEGRATED_DIR,
    SRC_DIR,
)
from buildlib.fs_utils import copy_tree, ensure_parent, remove_tree, reset_dir


def run_command(command):
    """运行外部命令，并将失败转换为终止构建的错误。"""
    try:
        subprocess.check_call(command)
    except OSError:
        raise SystemExit('Required command is not available: %s' % command[0])
    except subprocess.CalledProcessError as error:
        raise SystemExit('Command failed with exit code %s: %s' % (error.returncode, ' '.join(command)))


def ensure_dispersion_reticle_vendor_repo():
    """确保缓存的 DispersionReticle 检出版本匹配配置的 tag。"""
    if os.path.isdir(DISPERSION_RETICLE_SOURCE_DIR) and _is_dispersion_reticle_ref_current():
        return
    ensure_parent(DISPERSION_RETICLE_VENDOR_DIR)
    if os.path.exists(DISPERSION_RETICLE_VENDOR_DIR):
        remove_tree(DISPERSION_RETICLE_VENDOR_DIR)
    run_command([
        'git', '-c', 'advice.detachedHead=false', 'clone', '--depth', '1', '--branch', DISPERSION_RETICLE_REF,
        DISPERSION_RETICLE_REPO_URL, DISPERSION_RETICLE_VENDOR_DIR
    ])
    _write_dispersion_reticle_ref_marker()


def _is_dispersion_reticle_ref_current():
    """检查用于固定第三方缓存上游 ref 的轻量标记。"""
    try:
        with open(DISPERSION_RETICLE_REF_MARKER_PATH, 'r') as marker_file:
            return marker_file.read().strip() == DISPERSION_RETICLE_REF
    except IOError:
        return False


def _write_dispersion_reticle_ref_marker():
    """记录当前第三方缓存使用的上游 ref。"""
    with open(DISPERSION_RETICLE_REF_MARKER_PATH, 'w') as marker_file:
        marker_file.write(DISPERSION_RETICLE_REF)


def sync_public_dispersion_reticle_sources():
    """用本地源码和 DispersionReticle 源码生成集成源码树。"""
    reset_dir(INTEGRATED_DIR)
    copy_tree(SRC_DIR, INTEGRATED_DIR)

    ensure_dispersion_reticle_vendor_repo()

    entry_source = os.path.join(DISPERSION_RETICLE_SOURCE_DIR, 'mod_DispersionReticle.py')
    entry_target = os.path.join(INTEGRATED_DIR, 'res', 'scripts', 'client', 'gui', 'mods', 'mod_DispersionReticle.py')
    ensure_parent(entry_target)
    shutil.copy2(entry_source, entry_target)

    package_source = os.path.join(DISPERSION_RETICLE_SOURCE_DIR, 'dispersionreticle')
    package_target = os.path.join(INTEGRATED_DIR, 'res', 'scripts', 'client', 'dispersionreticle')
    copy_tree(package_source, package_target)

    gui_source = os.path.join(DISPERSION_RETICLE_SOURCE_DIR, 'gui', 'dispersionreticle')
    gui_target = os.path.join(INTEGRATED_DIR, 'res', 'gui', 'dispersionreticle')
    copy_tree(gui_source, gui_target)

    if not os.path.exists(DISPERSION_RETICLE_SWF_SOURCE_PATH):
        raise SystemExit('Missing DispersionReticle SWF source: %s' % DISPERSION_RETICLE_SWF_SOURCE_PATH)
    ensure_parent(DISPERSION_RETICLE_SWF_TARGET_PATH)
    shutil.copy2(DISPERSION_RETICLE_SWF_SOURCE_PATH, DISPERSION_RETICLE_SWF_TARGET_PATH)