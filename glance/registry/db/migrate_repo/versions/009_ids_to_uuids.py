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

import sqlalchemy


def upgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    t_images = sqlalchemy.Table('images', meta, autoload=True)

    t_image_members = sqlalchemy.Table('image_members', meta, autoload=True)
    t_image_members.c.id.alter('uuid', sqlalchemy.String(36))

    t_image_properties = sqlalchemy.Table('image_properties', meta, autoload=True)
    t_image_properties.c.id.alter('uuid', sqlalchemy.String(36))

#    ForeignKeyConstraint([t_images.c.id],
 #                        [t_image_properties.c.image_id]).drop()

#    t_images.c.id.alter(name='uuid', type=String(36))

#    t_image_properties.c.image_id.alter('image_uuid',
#                                        String(36),
#                                        ForeignKey('images.uuid'))
#
#    t_image_members.c.image_id.alter('image_uuid',
#                                     String(36),
#                                     ForeignKey('images.uuid'))
#

def downgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    t_image_members = sqlalchemy.Table('image_members', meta, autoload=True)
    t_image_members.c.uuid.alter('id', sqlalchemy.Integer)

    t_image_properties = sqlalchemy.Table('image_properties', meta, autoload=True)
    t_image_properties.c.uuid.alter('id', sqlalchemy.Integer)
