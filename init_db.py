import sqlite3
# create database connection
connection = sqlite3.connect('database.db')
# 会自动创建一个数据库database

# 执行db.sql脚本，with open as语句，可以保证读取后自动关闭,这里注意要增加utf-8编码，否则报错
with open('db.sql', 'r', encoding='utf-8') as f:
    connection.executescript(f.read())
# SQLite 数据库模块的游标对象还包含了一个 executescript() 方法，
# 这不是一个标准的 API 方法，这意味着在其他数据库 API 模块中可能没有这个方法。
# 但是这个方法却很实用，它可以执行一段 SQL 脚本。

# 创建一个执行句柄，用来执行后面的语句
cur = connection.cursor()

# 插入两条文章
cur.execute("INSERT INTO posts (title, content) VALUES (?,?)",
('第一章', '算法管理系统使用说明第一部分')
)# 双引号或引号中执行SQL语句
cur.execute("INSERT INTO posts (title, content) VALUES (?,?)",
('第二章', '算法管理系统使用说明第二部分')
)

# 提交前面的数据操作
connection.commit()

# 关闭链接
connection.close()