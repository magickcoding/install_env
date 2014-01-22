#encoding:utf-8
"""
Usage:
  install.py --conf | -c <conf>
  install.py -h | --help
  install.py --version

Options:
  -h, --help                  显示帮助信息
  -c, --conf  <conf>          指定项目的环境配置文件路径
  --version                   输出版本号
"""
from docopt import docopt
import sys
import sh
import yaml
from tools.pyshell import *

class PlatformEnv(object):
    def __init__(self, conf_path):
        with open(conf_path) as config_stream:
            self.config = yaml.load(config_stream)
        self.hosts_list = self.config['hosts_list']
        self.cmds_path = self.config['cmds_path']

    def run(self):
        for host_conf in self.hosts_list:
            env.host_string = host_conf['host']
            env.user = host_conf['user']
            for cmd in self.cmds_path:
                self.check_cmd(cmd)
                if cmd not in self.config:
                    continue
                for params in self.config[cmd]:
                    run_cmd = self.cmd_add_params(cmd, params)
                    if run_cmd:
                        remote_shell(run_cmd, capture = True, warn_only = True)

    def cmd_add_params(self, cmd, params):
        if cmd == 'yum':
            return 'sudo %s -y install %s' % (self.cmds_path[cmd], params['name'])
        elif cmd == 'easy_install':
            if 'version' not in params:
                return 'sudo %s %s' % (self.cmds_path[cmd], params['name'])
            if params['version'] == '-U':
                return 'sudo %s -U %s' % (self.cmds_path[cmd], params['name'])
            return 'sudo %s %s==%s' % (self.cmds_path[cmd], params['name'], params['version'])
        else:
            return False

    def check_cmd(self, cmd):
        run_cmd = "which %s" % (cmd)
        ret = remote_shell(run_cmd, capture = True, warn_only = True)
        if ret.stdout.find('third') > -1:
            self.cmds_path[cmd] = ret.stdout
        

def main(arguments):
    conf = arguments['<conf>']
    if conf:
        platform_env = PlatformEnv(conf)
        platform_env.run()
    else:
        print 'conf path must be specfied'
        sys.exit(1)

if __name__ == "__main__":
    arguments = docopt(__doc__, version='0.0.1', help=True)
    main(arguments)
    
