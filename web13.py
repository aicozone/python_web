"""
今天上课开始 我们要使用 flask 框架来替代我们之前实现的 server.py
我们写的 server.py 相当于一个简化版的 flask
本质是一样的, 使用方法也类似

需要安装 flask, 使用 pip 安装如下(不懂就问/等上课)
pip3 install flask

在Linux服务器上系统自带了python3
但并没有自带pip3
安装 pip3
apt-get install python3-pip

web 框架的发展历史
        c 语言写web
        perl 语言写web(风靡一时)
            带有大量的正则表达式
            写的代码可读性非常差
            现在没人用
        PHP
        java
        ruby on rails
            在国外很火, 在中国已经没有可能了
        python
            flask
            django
        node.js



flask 笔记
    flask 初始化方法:    需要导入 Flask
        # 先要初始化一个 Flask 实例, 类似于server, 作用是 绑定主机和端口, 监听请求, 接收请求, 处理请求, 发送响应
        # app = Flask(__name__)
    运行方法:
        # 设置参数:
            # config = dict(
            #         debug=True,       # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
            #         host='0.0.0.0',   # 主机设置为这个可以让其他机器访问
            #         port=2000,
            #     )
        # 运行服务器:
            # app.run(**config)
    设置路由和路由函数的方法
        # 设置路由:
            # @app.route('请求的path',methods=['请求的方法, 默认是GET']
                # 用 app.route 函数定义路由，参数是一个 path 路径
                # 注意 methods 参数是一个 list，它规定了这个函数能接受的 HTTP 方法
                # @ 为装饰器用法

        # 设置路由函数:
            @app.route下一行紧跟着的函数是处理这个请求的函数
                # 路由函数返回的东西就是响应的 http body
        # 动态路由
            # <int:todo_id> 的方式可以匹配一个 int 类型
            # int 指定了它的类型，省略的话参数中的 todo_id 就是 str 类型
            #
            # 这个概念叫做 动态路由
            # 意思是这个路由函数可以匹配一系列不同的路由
            #
            # 动态路由是现在流行的路由设计方案
            在路由定义时增加参数
            @main.route('/delete/<int:todo_id>/')
            在路由函数处传入参数
            def delete(todo_id)

    模块化路由的方法: 引入蓝图功能, 导入 Blueprint
        # 创建蓝图对象:
            # 第一个参数是蓝图的名字, 以后会有用(add函数里面就用到了)
            # 第二个参数是套路
            main = Blueprint('todo', __name__)

            路由定义在蓝图中:
                @main.route()

        # 在Flask 实例处注册蓝图
            # todo_routes是蓝图对象, url_prefix 可以用来给蓝图中的每个路由加一个前缀
            app.register_blueprint(todo_routes, url_prefix='/todo')

    各类接口:
        # render_template, 模板渲染接口
            读取项目根目录下 templates(必须是这个名字, 接口才能读取到) 文件夹下面的 jinja2 模板,
            可以传入参数进行渲染, 产生一个 http body 字符串
                render_template('message_index.html', messages=message_list)
                    # messages 是传给模板的参数，这样就能在模板中使用这个变量了
                    # 在模板中还可以调用局部函数, 如url-for, 或者是 messages 所拥有的方法
        # request, 请求对象, 只对本次请求有效
            request.method: 请求的方法
            request.args: flask 保存 URL 中的参数的属性, 返回一个不可变字典: ImmutableMultiDict([('a', '1')])
            request.form: flask 保存 POST 请求的表单数据的属性, 返回也是一个不可变字典
        # redirect, 重定向到某一路由
        # url_for,
            # 一般来说，我们会用 url_for 生成路由，如下
            # 注意, url_for 参数是 路由函数 的名字（格式为字符串）
                redirect(url_for('message_view'))
            # url_for 可以传递参数，先匹配动态路由，如果动态路由匹配失败则变成 query 参数
                前端请求: {{ url_for('todo.delete', todo_id=t.id) }}
            # 蓝图中的 url_for 需要加上蓝图的名字，这里是 todo

jinja2 笔记
    语法:
        # Jinja2 模板的注释语法，这样的注释并不会在生成的 HTML 代码中出现
            {#     #}
        # 引用变量语句:
            {{ 变量名  }}
        # 调用循环判断语句:
            {% 循环判断语句 %}
                # {% for m in messages %}
                #     <div>{{ m['content'] }}</div>     # m 为字典, 也可以用 . 语法使用变量: m.content
                # {% endfor %}
"""