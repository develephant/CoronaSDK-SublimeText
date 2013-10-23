import sublime, sublime_plugin
#    [ "close\tmath", "close()"],
class BuildListCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		name = ''
		for region in self.view.sel():
			lines = self.view.split_by_newlines(region)
			for l in lines:
				s = self.view.substr(l)
				s = s.strip()
				#split on dot and colon
				if s.find(':') > -1:
					sp = s.split(':')
				elif s.find('.') > -1:
					sp = s.split('.')

				name = sp[0]
				func = sp[1]
				name = func.split('(')[0]

				str += "[\"" + name + "\\t" + name + "\", \"" + func + "\"],\n"

		#self.view.insert(edit, 0, str)
		str += "\n//keywords\n"
		for t in types:
			str += "[\"" + t + "\\tLibrary\", \"" + t + "\"],\n"

		self.view.insert(edit, 0, str)
