-- 创建数据库
CREATE DATABASE `github_trending`;
-- 查看全部数据库
SHOW DATABASES;
-- 选用数据库
USE `github_trending`;

-- 创建表格待录入
CREATE TABLE `projects`(
    `name` VARCHAR(255), 
    `starter` VARCHAR(255), 
    `programming_language` VARCHAR(255),
    `total_star` INT, 
    `total_fork` INT, 
    `monthly_star` INT,
    PRIMARY KEY(`name`,`starter`)
);

-- 表格查询/删除
DESCRIBE `PROJECTS`;
DROP TABLE `PROJECTS`;
SELECT * FROM `projects`;

-- 检查资料录入数量
SELECT COUNT(*) FROM `projects`;

-- 创建总star排序视窗
CREATE VIEW order_using_star AS 
SELECT 
	RANK() OVER (ORDER BY `total_star` DESC) AS `ranking`,
	`name`, 
    `starter`, 
    `programming_language`,
    `total_star`, 
    `total_fork`,
    `monthly_star`
FROM `projects`
ORDER BY `total_star` DESC
LIMIT 10;

-- 创建总fork排序视窗
CREATE VIEW order_using_fork AS 
SELECT
	RANK() OVER (ORDER BY `total_fork` DESC) AS `ranking`,
	`name`, 
    `starter`, 
    `programming_language`,
    `total_star`, 
    `total_fork`,
    `monthly_star`
FROM `projects`
ORDER BY `total_fork` DESC
LIMIT 10;

-- 使用视窗
SELECT * FROM order_using_star;
SELECT * FROM order_using_fork;
