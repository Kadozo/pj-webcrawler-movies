from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `watchablegenre` ADD `watchable_id` INT NOT NULL;
        ALTER TABLE `watchablegenre` ADD `genre_id` INT NOT NULL;
        ALTER TABLE `watchablegenre` ADD CONSTRAINT `fk_watchabl_watchabl_f7fde563` FOREIGN KEY (`watchable_id`) REFERENCES `watchable` (`id`) ON DELETE CASCADE;
        ALTER TABLE `watchablegenre` ADD CONSTRAINT `fk_watchabl_genre_48c64ba0` FOREIGN KEY (`genre_id`) REFERENCES `genre` (`id`) ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `watchablegenre` DROP FOREIGN KEY `fk_watchabl_genre_48c64ba0`;
        ALTER TABLE `watchablegenre` DROP FOREIGN KEY `fk_watchabl_watchabl_f7fde563`;
        ALTER TABLE `watchablegenre` DROP COLUMN `watchable_id`;
        ALTER TABLE `watchablegenre` DROP COLUMN `genre_id`;"""
