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

from migrate.changeset import *
from sqlalchemy import *
from sqlalchemy.sql import and_, not_

from glance.registry.db.migrate_repo.schema import (
    Boolean, DateTime, Integer, String, Text, from_migration_import)
import glance.common.utils as utils


meta = MetaData()
new_id = Column('id', String(40), primary_key=True)
new_members_id = Column('new_images_id', String(40))
new_properties_id = Column('new_images_id', String(40))

def get_images_table(meta):
    return Table('images', meta, autoload=True, useexisting=True)


def get_image_properties_table(meta):
    return Table('image_properties', meta, autoload=True, useexisting=True)


def get_image_members_table(meta):
    return Table('image_members', meta, autoload=True, useexisting=True)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    conn = migrate_engine.connect()

    images = get_images_table(meta)
    image_properties = get_image_properties_table(meta)
    image_members = get_image_members_table(meta)

    images.create_column(new_id, primary_key=True)
    #image_properties.create_column(new_properties_id)
    #image_members.create_column(new_members_id)

    #raise Exception("TEST")


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    #images = get_images_table(meta)
    #image_properties = get_image_properties_table(meta)
    #image_members = get_image_members_table(meta)

    #images.drop_column(new_id)
    #image_properties.drop_column(new_properties_id)
    #image_members.drop_column(new_members_id)
