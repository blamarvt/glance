-- START images
ALTER TABLE "images" RENAME TO "images_backup";

CREATE TABLE "images" (
    id INTEGER NOT NULL, 
    name VARCHAR(255), 
    size INTEGER, 
    status VARCHAR(30) NOT NULL, 
    is_public BOOLEAN NOT NULL, 
    location TEXT, 
    created_at DATETIME NOT NULL, 
    updated_at DATETIME, 
    deleted_at DATETIME, 
    deleted BOOLEAN NOT NULL, 
    disk_format VARCHAR(20),
    container_format VARCHAR(20), checksum VARCHAR(32), owner VARCHAR(255), min_disk INTEGER, min_ram INTEGER,
    PRIMARY KEY (id), 
    CHECK (is_public IN (0, 1)), 
    CHECK (deleted IN (0, 1))
);

CREATE INDEX ix_images_deleted ON "images" (deleted);
CREATE INDEX ix_images_is_public ON "images" (is_public);

INSERT INTO "images" SELECT * FROM "images_backup";

DROP TABLE "images_backup";
-- END images


-- START image_members
ALTER TABLE "image_members" RENAME TO "image_members_backup";

CREATE TABLE image_members (
    id INTEGER NOT NULL, 
    image_id INTEGER NOT NULL, 
    member VARCHAR(255) NOT NULL, 
    can_share BOOLEAN NOT NULL, 
    created_at DATETIME NOT NULL, 
    updated_at DATETIME, 
    deleted_at DATETIME, 
    deleted BOOLEAN NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (image_id, member), 
    CHECK (deleted IN (0, 1)), 
    CHECK (can_share IN (0, 1)), 
    FOREIGN KEY(image_id) REFERENCES images (id)
);

CREATE INDEX ix_image_members_deleted ON image_members (deleted);
CREATE INDEX ix_image_members_image_id ON image_members (image_id);
CREATE INDEX ix_image_members_image_id_member ON image_members (image_id, member);

INSERT INTO "image_members" SELECT * FROM "image_members_backup";

DROP TABLE "image_members_backup";
-- END image_members


-- START image_properties
ALTER TABLE "image_properties" RENAME TO "image_properties_backup";

CREATE TABLE image_properties (
    id INTEGER NOT NULL, 
    image_id INTEGER NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    value TEXT, 
    created_at DATETIME NOT NULL, 
    updated_at DATETIME, 
    deleted_at DATETIME, 
    deleted BOOLEAN NOT NULL, 
    PRIMARY KEY (id), 
    CHECK (deleted IN (0, 1)), 
    UNIQUE (image_id, name), 
    FOREIGN KEY(image_id) REFERENCES images (id)
);

CREATE INDEX ix_image_properties_name ON image_properties (name);

INSERT INTO "image_properties" SELECT * FROM "image_properties_backup";

DROP TABLE "image_properties_backup";
-- END image_properties
