CREATE DATABASE IF NOT EXISTS officer DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

CREATE TABLE `corrupt` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `level` tinyint(4) DEFAULT 1 COMMENT '0中管干部1省管干部',
  `type` tinyint(4) DEFAULT 1 COMMENT '0执纪审查1党纪处分',
  `time`  timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `title` VARCHAR(256) DEFAULT NULL ,
  `content` text DEFAULT NULL ,
  `resourceUrl` VARCHAR(100) DEFAULT NULL ,
  `resource` VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=UTF8;
