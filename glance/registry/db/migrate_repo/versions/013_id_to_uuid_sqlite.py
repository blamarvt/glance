# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import migrate
import sqlalchemy

import glance.common.utils
from glance.registry.db.migrate_repo import schema


meta = sqlalchemy.MetaData()


_import_methods = ["_update_all_ids_to_uuids", "_update_all_uuids_to_ids"]
_update_all_ids_to_uuids, _update_all_uuids_to_ids = \
    schema.from_migration_import("012_id_to_uuid", _import_methods)


def upgrade(migrate_engine):
    if migrate_engine.url.get_dialect().name == "sqlite":
        return upgrade_sqlite(migrate_engine)


def downgrade(migrate_engine):
    if migrate_engine.url.get_dialect().name == "sqlite":
        return downgrade_sqlite(migrate_engine)


def upgrade_sqlite(migrate_engine):
    meta.bind = migrate_engine

    t_images = _get_table('images', meta)
    t_image_members = _get_table('image_members', meta)
    t_image_properties = _get_table('image_properties', meta)

    _update_all_ids_to_uuids(t_images, t_image_members, t_image_properties)


def downgrade_sqlite(migrate_engine):
    meta.bind = migrate_engine

    t_images = _get_table('images', meta)
    t_image_members = _get_table('image_members', meta)
    t_image_properties = _get_table('image_properties', meta)

    _update_all_uuids_to_ids(t_images, t_image_members, t_image_properties)


def _get_table(table_name, metadata):
    """Return a sqlalchemy Table definition with associated metadata."""
    return sqlalchemy.Table(table_name, metadata, autoload=True)
