import sublime, sublime_plugin, os, shutil
from os.path import basename, dirname, realpath

SUBLIME_VERSION = 3000 if sublime.version() == '' else int(sublime.version())

class NewProjectCommand(sublime_plugin.WindowCommand):
	def run(self):
		if SUBLIME_VERSION < 3000:
			message_dialog("This feature is only available in Sublime Text 3.")
		else:
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

		stubs = ['main.lua','config.lua','build.settings']

		for x in range(0,3):
			data = sublime.load_binary_resource("Packages/Corona Editor/project_stub/"+stubs[x])
			# Open a file
			fo = open(os.path.join(destFolder, stubs[x]), "wb")
			fo.write(data);

			# Close opend file
			fo.close()

		#open main.lua
		self.window.open_file(os.path.join(destFolder, "main.lua"))
		self.window.active_view().set_syntax_file("Packages/Corona Editor/CoronaSDKLua.tmLanguage")

		istrue = sublime.ok_cancel_dialog("Save your new project now?", "Save")
		
		if istrue:
			self.window.run_command("save_project_and_workspace_as")


