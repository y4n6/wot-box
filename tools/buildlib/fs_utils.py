# -*- coding: utf-8 -*-
# Python 2.7 构建脚本共享的文件系统辅助函数。
# @author ytyang
import os
import shutil
import stat


def reset_dir(path):
    """从零重建目录。"""
    if os.path.exists(path):
        remove_tree(path)
    os.makedirs(path)


def remove_tree(path):
    """删除目录树，并处理 Windows 下 Git 留下的只读文件。"""
    def on_error(func, failed_path, _exc_info):
        os.chmod(failed_path, stat.S_IWRITE)
        func(failed_path)

    shutil.rmtree(path, onerror=on_error)


def ensure_parent(path):
    """确保文件路径的父目录存在。"""
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent)


def copy_tree(source_dir, target_dir):
    """复制目录树，不要求目标根目录预先不存在。"""
    for base, dirs, files in os.walk(source_dir):
        relative = os.path.relpath(base, source_dir)
        current_target = target_dir if relative == '.' else os.path.join(target_dir, relative)
        if not os.path.exists(current_target):
            os.makedirs(current_target)
        for dir_name in dirs:
            child_dir = os.path.join(current_target, dir_name)
            if not os.path.exists(child_dir):
                os.makedirs(child_dir)
        for file_name in files:
            source_path = os.path.join(base, file_name)
            target_path = os.path.join(current_target, file_name)
            ensure_parent(target_path)
            shutil.copy2(source_path, target_path)


def normalize_arcname(path):
    """将本地路径规范化为 ZIP 包内路径。"""
    return path.replace('\\', '/')