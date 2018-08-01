# web 8
# 数据库
#

"""
数据库是应用最广泛的计算机软件
# 数据库现在主要分 关系型数据库（传统） 和 NoSQL（新式比如 mongodb）
# 和一些其他数据库（比如 fb 的图数据库）
# 本课只讲 关系型数据库 和 mongodb
本节课讲 sqlite 和 mongodb

关系型数据库介绍: sqlite3
sqlite 是 python3 自带的数据库，不用安装
但是需要安装一个叫 sqlitebrowser 的管理软件
# 常用的关系型数据库有 mysql postgresql sqlite 等（具体区别上课再说）
# mysql 使用人数最多, 在开发中一般使用 sqlite, postgresql: 微软的数据库
# 传统数据库以表的形式存储数据
# 一张表可以有很多个字段

# 以用户表为例, 存储 4 个数据的表结构如下
# 用户 id
# 用户名
# 密码
# 邮箱
#
# 范例数据如下
# 1     gua     123     gua@qq.com
# 2     gua1    23      gua1@q.com

# 数据库通过 SQL 来操作数据
# SQL （结构化查询语言）
# 操作数据库的接口 也就是操作数据库的方法
# 增加数据
# 删除数据
# 修改数据
# 查询数据
# CRUD
# create retrieve update delete
#
# 数据库的更多的概念，上课会解释（文字太苍白）
# 一般不会写 sql 语句, 都是在 model 层面对数据进行操作
# 请下载 sqlitebrowser 软件（这是一个管理 sqlite 数据库的免费软件，自行搜索或者等群内链接）

# SQL 语句如下（仅为范例，上课会讲具体的语法）
    创建表格的语句
    # 注意 CREATE TABLE 这种语句不分大小写
    CREATE TABLE `users`(表名) (
        `id`(字段名)	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, (字段的限制符, 一般不在这边限制)
        `username`	TEXT NOT NULL UNIQUE,
        `password`	TEXT NOT NULL,
        `email`	TEXT
    )

    插入语句
    INSERT INTO
        `users` (表名)  (`id`,`username`,`password`,`email`) (插入的字段)
    VALUES
        (2,'','',NULL); (插入的值)

    删除语句
        DELETE FROM
            users (表名)
        WHERE
            id= ? # 设为问号, 在执行sql语句时传入相应的tuple可以防止 sql 注入

    编辑语句
    UPDATE
        `users` (表名)  SET `username`=?  (需要编辑的字段)
    WHERE   (限定符, 更新哪一行)
        `_rowid_`='2';

    查询语句
    SELECT  (选择哪几个字段)
        id, username, email
    FROM    (从哪张表查询)
        users
    WHERE   (只看那些符合规定的用户)
        username=? and password=?

sqlite_demo:
    执行流程:
        1. 指定数据库名称
            db_path = 'web8.sqlite'   # 若不存在, 会自动创建
        2. 通过sqlite3这个库连接到数据库, 并返回一个连接对象
            conn = sqlite3.connect(db_path)
        3. 创建表格
            调用create方法 (用 execute 执行一条 sql 语句)
            conn.execute(sql_create)
        4, 插入表格元素,  ... 增删改查
            调用相应方法并执行
            # sql语句参数拼接要用 ?，execute 中的参数传递必须是一个 tuple 类型
            conn.execute(sql_insert, (username, password, email))
        5. 提交修改
            # 必须用 commit 函数提交你的修改, 否则你的修改不会被写入数据库
            conn.commit()
        6, 关闭连接
            conn.close()

关系型数据库介绍: mongodb

mongodb 需要安装，链接如下
软件本身
http://www.runoob.com/mongodb/mongodb-window-install.html
有 mongo compass 无须安装, 它也是一个管理软件, 安装好之后需要在本地创建 数据文件夹: C:\data\db
管理软件 robo 3T
https://robomongo.org/download
软件使用:
    找到安装 mongodb 的目录, C:\Program Files\MongoDB\Server\4.0\bin, 并开启 mongod.exe
    使用 robomongo 连接到数据库

注意，需要安装 pymongo 这个库
pip3 install pymongo
在你安装并开启 mongo 之后，就可以使用 pymongo 来连接使用 mongodb 了

mongo_demo 执行流程:
    1. 创建连接:
        # 连接 mongo 数据库, 主机是本机, 端口是默认的端口
        client = pymongo.MongoClient("mongodb://localhost:27017")
    2. 设置使用的数据库: (client 其实是一个特殊的字典)
        database = client['数据库名字']
    3. mongo 无须创建表 (MongoDB里面是document), 可以直接插入
        database.my_user.insert(u)        # u 是一个字典, 包含了一个对象的字段名和值
    4. 编辑字段:
        # query 表示更新那些拥有某个字段值的对象, form 表示需要更新哪个字段(默认更新查询到的第一个对象
        # 如果想要更新所有查询到的数据, 需要加入参数 {'multi': True}, 相当于 db.user.update(query, form, multi=True)
        database.my_user.update(query, form, **options)
    5. 查询字段:
        # find 返回一个可迭代对象, 使用 list 函数转为数组
        # query 为一个参数字典, 表示查询那些拥有某些字段值的对象, 可以设置查询条件: $gt $lt $let $get $ne $or
        #  query = {
        #         '随机值': {
        #             '$gt': 1
        #         },
        #     }
        #  field 表示 需要提取哪些字段
        # field = {
        #         # 字段: 1 表示提取这个字段
        #         # 不传的 默认是 0 表示不提取
        #         # _id 默认是 1
        #         'name': 1,
        #         '_id': 0,
        #     }
        database.my_user.find(query, field)
    6. 删除操作
        一般不删除
        database.my_user.remove()
        一般添加一个新的字段来判断是否被用户删除了
        "_deleted": False       # 默认是false
        当用户查询时, 设置query来find, 同时隐藏该字段
        # all 是给用户使用的查询函数
        # def all():
        #     query = {
        #         '_deleted': False,
        #     }
        #     user_list = list(db.user.find(query))
        #     us = []
        #     for u in user_list:
        #         u.pop('_deleted')
        #         us.append(u)
        #     print('所有用户', len(us), us)
"""


