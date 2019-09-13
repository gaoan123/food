 create database my_stock DEFAULT CHARACTER SET gbk COLLATE gbk_chinese_ci;
create database can_yin_shop DEFAULT CHARACTER SET gbk COLLATE gbk_chinese_ci;

 一般情况下，我们在数据库建库的时候会指定编码格式为utf8，如：

CREATE DATABASE `test` CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';

问题就出现在编码格式上，将其改为utf8mb4即可，如：

CREATE DATABASE can_yin_shop CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci';



create table shop_catagory
	(
	    id int unsigned not null  primary key auto_increment,
	    shop_name                 char(48) not null,
	    address_info               char(64) not null,
	    shop_url                  char(48) not null DEFAULT '',
	    distance_km               char(8) not null
  )

create table shop_info_huoguo
	(
	    id int unsigned not null  primary key auto_increment,
	    shop_name                 char(48) not null,
	    shop_id                   char(48) not null,
	    shop_mainRegionName       char(48) not null,
	    address_info               char(64) not null,
	    shop_url                  char(48) not null DEFAULT '',
	    shop_city                 char(48) not null DEFAULT '',
	    shop_district             char(48) not null DEFAULT '',
	    shop_catagory             char(48) not null DEFAULT '',
	    shop_subcatagory          char(48) not null DEFAULT '',
	    shop_star                 char(48) not null DEFAULT '',
        taste_score               char(48) not null DEFAULT '',
        environment_score         char(48) not null DEFAULT '',
        service_score             char(48) not null DEFAULT '',
        avgPrice                  char(48) not null DEFAULT '',
        recommend_foods           char(255) not null DEFAULT '',
	    distance_km               char(8) not null
  )

create table profession_url_table
	(
      id int unsigned not null  primary key auto_increment,
	    profession_name               char(16) not null,	
      profession_url      char(60) not null DEFAULT ''
  )
id int unsigned not null  primary key auto_increment,
  create table stock_related_urls_table
	(
	    stock_code                 char(16) not null,
	    company_name               char(32) not null,
	    stock_url                  char(60) not null DEFAULT '',
	    company_url                char(60) not null DEFAULT '',
	    detail_url                 char(60) not null DEFAULT '',
	    report_url                 char(60) not null DEFAULT ''
  )

  create table 银行_time_data_table
	(
	    stock_code                 char(16) not null,
	    trade_date                 char(16) not null,
	    trade_time                 char(16) not null,
	    price_color                 char(8) not null,
	    price                      char(8) not null,
	    quatity_color               char(8) not null,
	    trade_quatity               char(16) not null,
        arrow_color                char(8) not null
  )

  create table stock_history_info
	(
	    stock_code                 char(16) not null,
	    trade_date                 char(16) not null,
	    closing_price                 char(8) not null,
	    price_change                 char(8) not null,
	    main_net_inflow                char(16) not null,
	    main_net_occupation_ratio              char(8) not null,
	    super_large_inflow                char(16) not null,
	    super_large_net_occupation_ratio                char(16) not null,
        large_inflow                char(16) not null,
	    large_net_occupation_ratio                char(16) not null,
	    middle_inflow                char(16) not null,
	    middle_net_occupation_ratio                char(16) not null,
	    little_inflow                char(16) not null,
	    little_net_occupation_ratio   char(16) not null
  )

