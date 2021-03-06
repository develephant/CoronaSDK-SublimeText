import sublime
import sublime_plugin
import os
from os.path import basename, dirname, realpath
import json

PLUGIN_DIR = dirname(realpath(__file__))
SUBLIME_VERSION = 3000 if sublime.version() == '' else int(sublime.version())

class CoronaSnippetCommand(sublime_plugin.TextCommand):

	completions = {}
	_tmpCompletions = []

	def __init__(self, *args, **kwargs):
		super(CoronaSnippetCommand, self).__init__(*args, **kwargs)

		if (len(self.completions) == 0):
			# Files in the package are loaded differently in ST2 as ST3
			if (SUBLIME_VERSION < 3000):
				comp_path = PLUGIN_DIR
				comp_path = os.path.join(comp_path, "sublime-completions", "API-completions-Corona.sublime-settings")

				json_data = open(comp_path)
				self._tmpCompletions = json.load(json_data)
				json_data.close()

			else:
				self._tmpCompletions = json.loads(sublime.load_resource('Packages/Corona Editor/sublime-completions/API-completions-Corona.sublime-settings'))

				for c in self._tmpCompletions['completions']:

					trigger = c[0].split("\t")[0]
					name = c[0].split("\t")[1]
					if c[1].find("(") > -1:
						self.completions[name+"."+trigger] = name+"."+c[1]

			self._tmpCompletions = None

	def run(self, edit, **args):
		trigger = args['name']
		if trigger in self.completions:
			self.view.run_command( "insert_snippet", { "contents": self.completions[trigger] } )
		else:
			self.view.run_command( "insert_snippet", { "name": 'Packages/Corona Editor/snippets/'+ trigger +'.sublime-snippet' } )
