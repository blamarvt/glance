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


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    t_images = _get_table('images', meta)

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


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    t_images = _get_table('images', meta)

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
