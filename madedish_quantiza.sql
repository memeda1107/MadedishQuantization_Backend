/*
 Navicat Premium Data Transfer

 Source Server         : 本地数据库
 Source Server Type    : MySQL
 Source Server Version : 80011
 Source Host           : localhost:3306
 Source Schema         : madedish_quantiza

 Target Server Type    : MySQL
 Target Server Version : 80011
 File Encoding         : 65001

 Date: 29/04/2025 01:38:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for review_diary
-- ----------------------------
DROP TABLE IF EXISTS `review_diary`;
CREATE TABLE `review_diary`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `income` float(50, 0) NULL DEFAULT NULL COMMENT '今日收益',
  `market_trend` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '大盘走势',
  `market_increase` float NULL DEFAULT NULL COMMENT '大盘涨幅',
  `turnover` float NULL DEFAULT NULL COMMENT '成交量',
  `number_of_rising` int(11) NULL DEFAULT NULL COMMENT '上涨家数',
  `number_of_falling` int(11) NULL DEFAULT NULL COMMENT '下跌家数',
  `number_of_limit_up` int(11) NULL DEFAULT NULL COMMENT '涨停家数',
  `number_of_limit_down` int(11) NULL DEFAULT NULL COMMENT '跌停家数',
  `explosion_rate` float NULL DEFAULT NULL COMMENT '炸板率',
  `yesterday_limit_up` float NULL DEFAULT NULL COMMENT '昨日涨停',
  `yesterday_connecting_plate` float NULL DEFAULT NULL COMMENT '昨日连板',
  `short_term_funds` float NULL DEFAULT NULL COMMENT '短线资金',
  `overall_market_review` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '整体盘面回顾',
  `any_differences_sectors` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '板块是否有分歧',
  `expected_leaders` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '龙头预期',
  `today_best_solution` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '今日最优解',
  `mistakes_made_today` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '今日交易犯错',
  `record_date` date NULL DEFAULT NULL COMMENT '记录日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
