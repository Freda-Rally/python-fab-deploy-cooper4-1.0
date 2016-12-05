#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Cooper4-1.0 Python 发布脚本
from fabric.api import *

# 发布任务列表
funcs = ('deploy', 'start', 'stop', 'restart', 'redeploy')

# 不同profile的ssh链接地址
deploy_ssh = {
    'test': [],
    'demo': [],
    'production': []
}
# 服务器项目代码目录
project_dir = '/www.bjzhzj.com'

# Git 远程地址
git_remote_url = 'https://github.com/Freda-Rally/Cooper4.git'

# Git 发布的branch
git_remote_branch = 'master'

# 项目名称
application_name = 'Cooper4'

# 生成的Jar的文件名
application_jar_name = 'Cooper4-1.0.1.jar'


# 发布总输入口
@task
def deploy(profile, func):

    print 'profile : %s task : %s ' % (profile, func)

    if validate(index=0, args=profile):

        for var in deploy_ssh[profile]:

            if validate(index=1, args=func):

                with settings(host_string=var):
                    if func == funcs[0]:
                        init(var)
                        start(profile=profile)
                    elif func == funcs[1]:
                        start(profile=profile)
                    elif func == funcs[2]:
                        stop()
                    elif func == funcs[3]:
                        restart(profile=profile)
                    elif func == funcs[4]:
                        stop()
                        init(var)
                        start(profile=profile)


# 验证参数 验证总入口中的参数是否合法

def validate(index, args):
    # 判断 参数是否合法
    if index == 0 and args in deploy_ssh.keys():
        return True
    elif index == 1 and args in funcs:
        return True
    else:
        print '[ERROR] deploy args validate error.'
        print 'INFO : index(%d) args(%s) has been error in env! please check!' % (index, args)

        return False

# 初始化发布

def init(var):

    print 'starting init deploy to host: %s ' % var

    run('test -d %s' % project_dir)
    clone()


# git clone文件

def clone():

    print 'git clone object url(%s),branch(%s)' % (git_remote_url, git_remote_branch)

    with cd(project_dir):
        run('rm -rf %s' % application_name)
        run('git clone -b %s %s' % (git_remote_branch, git_remote_url))
        build()

# build项目

def build():

    print 'build all models'

    run('test -d %s/%s' % (project_dir, application_name))

    with cd('%s/%s' % (project_dir, application_name)):
        run('./gradlew build -x test')
        run('cp build/libs/%s .' % application_jar_name)


# 启动模块

def start(profile):

    print 'start %s ' % application_name
    with cd('%s/%s' % (project_dir, application_name)):
        run('nohup java -jar -Dspring.profiles.active=%s %s '
            '>Cooper4-nohup.log 2>&1 & sleep 1' % (profile, application_jar_name))
        run('uptime')

# 停止模块

def stop():

    print 'stop %s ' % application_name

    with cd('%s/%s' % (project_dir, application_name)):
        run('test -f shared/tmp/pids/application.pid')
        run('kill -9 `cat shared/tmp/pids/application.pid`')
        run('rm shared/tmp/pids/application.pid')


# 重启模块

def restart(profile):

    print 'restart %s ' % application_name
    stop()
    start(profile=profile)


if __name__ == "__main__":

    # 参数为profile与task
    deploy(profile='production', func='start')