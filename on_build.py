import sublime, sublime_plugin

class OnBuildCommand(sublime_plugin.WindowCommand):
	def run(self, **args):
		#print("args",args)
		platform = sublime.platform()
		arch = sublime.arch()

		cmd = args['cmd']
		file_regex = args['file_regex']

		if platform == 'windows' and arch == "x64":
			cmd = ["C:\\Program Files (x86)\\Corona Labs\\Corona SDK\\Corona Simulator.exe", cmd[1]]
		elif platform == 'windows':
			cmd = ["C:\\Program Files\\Corona Labs\\Corona SDK\\Corona Simulator.exe", cmd[1]]
		#else it must be Mac - carry on

		if not cmd == None:
			self.window.run_command('exec', { 'kill' : True }) #close sim if open
			self.window.run_command('exec', {'cmd': cmd, 'file_regex': file_regex})
