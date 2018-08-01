"""
web20
server 层次
    0.web server app
    1.web server framework
    2.http server
    3.tcp server

nginx, gunicorn 和 wsgi 的区别
    nginx : http server
    gunicorn: http server
    wsgi: 包装出来一个app

nginx gunicorn的区别
data -> nginx -> gunicorn -> wsgi -> app ?

nginx的优点
    1. 反向代理
        gunicorn 2000
        gunicorn 2002
        nginx 80
    2. 负载均衡
        haproxy 去访问google.com
    3. 静态文件托管
        send_by_directory 每次都send很不好
        配置了一个rule，保存在nginx的缓存，不会走到app这一层
    4. 缓冲
        traffic busy
        缓冲负载

上传头像功能
    model 层:
        在 model/user 类里添加 'user_image' 字段, 使每个用户拥有自己的所属头像: self.user_image = 'default.png'
    view 层:
        在 profile 页面添加一个 form 表单: (需要 add_img 路由函数)
            <h1>Upload new File</h1>
            <form method=post action={{ url_for("index.add_img") }} enctype=multipart/form-data>
            <p>
                <input type=file name=file>
                <input type=submit value=Upload>
            </p>
            </form>
        注解: enctype=multipart/form-data, 表示: 不对字符编码, 在使用包含文件上传控件的表单时，必须使用该值。
    routes 层:
        在 routes/index 里添加 add_img 路由:
            1. 文件后缀要做过滤 img png gif
                def allow_file(filename):               # 判断是否是合适的文件类型
                    suffix = filename.split('.')[-1]
                    from config import accept_user_file_type
                    return suffix in accept_user_file_type
            2. 文件名也要小心
                # werkzeug.utils中的 secure_filename 可对文件名进行转换
                filename = secure_filename(file.filename)
            具体函数:
                @main.route('/addimg', methods=["POST"])
                def add_img():
                    u = current_user()
                    if u is None:           # 如果用户为空, 就让他转到登录界面
                        return redirect(url_for(".index"))
                    if 'file' not in request.files:         # 如果请求中没有file对象, 重启请求原路径, 会因为调用了GET方法被拦截
                        return redirect(request.url)
                    file = request.files['file']            # 从请求的files字典中得到 file 对象
                    if file.filename == '':
                        return redirect(request.url)
                    if allow_file(file.filename):
                        filename = secure_filename(file.filename)               # 将传上来的 filename 进行转换
                        file.save(os.path.join(user_file_director, filename))   # 将上传上来的文件保存在一个地址, save为一个flask本身的函数
                        u.user_image = filename                                 # 设置该用户的头像信息
                        u.save()
                    return redirect(url_for(".profile"))

展示头像功能
    model 层:
        在 model/topic 类里 添加根据用户ID 找到用户的功能
            def user(self):
                u = User.fing(id=self.user_id)
                return u
    view 层:
        在 topic/index 页面展示每个 topic 所拥有的头像, 通过 img src= '' 发起请求
            <img src="{{ url_for('index.uploads',  filename=t.user().user_image) }}"/>
    routes 层:
        在 routes/topic 里的 index 路由函数里传入 topic 即可
        在 routes/index 里添加 uploads 路由函数, 接收filename 作为参数
            @main.route('uploads/<filename>')
            def uploads(filename):
                # send_from_directory 函数为 flask 自带的函数, 主要是从文件夹中找到对应的文件
                return send_from_directory(user_file_director, filename)
具体见:
       flask upload file: http://flask.pocoo.org/docs/1.0/patterns/fileuploads/



发私信功能 (基于 HTTP)

    model 层面:
        数据内容:
            1. id
            2. content
            3. title
            4. sender_id # 这个不应该是从表单里面拿的，hidden，伪造成任何人
            5. receiver_id
            6. read
        数据操作:
            set_sender_id: 因为 sender_id 不应该从表单层面传递过去, 因此需要在发送的时候直接存储到数据库
            mark_read: 通过该函数来标记该私信是否已经被接收的用户读过了

    view 层面:
        在 templates 文件夹里添加 mail文件夹, 并添加 index 页面和私信的 detail 页面
        index 页面: (添加 index 路由函数)
            1. 发送私信的表单  (添加 send 路由函数)
            2. 显示当前用户发送的所有私信, 点击链接显示详细信息 (detail 路由函数处理)
            3. 显示当前用户接收的所有私信, 点击链接显示详细信息 (detail 路由函数处理)
        detail 页面: (添加 detail 路由函数)
            显示私信的详细信息:  发送者, 接收者, 私信内容

    routes 层面:
        添加 routes/mail.py 文件, 拥有3个路由函数:
            index 路由函数
                得到当前用户, 找到属于当前用户的所有收到的私信和发送的私信
            send 路由函数
                从传过来的表单数据中构造新的 mail 数据, 并重置 sender_id 再保存到数据库
            detail 路由函数
                从传过来的请求数据中得到私信 ID
                根据 ID 找到该条私信
                    mail = Mail.find(id)
                根据当前用户判断
                    #不是你自己收发的，你肯定不能看
                    #不是收的人，那你看了也不会变成已读
                        if current_user().id == mail.receiver_id:
                            mail.mark_read()
                        if current_user().id in [mail.receiver_id, mail.sender_id]:
                            return render_template("mail/detail.html", mail=mail)
                        else:
                            return redirect(url_for(".index"))

"""