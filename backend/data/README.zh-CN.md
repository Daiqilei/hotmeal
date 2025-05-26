# 数据库准备工作

在正式启动后端项目之前，建议先完成数据库的准备工作

环境：linux(windows\macOS)

初始化：使用 hotmeal.sql

以下命令请在终端中执行（无需输入 `$` 符号）：

推荐数据库：mysql8.0+
以下演示运行在：macOS Sequoia 15.5.1

- 下载 docker
- 查看 docker 版本

```shell
  docker -version
```

```shell
Docker version 28.0.4, build b8034c0
```

```shell
  docker pull mysql:latest
```

```shell
latest: Pulling from library/mysql
Digest: sha256:7839322bd6c3174a699586c3ea36314c59b61b4ce01b4146951818b94aef5fd7
Status: Image is up to date for mysql:latest
docker.io/library/mysql:latest
What's next:
View a summary of image vulnerabilities and recommendations → docker scout quickview mysql:latest
```

docker 创建一个数据库，容器名称这里使用的是 HOTMEAL。可以用默认的密码 hotmeal(实际开发使用自己的密码，注意 ⚠️：必须注意密码安全 🔐)
--name 指定容器的名字，可以是 mysql 或其他你喜欢的名字
-p 3306:3306 表示把 3306 映射到宿主机的 3306 3306 暴露在外

```shell
docker run --name hotmeal-db -e MYSQL_ROOT_PASSWORD=hotmeal -p 3306:3306 -d mysql
```

-运行之后会返回类似于“5ca16a4b68c40733d16e4bc50cd7c5e02e1afe0dba5e049c3e27c909e7dd8478”的容器名称

- 你可以尝试运行

```shell
docker ps
```

来查看运行状态。

- 接下来可以进入数据库

```shell
docker exec -it HOTMEAL mysql -uroot -p # - 根据提示输入密码
docker exec -it HOTMEAL mysql -uroot -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 9.3.0 MySQL Community Server - GPL

Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

- 我们进入了 mysql 容器 HOTMEAL

```
show databases;
```

看到了

> +--------------------+
> | Database |
> +--------------------+
> | information_schema |
> | mysql |
> | performance_schema |
> | sys |
> +--------------------+
> 4 rows in set (0.019 sec)
> 这是自带的。接下来我们开始创建数据库，这里建议指定 utf8mb4

```shell
CREATE DATABASE hotmeal CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
use hotmeal;
```

> 接下来你可以把打开项目 data 目录下的 hotmeal.sql 文件，将建表数据复制到命令行。这里略过具体细节，展示结果
> mysql> show tables;
> +-------------------+
> | Tables_in_hotmeal |
> +-------------------+
> | category |
> | dining_area |
> | dish |
> | menu_chat |
> | order_items |
> | orders |
> | user |
> +-------------------+
> 7 rows in set (0.004 sec)

####数据库的建立基本完成。
接下来我们要打开后端 flask 项目的文件夹，注意 ⚠️ 根据你的操作系统选择显示隐藏文件
你可以看到 .env 和 .env.example，根据样本填写你所需要的配置。
我这里演示的如下

> DB_USER=root
> DB_PASSWORD=hotmeal
> DB_HOST=127.0.0.1
> DB_PORT=3306
> DB_NAME=hotmeal
> DB_TZ=UTC

接下来，请移步 backend 下面的文档，进行后续操作
