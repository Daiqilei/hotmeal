CREATE TABLE category (
	category_id INTEGER NOT NULL COMMENT '分类主键 ID' AUTO_INCREMENT, 
	name VARCHAR(50) NOT NULL COMMENT '分类名称', 
	description TEXT COMMENT '分类描述', 
	img_url VARCHAR(255) COMMENT '分类图片 URL', 
	deleted_at DATETIME COMMENT '删除时间（软删除）', 
	created_at DATETIME NOT NULL COMMENT '创建时间' DEFAULT now(), 
	updated_at DATETIME NOT NULL COMMENT '最后更新时间' DEFAULT now(), 
	parent_category_id INTEGER COMMENT '父分类 ID（构建分类树）', 
	PRIMARY KEY (category_id), 
	UNIQUE (name), 
	CONSTRAINT fk_category_parent_id FOREIGN KEY(parent_category_id) REFERENCES category (category_id)
);


CREATE TABLE user (
	user_id INTEGER NOT NULL AUTO_INCREMENT, 
	account VARCHAR(255) NOT NULL COMMENT '登录账号', 
	password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希 (Werkzeug)', 
	phone_number VARCHAR(20) COMMENT '手机号', 
	username VARCHAR(50) COMMENT '昵称/显示名称', 
	avatar_url VARCHAR(255) COMMENT '用户头像URL', 
	email VARCHAR(120) COMMENT '邮箱', 
	`role` ENUM('ADMIN','STAFF','USER') NOT NULL COMMENT '用户角色' DEFAULT 'USER', 
	status ENUM('ACTIVE','BANNED','DELETED') NOT NULL COMMENT '用户状态' DEFAULT 'ACTIVE', 
	favorite_cuisine VARCHAR(50) COMMENT '用户偏好的菜系', 
	created_at DATETIME NOT NULL COMMENT '创建时间' DEFAULT now(), 
	updated_at DATETIME NOT NULL COMMENT '最后更新时间' DEFAULT now(), 
	deleted_at DATETIME COMMENT '删除时间（软删除）', 
	PRIMARY KEY (user_id), 
	UNIQUE (account), 
	UNIQUE (phone_number), 
	UNIQUE (email)
);


CREATE TABLE dining_area (
	area_id INTEGER NOT NULL COMMENT '区域ID' AUTO_INCREMENT, 
	area_name VARCHAR(50) NOT NULL COMMENT '区域名称', 
	state ENUM('FREE','OCCUPIED') NOT NULL COMMENT '区域状态：FREE空闲/OCCUPIED占用', 
	max_capacity INTEGER COMMENT '区域最大容纳人数', 
	usage_count INTEGER NOT NULL COMMENT '区域使用次数', 
	assigned_user_id INTEGER COMMENT '当前占用用户ID', 
	area_type ENUM('PRIVATE','TABLE','BAR') NOT NULL COMMENT '区域类型', 
	created_at DATETIME NOT NULL COMMENT '创建时间' DEFAULT now(), 
	last_used DATETIME COMMENT '上一次使用时间', 
	updated_at DATETIME NOT NULL COMMENT '最后更新时间' DEFAULT now(), 
	PRIMARY KEY (area_id), 
	UNIQUE (area_name), 
	CONSTRAINT fk_dining_area_user_id FOREIGN KEY(assigned_user_id) REFERENCES user (user_id)
);


CREATE TABLE dish (
	dish_id INTEGER NOT NULL COMMENT '菜品主键 ID' AUTO_INCREMENT, 
	name VARCHAR(50) NOT NULL COMMENT '菜品名称', 
	price NUMERIC(10, 2) NOT NULL COMMENT '菜品价格', 
	stock INTEGER NOT NULL COMMENT '库存数量', 
	image_url VARCHAR(255) COMMENT '菜品图片链接', 
	sales INTEGER NOT NULL COMMENT '已售数量', 
	rating NUMERIC(3, 2) NOT NULL COMMENT '菜品评分 (0.00-5.00)', 
	description VARCHAR(255) COMMENT '菜品描述', 
	category_id INTEGER COMMENT '所属分类ID', 
	created_at DATETIME NOT NULL COMMENT '创建时间' DEFAULT now(), 
	updated_at DATETIME NOT NULL COMMENT '最后更新时间' DEFAULT now(), 
	is_available BOOL NOT NULL COMMENT '是否上架', 
	deleted_at DATETIME COMMENT '删除时间（软删除）', 
	PRIMARY KEY (dish_id), 
	UNIQUE (name), 
	CONSTRAINT fk_dish_category_id FOREIGN KEY(category_id) REFERENCES category (category_id) ON DELETE SET NULL
);


CREATE TABLE menu_chat (
	chat_id INTEGER NOT NULL COMMENT '聊天记录ID' AUTO_INCREMENT, 
	user_id INTEGER NOT NULL COMMENT '所属用户ID', 
	question VARCHAR(255) COMMENT '用户提出的问题或内容', 
	answer TEXT COMMENT 'AI或人工回答的内容', 
	status ENUM('PENDING','PROCESSING','ANSWERED','FAILED') NOT NULL COMMENT '聊天状态', 
	created_at DATETIME NOT NULL COMMENT '创建时间' DEFAULT now(), 
	updated_at DATETIME NOT NULL COMMENT '最后更新时间' DEFAULT now(), 
	response_time FLOAT COMMENT 'AI响应时间（秒）', 
	confidence FLOAT COMMENT 'AI回答置信度', 
	source VARCHAR(50) COMMENT '回答来源：AI/人工', 
	tags VARCHAR(255) COMMENT '标签（逗号分隔）', 
	message_type ENUM('TEXT','VOICE','IMAGE') NOT NULL COMMENT '消息类型', 
	response_duration FLOAT COMMENT '生成答案所耗时长（秒）', 
	image_url VARCHAR(255) COMMENT '用户上传的图片链接', 
	PRIMARY KEY (chat_id), 
	CONSTRAINT fk_chat_user_id FOREIGN KEY(user_id) REFERENCES user (user_id)
);


CREATE TABLE orders (
	order_id INTEGER NOT NULL COMMENT '订单号（主键）' AUTO_INCREMENT, 
	user_id INTEGER NOT NULL COMMENT '下单用户ID', 
	area_id INTEGER COMMENT '关联用餐区域ID（可选）', 
	state ENUM('PENDING','PAID','CANCELED','COMPLETED') NOT NULL COMMENT '订单状态', 
	price NUMERIC(10, 2) NOT NULL COMMENT '订单总金额', 
	payment_method ENUM('WECHAT','ALIPAY','CASH','CARD','MEITUAN','DOUYIN','JD','OTHER') COMMENT '支付方式', 
	image_url VARCHAR(255) COMMENT '支付凭证图片URL', 
	created_at DATETIME NOT NULL COMMENT '订单创建时间' DEFAULT now(), 
	updated_at DATETIME NOT NULL COMMENT '订单更新时间' DEFAULT now(), 
	deleted_at DATETIME COMMENT '删除时间（软删除）', 
	PRIMARY KEY (order_id), 
	CONSTRAINT fk_order_user_id FOREIGN KEY(user_id) REFERENCES user (user_id), 
	CONSTRAINT fk_order_area_id FOREIGN KEY(area_id) REFERENCES dining_area (area_id)
);


CREATE TABLE order_items (
	order_item_id INTEGER NOT NULL COMMENT '订单项ID' AUTO_INCREMENT, 
	order_id INTEGER NOT NULL COMMENT '所属订单ID', 
	dish_id INTEGER NOT NULL COMMENT '关联菜品ID', 
	quantity INTEGER NOT NULL COMMENT '菜品数量', 
	unit_price NUMERIC(10, 2) NOT NULL COMMENT '下单时菜品单价快照', 
	PRIMARY KEY (order_item_id), 
	CONSTRAINT fk_order_item_order_id FOREIGN KEY(order_id) REFERENCES orders (order_id) ON DELETE CASCADE, 
	CONSTRAINT fk_order_item_dish_id FOREIGN KEY(dish_id) REFERENCES dish (dish_id)
);

