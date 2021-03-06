# Copyright 2014 0xc0170
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Settings needed:
UV4
IARBUILD
PROJECT_ROOT
GCC_BIN_PATH
"""

import os
from os.path import expanduser, normpath

import yaml

from os.path import join, pardir, sep

class ProjectSettings:
    PROJECT_ROOT = os.environ.get('PROJECT_GENERATOR_ROOT') or join(pardir, pardir)
    DEFAULT_TOOL = os.environ.get('PROJECT_GENERATOR_DEFAULT_TOOL') or 'uvision'

    def __init__(self):
        """ This are default enviroment settings for build tools. To override,
        define them in the projects.yaml file. """
        self.paths = {}
        self.paths['uvision'] = os.environ.get('UV4') or join('C:', sep,
            'Keil', 'UV4', 'UV4.exe')
        self.paths['iar'] = os.environ.get('IARBUILD') or join(
            'C:', sep, 'Program Files (x86)',
            'IAR Systems', 'Embedded Workbench 7.0',
            'common', 'bin', 'IarBuild.exe')
        self.paths['gcc'] = os.environ.get('ARM_GCC_PATH') or ''
        self.paths['definitions'] = join(expanduser('~/.pg'), 'definitions')
        if not os.path.exists(join(expanduser('~/.pg'))):
            os.mkdir(join(expanduser('~/.pg')))
        self.generated_projects_dir_default = 'generated_projects'
        self.generated_projects_dir = self.generated_projects_dir_default

    def update(self, settings):
        if 'tools' in settings:
            for k, v in settings['tools'].items():
                if k in self.paths:
                    self.paths[k] = v['path'][0]
        if 'definitions_dir' in settings:
            self.paths['definitions'] = normpath(settings['definitions_dir'][0])

        if 'export_dir' in settings:
            self.generated_projects_dir = normpath(settings['export_dir'][0])

    def set_definitions_file(self, def_dir):
        self.paths['definitions'] = def_dir

    def get_env_settings(self, env_set):
        return self.paths[env_set]
