# -*- coding: utf-8 -*-
# 生成独立 WoT 模组包的构建入口。
# @author ytyang
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from buildlib.compiler import compile_sources
from buildlib.config import DISPERSION_RETICLE_REF, PACKAGE_ID, PACKAGE_VERSION, SRC_DIR
from buildlib.packager import package_wotmod, validate_release
from buildlib.vendor_sync import sync_public_dispersion_reticle_sources


def print_build_info(label, value):
    # Python 2.7 下直接打印 Unicode 元组会显示转义文本，这里按终端编码输出文本行。
    encoding = sys.stdout.encoding or 'utf-8'
    line = u'%s %s\n' % (label, unicode(value))
    sys.stdout.write(line.encode(encoding, 'replace'))


def main():
    # 保持本文件只做流程编排，具体实现放在 buildlib 中。
    if not os.path.exists(SRC_DIR):
        raise SystemExit('Missing source directory: %s' % SRC_DIR)

    sync_public_dispersion_reticle_sources()
    compiled_count = compile_sources()
    output_path = package_wotmod()
    atlas_entry_count, atlas_file_count = validate_release(output_path, compiled_count)
    print_build_info(u'编译模块数:', compiled_count)
    print_build_info(u'保留 atlas 条目数:', atlas_entry_count)
    print_build_info(u'保留 atlas 文件数:', atlas_file_count)
    print_build_info(u'集成公开落弹环版本:', DISPERSION_RETICLE_REF)
    print_build_info(u'包标识:', PACKAGE_ID)
    print_build_info(u'包版本:', PACKAGE_VERSION)
    print_build_info(u'输出文件:', output_path)


if __name__ == '__main__':
    main()
