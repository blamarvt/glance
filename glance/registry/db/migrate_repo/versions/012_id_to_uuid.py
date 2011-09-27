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


meta = sqlalchemy.MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t_images = _get_table('images', meta)
    t_image_members = _get_table('image_members', meta)
    t_image_properties = _get_table('image_properties', meta)

    fk1, fk2 = _get_foreign_keys(t_images, t_image_members, t_image_properties)

    fk1.drop()
    fk2.drop()

    t_images.c.id.alter(sqlalchemy.String(36), primary_key=True)
    t_image_members.c.image_id.alter(sqlalchemy.String(36))
    t_image_properties.c.image_id.alter(sqlalchemy.String(36))

    _update_all_ids_to_uuids(t_images, t_image_members, t_image_properties)

    fk1.create()
    fk2.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    t_images = _get_table('images', meta)
    t_image_members = _get_table('image_members', meta)
    t_image_properties = _get_table('image_properties', meta)

    fk1, fk2 = _get_foreign_keys(t_images, t_image_members, t_image_properties)

    fk1.drop()
    fk2.drop()

    t_images.c.id.alter(sqlalchemy.Integer(), primary_key=True)
    t_image_members.c.image_id.alter(sqlalchemy.Integer())
    t_image_properties.c.image_id.alter(sqlalchemy.Integer())

    _update_all_uuids_to_ids(t_images, t_image_members, t_image_properties)

    fk1.create()
    fk2.create()


def _get_table(table_name, metadata):
    """Return a sqlalchemy Table definition with associated metadata."""
    return sqlalchemy.Table(table_name, metadata, autoload=True)


def _get_foreign_keys(t_images, t_image_members, t_image_properties):
    """Retrieve and return foreign keys for members/properties tables."""
    image_members_fk_name = t_image_members.foreign_keys[0].name
    image_properties_fk_name = t_image_properties.foreign_keys[0].name

    fk1 = migrate.ForeignKeyConstraint([t_image_members.c.image_id],
                                       [t_images.c.id],
                                       name=image_members_fk_name)

    fk2 = migrate.ForeignKeyConstraint([t_image_properties.c.image_id],
                                       [t_images.c.id],
                                       name=image_properties_fk_name)

    return fk1, fk2


def _update_all_ids_to_uuids(t_images, t_image_members, t_image_properties):
    """Transition from INTEGER id to VARCHAR(36) id."""
    for image in t_images.select().execute():
        old_id = image["id"]
        new_id = glance.common.utils.generate_uuid()

        t_images.update().\
            where(t_images.c.id==old_id).\
            values(id=new_id).execute()

        t_image_members.update().\
            where(t_image_members.c.image_id==old_id).\
            values(image_id=new_id).execute()

        t_image_properties.update().\
            where(t_image_properties.c.image_id==old_id).\
            values(image_id=new_id).execute()


def _update_all_uuids_to_ids(t_images, t_image_members, t_image_properties):
    """Transition from VARCHAR(36) id to INTEGER id."""
    for image in t_images.select().execute():
        old_id = image["id"]
        new_id = 0

        t_images.update().\
            where(t_images.c.id==old_id).\
            values(id=new_id).execute()

        t_image_members.update().\
            where(t_image_members.c.image_id==old_id).\
            values(image_id=new_id).execute()

        t_image_properties.update().\
            where(t_image_properties.c.image_id==old_id).\
            values(image_id=new_id).execute()

        new_id += 1
