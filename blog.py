from flask import Flask,render_template, request, url_for, flash, redirect
#  request - 代表请求，表单中填写的信息都可以通过request获取到
# flash - 代表提示语，比如提示用户标题不能为空，这句话放在flash变量中，页面从flash中获取
# redirect - 代表页面重定向，也就是转到另外一个页面。

import sqlite3 #引入 sqlite3
import setting  #导入配置
app = Flask(__name__) #创建一个Flask对象
app.config.from_object(setting)  #加载配置
app.config['SECRET_KEY'] = 'mancy is so good'
# app.config后面的值改成随便的字符串。这是用来做浏览器和flask之间的加密，防止黑客串改数据。

def get_db_connection():
  '''连接到database.db数据库'''
  conn = sqlite3.connect('database.db')
  # 设置数据的解析方法，有了这个设置，就可以像字典一样访问每一列数据
  conn.row_factory=sqlite3.Row
  # 查询所有数据，放到变量posts中
  return conn
def get_post(post_id):
  '''根据post_id从数据库中获取post'''
  conn=get_db_connection()
  post=conn.execute('SELECT * From posts WHERE id = ?', (post_id,)).fetchone()
  conn.close()
  return post

@app.route('/') #如果请求根目录url，就访问下面的hello方法
def index():
 
  conn = get_db_connection()
  posts=conn.execute('SELECT * FROM posts').fetchall()
  conn.close()

  # return render_template('index.html')  
  return render_template('index2.html', posts=posts) #查询到的数据传给网页

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts/<int:post_id>')
# 帖子页面
def post(post_id):
  post = get_post(post_id) #获取数据库的对应行
  return render_template('post.html',post=post)  #将这行数据给前端页面

# 新建页面
@app.route('/posts/new',methods=('GET','POST'))
def new():
  '''
  这个方法接受GET请求和POST请求。
  如果是GET请求就直接显示新建页面。
  如果是POST请求就把用户提交的内容保存到数据库，然后重定向到列表页。
  '''
  if request.method == 'POST':
    title = request.form['title']
    content = request.form['content']
    if not title:
      flash('标题不能为空!')
        # 仅调用flash只是发给客户端一条信息，不负责显示的。
    elif not content:
        flash('内容不能为空')   
    else:
      conn = get_db_connection()
      conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
      conn.commit()
      conn.close()
      return redirect(url_for('index'))
      # 新内容储存在数据库中
  return render_template('new.html')

# 编辑
@app.route('/posts/<int:id>/edit', methods=['GET','POST'])
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/posts/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" 删除成功!'.format(post['title']))
    return redirect(url_for('index'))

if __name__== '__main__':
  app.run()