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


def upgrade_sqlite(migrate_engine):
    pass


def downgrade_sqlite(migrate_engine):
    pass


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    dialect_name = migrate_engine.url.get_dialect().name

    if dialect_name == "sqlite":
        return upgrade_sqlite(migrate_engine)

    fk1, fk2 = _get_foreign_keys(t_images, t_image_members, t_image_properties)

    fk1.drop()
    fk2.drop()

    t_images.c.id.alter(sqlalchemy.String(36), primary_key=True)
    t_image_members.c.image_id.alter(sqlalchemy.String(36))
    t_image_properties.c.image_id.alter(sqlalchemy.String(36))

    for image in migrate_engine.execute(t_images.select()):
        old_id = image["id"]
        new_id = glance.common.utils.generate_uuid()

        query = t_images.update().\
                    where(t_images.c.id==old_id).\
                    values(id=new_id)

        migrate_engine.execute(query)

        query = t_image_members.update().\
                    where(t_image_members.c.image_id==old_id).\
                    values(image_id=new_id)

        migrate_engine.execute(query)

        query = t_image_properties.update().\
                    where(t_image_properties.c.image_id==old_id).\
                    values(image_id=new_id)

        migrate_engine.execute(query)

    fk1.create()
    fk2.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    dialect_name = migrate_engine.url.get_dialect().name

    if dialect_name == "sqlite":
        return downgrade_sqlite(migrate_engine)

    t_images = sqlalchemy.Table('images', meta, autoload=True)
    t_image_members = sqlalchemy.Table('image_members', meta, autoload=True)
    t_image_properties = sqlalchemy.Table('image_properties',
                                          meta,
                                          autoload=True)

    fk1, fk2 = _get_foreign_keys(t_images, t_image_members, t_image_properties)

    fk1.drop()
    fk2.drop()

    t_images.c.id.alter(sqlalchemy.Integer(), primary_key=True)
    t_image_members.c.image_id.alter(sqlalchemy.Integer())
    t_image_properties.c.image_id.alter(sqlalchemy.Integer())

    for image in migrate_engine.execute(t_images.select()):
        old_id = image["id"]
        new_id = 0

        query = t_images.update().\
                    where(t_images.c.id==old_id).\
                    values(id=new_id)

        migrate_engine.execute(query)

        query = t_image_members.update().\
                    where(t_image_members.c.image_id==old_id).\
                    values(image_id=new_id)

        migrate_engine.execute(query)

        query = t_image_properties.update().\
                    where(t_image_properties.c.image_id==old_id).\
                    values(image_id=new_id)

        migrate_engine.execute(query)

        new_id += 1

    fk1.create()
    fk2.create()

