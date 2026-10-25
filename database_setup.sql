
CREATE DATABASE IF NOT EXISTS deadline_tracker
CHARACTER SET utf8
COLLATE utf8_unicode_ci;

USE deadline_tracker;

CREATE TABLE IF NOT EXISTS tasks (
    id INT NOT NULL AUTO_INCREMENT,
    task_name VARCHAR(150) NOT NULL,
    description VARCHAR(255) NULL,
    deadline DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB;
