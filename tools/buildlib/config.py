# -*- coding: utf-8 -*-
# 集中维护路径、包元数据、第三方引用和 atlas 校验相关构建常量。
# @author ytyang
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_DIR = os.path.join(ROOT, 'src')
BUILD_DIR = os.path.join(ROOT, '.build')
COMPILED_DIR = os.path.join(BUILD_DIR, 'compiled')
INTEGRATED_DIR = os.path.join(BUILD_DIR, 'integrated_src')
RELEASE_DIR = os.path.join(ROOT, 'release')
ATLAS_SRC_DIR = os.path.join(SRC_DIR, 'atlas')
META_XML_PATH = os.path.join(SRC_DIR, 'meta.xml')
META_XML_ARCNAME = 'meta.xml'

PACKAGE_ID = 'battle.efficiency.standalone'
PACKAGE_VERSION = '2.1.0'
RELEASE_NAME = 'battle_efficiency_standalone.wotmod'

DISPERSION_RETICLE_REF = 'v3.1.3'
DISPERSION_RETICLE_REPO_URL = 'https://github.com/Pruszko/DispersionReticle.git'
DISPERSION_RETICLE_VENDOR_DIR = os.path.join(BUILD_DIR, 'vendor', 'DispersionReticle')
DISPERSION_RETICLE_SOURCE_DIR = os.path.join(DISPERSION_RETICLE_VENDOR_DIR, 'src')
DISPERSION_RETICLE_REF_MARKER_PATH = os.path.join(DISPERSION_RETICLE_VENDOR_DIR, '.wot-box-ref')
DISPERSION_RETICLE_SWF_SOURCE_PATH = os.path.join(SRC_DIR, 'res', 'gui', 'flash', 'DispersionReticleFlash.swf')
DISPERSION_RETICLE_SWF_TARGET_PATH = os.path.join(INTEGRATED_DIR, 'res', 'gui', 'flash', 'DispersionReticleFlash.swf')

ATLAS_ENTRIES = (
    ('res/', None, (2020, 11, 27, 12, 51, 18), 16),
    ('res/gui/', None, (2020, 11, 27, 12, 51, 18), 16),
    ('res/gui/flash/', None, (2020, 11, 27, 12, 51, 18), 16),
    ('res/gui/flash/atlases/', None, (2020, 11, 27, 12, 51, 18), 16),
    ('res/gui/flash/atlases/battleAtlas.dds', 'res/gui/flash/atlases/battleAtlas.dds', (2026, 1, 14, 10, 50, 56), 32),
    ('res/gui/flash/atlases/battleAtlas.xml', 'res/gui/flash/atlases/battleAtlas.xml', (2026, 1, 14, 10, 50, 56), 32),
)

REQUIRED_BADGE_NAMES = tuple(['badge_%s' % index for index in range(10, 18)] + ['badge_%s' % index for index in range(20, 24)])
ATLAS_RESOURCE_GROUPS = (
    (
        'battle badges',
        (
            'res/gui/flash/atlases/battleAtlas.xml',
            'res/gui/flash/atlases/battleAtlas.dds',
        ),
    ),
)