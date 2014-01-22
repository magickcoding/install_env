依赖包:docopt,yaml,fabric
可以远程执行命令easy_install,yum等,执行效果就像在本机执行一样
you run follows cmds in remote machines just like local:
easy_install -U docopt 
easy_install docopt==0.6.1
easy_install -U yaml
来完成依赖包安装
注意:所有的配置文件均使用yaml格式
使用步骤：
1,配置某个项目需要安装的软件包信息,将配置文件放在指定目录conf下
3,执行命令python install.py --conf conf/searchapi.conf 
