-- CreateTable
CREATE TABLE `archive_artist` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `slug` VARCHAR(50) NOT NULL,
    `name` VARCHAR(100) NOT NULL,

    UNIQUE INDEX `slug`(`slug`),
    UNIQUE INDEX `name`(`name`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `archive_audiofile` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `slug` VARCHAR(50) NOT NULL,
    `session_subsection` VARCHAR(50) NOT NULL,
    `data` VARCHAR(100) NOT NULL,
    `name` VARCHAR(200) NOT NULL,
    `artist_id` INTEGER NULL,
    `session_id` INTEGER NOT NULL,

    UNIQUE INDEX `slug`(`slug`),
    INDEX `archive_audiofile_artist_id_4770b25c_fk_archive_artist_id`(`artist_id`),
    INDEX `archive_audiofile_session_id_ed86f222_fk_archive_session_id`(`session_id`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `archive_challenge` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `slug` VARCHAR(50) NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    `blurb` LONGTEXT NOT NULL,
    `description` LONGTEXT NOT NULL,
    `copyright_issues` BOOLEAN NOT NULL,

    UNIQUE INDEX `slug`(`slug`),
    UNIQUE INDEX `name`(`name`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `archive_session` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `slug` VARCHAR(50) NOT NULL,
    `date` DATE NOT NULL,
    `challenge_id` INTEGER NOT NULL,

    UNIQUE INDEX `slug`(`slug`),
    INDEX `archive_session_challenge_id_d984eaa0_fk_archive_challenge_id`(`challenge_id`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `uploadform_uploadformvars` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `uploads_open` BOOLEAN NOT NULL,
    `upload_password` VARCHAR(20) NOT NULL,
    `session_info` LONGTEXT NOT NULL,
    `session_id` INTEGER NULL,
    `session_subsection` VARCHAR(50) NOT NULL,

    INDEX `uploadform_uploadfor_session_id_b3a1c179_fk_archive_s`(`session_id`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `archive_audiofile` ADD CONSTRAINT `archive_audiofile_artist_id_4770b25c_fk_archive_artist_id` FOREIGN KEY (`artist_id`) REFERENCES `archive_artist`(`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE `archive_audiofile` ADD CONSTRAINT `archive_audiofile_session_id_ed86f222_fk_archive_session_id` FOREIGN KEY (`session_id`) REFERENCES `archive_session`(`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE `archive_session` ADD CONSTRAINT `archive_session_challenge_id_d984eaa0_fk_archive_challenge_id` FOREIGN KEY (`challenge_id`) REFERENCES `archive_challenge`(`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE `uploadform_uploadformvars` ADD CONSTRAINT `uploadform_uploadfor_session_id_b3a1c179_fk_archive_s` FOREIGN KEY (`session_id`) REFERENCES `archive_session`(`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

