# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import os
import json
from os.path import basename, dirname, realpath

SOURCES_DIR = dirname(dirname(__file__))

class GrabCommand(sublime_plugin.WindowCommand):

    packageList = []

    s = None
    packageUrl = None
    archiveId = None
    sources = None

    def __init__(self, *args, **kwargs):
        super(GrabCommand, self).__init__(*args, **kwargs)

        #comp_path = os.path.join(sublime.packages_path(), "Corona Editor", "coronaget.json")
        json_data = sublime.load_resource("Packages/Corona Editor/coronaget.json")

        #json_data = open(comp_path)

        self.sources = json.loads(json_data)

        #json_data.close()

    def run(self, *args, **kwargs):
        _type = kwargs.get('type', None)

        self.packageList = []

        self.archiveId = _type

        if self.archiveId:
            self.list_archives()

    def list_archives(self):
        for name, url in self.sources[self.archiveId].items():
            try:
                # Python 2
                self.packageList.append([name.decode('utf-8'),
                                         url.decode('utf-8')])
            except AttributeError:
                # Python 3
                self.packageList.append([name, url])
                
        self.window.show_quick_panel(self.packageList,
                    self.set_package_location)

    def set_package_location(self, index):
        if (index > -1):
            self.packageUrl = self.packageList[index][1]

            if not self.window.folders():
                initialFolder = os.path.expanduser('~')
                try:
                    from win32com.shell import shellcon, shell
                    initialFolder = shell.SHGetFolderPath(0,
                                    shellcon.CSIDL_APPDATA, 0, 0)

                except ImportError:
                    initialFolder = os.path.expanduser("~")

            else:
                initialFolder = self.window.folders()[0]

            self.window.show_input_panel(
                "Select a location to extract the files: ",
                initialFolder,
                self.get_package,
                None,
                None
            )

    def get_package(self, location):
        if not os.path.exists(location):
            try:
                os.makedirs(location)
            except:
                sublime.error_message('ERROR: Could not create directory.')
                return False

        if not self.window.views():
            self.window.new_file()

        self.window.run_command("grab_get", {"option":
                    "package", "url": self.packageUrl, "location": location})
