import sublime, sublime_plugin, os, shutil
from os.path import basename, dirname, realpath

class NewProjectCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.create_files()

	def create_files(self):

		if ( len(self.window.folders()) > 0 ):
			topFolder =  self.window.folders()[0]
		else:
			if (sublime.platform() == 'windows'):
				self.window.run_command('prompt_open_folder')
			else:
				self.window.run_command('prompt_open')

		if ( len(self.window.folders()) > 0 ):
			topFolder =  self.window.folders()[0]
			self.copy_files(topFolder)
		else:
			sublime.error_message("A folder is required to create a new project.")


	def copy_files(self, destFolder):

		stub_dir = os.path.join( sublime.packages_path(), 'Corona Editor', 'project_stub')
		stubs = ['main.lua','config.lua','build.settings']

		for x in range(0,3):
			stubpath = os.path.join( stub_dir, stubs[x] )
			shutil.copy(stubpath, destFolder)

		istrue = sublime.ok_cancel_dialog("Save your new project now?", "Save")
		
		if istrue:
			self.window.run_command("save_project_and_workspace_as")

		#open main.lua
		mainlua = os.path.join(destFolder, 'main.lua')
		print(mainlua)
		self.window.open_file(mainlua)
