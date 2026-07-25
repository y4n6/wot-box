# -*- coding: utf-8 -*-
import os
import py_compile
import shutil
import zipfile
import xml.etree.ElementTree as ElementTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, 'src')
BUILD_DIR = os.path.join(ROOT, '.build')
COMPILED_DIR = os.path.join(BUILD_DIR, 'compiled')
RELEASE_DIR = os.path.join(ROOT, 'release')
ORIGINAL_DIR = os.path.join(ROOT, 'original')
ATLAS_WOTMOD_PATH = os.path.join(ORIGINAL_DIR, 's0urce.box.combat.eff.atlas.wotmod')
META_XML_PATH = os.path.join(SRC_DIR, 'meta.xml')
META_XML_ARCNAME = 'meta.xml'
PACKAGE_ID = 's0urce.box.combat.eff.atlas'
PACKAGE_VERSION = '2.0.0'
RELEASE_NAME = 'battle_efficiency_standalone.wotmod'
STALE_RELEASE_NAMES = ('s0urce.box.combat.eff.atlas.wotmod', 's0urce.box.combat.eff.wotmod')

REQUIRED_BADGE_NAMES = tuple(['badge_%s' % index for index in range(10, 18)] + ['badge_%s' % index for index in range(20, 24)])
ATLAS_RESOURCE_GROUPS = (
    (
        'battle badges',
        (
            'res/gui/flash/atlases/battleAtlas.xml',
            'res/gui/flash/atlases/battleAtlas.dds',
        ),
    ),
    (
        'vehicle markers',
        (
            'res/gui/flash/atlases/vehicleMarkerAtlas.xml',
            'res/gui/flash/atlases/vehicleMarkerAtlas.dds',
        ),
    ),
)


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


def normalize_arcname(path):
    return path.replace('\\', '/')


def iter_compiled_files():
    for base, _dirs, files in os.walk(COMPILED_DIR):
        for name in files:
            path = os.path.join(base, name)
            arcname = normalize_arcname(os.path.relpath(path, COMPILED_DIR))
            yield path, arcname


def get_required_atlas_resources():
    resources = []
    for _group_name, group_resources in ATLAS_RESOURCE_GROUPS:
        resources.extend(group_resources)
    return tuple(resources)


def validate_atlas_resources():
    if not os.path.exists(ATLAS_WOTMOD_PATH):
        raise SystemExit('Missing atlas input: %s' % ATLAS_WOTMOD_PATH)

    with zipfile.ZipFile(ATLAS_WOTMOD_PATH, 'r') as zf:
        atlas_names = set([normalize_arcname(name) for name in zf.namelist()])
        missing_resources = [resource for resource in get_required_atlas_resources() if resource not in atlas_names]
        if missing_resources:
            raise SystemExit('Atlas input is missing required resources: %s' % ', '.join(missing_resources))

        battle_xml = zf.read('res/gui/flash/atlases/battleAtlas.xml')
        missing_badges = []
        for badge_name in REQUIRED_BADGE_NAMES:
            marker = '<name> %s </name>' % badge_name
            if marker not in battle_xml:
                missing_badges.append(badge_name)
        if missing_badges:
            raise SystemExit('battleAtlas.xml is missing required badge entries: %s' % ', '.join(missing_badges))


def write_zip_entry(zf, written_arcnames, source_path, arcname):
    if arcname in written_arcnames:
        raise SystemExit('Duplicate package entry: %s' % arcname)
    zf.write(source_path, arcname)
    written_arcnames.add(arcname)


def validate_meta_xml(xml_data):
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
    with zipfile.ZipFile(ATLAS_WOTMOD_PATH, 'r') as atlas_zip:
        atlas_infos = atlas_zip.infolist()
        atlas_names = [normalize_arcname(info.filename) for info in atlas_infos]
        atlas_files = [info for info in atlas_infos if not info.filename.endswith('/')]

        with zipfile.ZipFile(output_path, 'r') as release_zip:
            release_infos = release_zip.infolist()
            release_names = [normalize_arcname(info.filename) for info in release_infos]
            if release_names[:len(atlas_names)] != atlas_names:
                raise SystemExit('Release does not preserve the atlas package entry order.')

            metadata_attributes = ('date_time', 'compress_type', 'comment', 'extra', 'create_system', 'external_attr')
            for index, atlas_info in enumerate(atlas_infos):
                release_info = release_infos[index]
                for attribute in metadata_attributes:
                    if getattr(release_info, attribute) != getattr(atlas_info, attribute):
                        raise SystemExit('Release atlas entry metadata differs from original: %s (%s)' % (atlas_info.filename, attribute))

            for atlas_info in atlas_files:
                arcname = normalize_arcname(atlas_info.filename)
                release_info = release_zip.getinfo(arcname)
                if release_info.CRC != atlas_info.CRC or release_info.file_size != atlas_info.file_size:
                    raise SystemExit('Release atlas resource differs from original: %s' % arcname)
                if release_zip.read(arcname) != atlas_zip.read(atlas_info.filename):
                    raise SystemExit('Release atlas resource bytes differ from original: %s' % arcname)

            script_names = [name for name in release_names if name.endswith('.pyc')]
            if len(script_names) != compiled_count:
                raise SystemExit('Release script count mismatch: expected %s, got %s' % (compiled_count, len(script_names)))
            if release_names.count(META_XML_ARCNAME) != 1:
                raise SystemExit('Release must contain exactly one root meta.xml.')
            validate_meta_xml(release_zip.read(META_XML_ARCNAME))

    return len(atlas_names), len(atlas_files)


def package_wotmod():
    if not os.path.exists(RELEASE_DIR):
        os.makedirs(RELEASE_DIR)
    output_path = os.path.join(RELEASE_DIR, RELEASE_NAME)
    if os.path.exists(output_path):
        os.remove(output_path)
    for stale_release_name in STALE_RELEASE_NAMES:
        stale_output_path = os.path.join(RELEASE_DIR, stale_release_name)
        if os.path.exists(stale_output_path):
            os.remove(stale_output_path)
    validate_atlas_resources()
    if not os.path.exists(META_XML_PATH):
        raise SystemExit('Missing package metadata: %s' % META_XML_PATH)
    with open(META_XML_PATH, 'rb') as meta_file:
        meta_xml = meta_file.read()
    validate_meta_xml(meta_xml)
    shutil.copyfile(ATLAS_WOTMOD_PATH, output_path)
    with zipfile.ZipFile(output_path, 'a', zipfile.ZIP_STORED) as zf:
        written_arcnames = set([normalize_arcname(name) for name in zf.namelist()])
        for path, arcname in iter_compiled_files():
            write_zip_entry(zf, written_arcnames, path, arcname)
        if META_XML_ARCNAME in written_arcnames:
            raise SystemExit('Duplicate package entry: %s' % META_XML_ARCNAME)
        zf.writestr(META_XML_ARCNAME, meta_xml)
    return output_path


def main():
    if not os.path.exists(SRC_DIR):
        raise SystemExit('Missing source directory: %s' % SRC_DIR)
    compiled_count = compile_sources()
    output_path = package_wotmod()
    atlas_entry_count, atlas_file_count = validate_release(output_path, compiled_count)
    print('Compiled modules:', compiled_count)
    print('Preserved atlas entries:', atlas_entry_count)
    print('Preserved atlas files:', atlas_file_count)
    print('Package id:', PACKAGE_ID)
    print('Package version:', PACKAGE_VERSION)
    print('Release output:', output_path)


if __name__ == '__main__':
    main()
