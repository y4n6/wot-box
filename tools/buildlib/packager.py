# -*- coding: utf-8 -*-
# 将已编译脚本和静态资源打包为最终 .wotmod 文件。
# @author ytyang
import os
import zipfile
import xml.etree.ElementTree as ElementTree

from buildlib.compiler import iter_compiled_files, iter_static_package_files
from buildlib.config import (
    ATLAS_ENTRIES,
    ATLAS_RESOURCE_GROUPS,
    ATLAS_SRC_DIR,
    META_XML_ARCNAME,
    META_XML_PATH,
    PACKAGE_ID,
    PACKAGE_VERSION,
    RELEASE_DIR,
    RELEASE_NAME,
    REQUIRED_BADGE_NAMES,
)
from buildlib.fs_utils import normalize_arcname


def get_required_atlas_resources():
    """将 atlas 资源组展开为必需资源列表。"""
    resources = []
    for _group_name, group_resources in ATLAS_RESOURCE_GROUPS:
        resources.extend(group_resources)
    return tuple(resources)


def get_atlas_source_path(arcname):
    """将 atlas 包内路径解析为源码文件路径。"""
    return os.path.join(ATLAS_SRC_DIR, arcname.replace('/', os.sep))


def validate_atlas_resources():
    """打包前校验徽章 atlas 文件和必需徽章条目。"""
    missing_resources = [resource for resource in get_required_atlas_resources() if not os.path.exists(get_atlas_source_path(resource))]
    if missing_resources:
        raise SystemExit('Atlas source is missing required resources: %s' % ', '.join(missing_resources))

    with open(get_atlas_source_path('res/gui/flash/atlases/battleAtlas.xml'), 'rb') as battle_xml_file:
        battle_xml = battle_xml_file.read()
    missing_badges = []
    for badge_name in REQUIRED_BADGE_NAMES:
        marker = '<name> %s </name>' % badge_name
        if marker not in battle_xml:
            missing_badges.append(badge_name)
    if missing_badges:
        raise SystemExit('battleAtlas.xml is missing required badge entries: %s' % ', '.join(missing_badges))


def write_stored_entry(zf, written_arcnames, arcname, data, date_time, external_attr):
    """写入带固定元数据的未压缩 ZIP 条目，并检测重复路径。"""
    if arcname in written_arcnames:
        raise SystemExit('Duplicate package entry: %s' % arcname)
    info = zipfile.ZipInfo(arcname, date_time)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 0
    info.external_attr = external_attr
    zf.writestr(info, data)
    written_arcnames.add(arcname)


def write_atlas_entries(zf, written_arcnames):
    """优先写入 atlas 条目，保持 release 元数据稳定。"""
    for arcname, source_arcname, date_time, external_attr in ATLAS_ENTRIES:
        if source_arcname is None:
            write_stored_entry(zf, written_arcnames, arcname, '', date_time, external_attr)
            continue
        source_path = get_atlas_source_path(source_arcname)
        with open(source_path, 'rb') as source_file:
            write_stored_entry(zf, written_arcnames, arcname, source_file.read(), date_time, external_attr)


def write_zip_entry(zf, written_arcnames, source_path, arcname):
    """将普通文件写入包内，并防止重复路径。"""
    if arcname in written_arcnames:
        raise SystemExit('Duplicate package entry: %s' % arcname)
    zf.write(source_path, arcname)
    written_arcnames.add(arcname)


def validate_meta_xml(xml_data):
    """校验 meta.xml 中的包标识和版本。"""
    try:
        root = ElementTree.fromstring(xml_data)
    except ElementTree.ParseError as error:
        raise SystemExit('Invalid meta.xml: %s' % error)

    if root.tag != 'root':
        raise SystemExit('meta.xml root element must be <root>.')
    package_id = root.findtext('id')
    package_version = root.findtext('version')
    if package_id != PACKAGE_ID:
        raise SystemExit('meta.xml package id mismatch: expected %s, got %s' % (PACKAGE_ID, package_id))
    if package_version != PACKAGE_VERSION:
        raise SystemExit('meta.xml package version mismatch: expected %s, got %s' % (PACKAGE_VERSION, package_version))


def validate_release(output_path, compiled_count):
    """检查产物包的条目顺序、资源、脚本数量和元数据。"""
    atlas_names = [entry[0] for entry in ATLAS_ENTRIES]
    atlas_files = [entry for entry in ATLAS_ENTRIES if entry[1] is not None]

    with zipfile.ZipFile(output_path, 'r') as release_zip:
        release_infos = release_zip.infolist()
        release_names = [normalize_arcname(info.filename) for info in release_infos]
        if release_names[:len(atlas_names)] != atlas_names:
            raise SystemExit('Release does not preserve the atlas package entry order.')

        for index, (arcname, _source_arcname, date_time, external_attr) in enumerate(ATLAS_ENTRIES):
            release_info = release_infos[index]
            if normalize_arcname(release_info.filename) != arcname:
                raise SystemExit('Release atlas entry order differs from expected: %s' % arcname)
            if release_info.date_time != date_time or release_info.compress_type != zipfile.ZIP_STORED or release_info.create_system != 0 or release_info.external_attr != external_attr:
                raise SystemExit('Release atlas entry metadata differs from expected: %s' % arcname)

        for arcname, source_arcname, _date_time, _external_attr in atlas_files:
            with open(get_atlas_source_path(source_arcname), 'rb') as source_file:
                source_data = source_file.read()
            release_info = release_zip.getinfo(arcname)
            if release_info.file_size != len(source_data) or release_zip.read(arcname) != source_data:
                raise SystemExit('Release atlas resource differs from source: %s' % arcname)

        script_names = [name for name in release_names if name.endswith('.pyc')]
        if len(script_names) != compiled_count:
            raise SystemExit('Release script count mismatch: expected %s, got %s' % (compiled_count, len(script_names)))
        if release_names.count(META_XML_ARCNAME) != 1:
            raise SystemExit('Release must contain exactly one root meta.xml.')
        validate_meta_xml(release_zip.read(META_XML_ARCNAME))

    return len(atlas_names), len(atlas_files)


def package_wotmod():
    """根据已编译模块和静态资源创建最终 .wotmod 包。"""
    if not os.path.exists(RELEASE_DIR):
        os.makedirs(RELEASE_DIR)
    output_path = os.path.join(RELEASE_DIR, RELEASE_NAME)
    if os.path.exists(output_path):
        os.remove(output_path)
    validate_atlas_resources()
    if not os.path.exists(META_XML_PATH):
        raise SystemExit('Missing package metadata: %s' % META_XML_PATH)
    with open(META_XML_PATH, 'rb') as meta_file:
        meta_xml = meta_file.read()
    validate_meta_xml(meta_xml)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_STORED) as zf:
        written_arcnames = set()
        write_atlas_entries(zf, written_arcnames)
        for path, arcname in iter_compiled_files():
            write_zip_entry(zf, written_arcnames, path, arcname)
        for path, arcname in iter_static_package_files():
            write_zip_entry(zf, written_arcnames, path, arcname)
        if META_XML_ARCNAME in written_arcnames:
            raise SystemExit('Duplicate package entry: %s' % META_XML_ARCNAME)
        zf.writestr(META_XML_ARCNAME, meta_xml)
    return output_path