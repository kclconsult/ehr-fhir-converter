from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.unittest")

default_task = "publish"

@init
def initialize(project):
    project.build_depends_on('mockito')
