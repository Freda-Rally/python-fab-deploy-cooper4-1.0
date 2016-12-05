# python-fab-deploy-cooper4-1.0
为cooper4-1.0做的 自动发布脚本

使用方法:

    请先安装 fabfic python2.7环境

        将文件复制到项目中.更改参数.

        进入项目目录下执行如下命令:

        profile为项目的profile func为task 请更改脚本中的部分参数.

        发布 : fab deploy:profile='production',func='deploy'
        重新发布:fab deploy:profile='production',func='redeploy'
        启动:fab deploy:profile='production',func='start'
        停止:fab deploy:profile='production',func='stop'
        重启:fab deploy:profile='production',func='restart'
