import sublime, sublime_plugin
import string


class CoronaCompletionsPackage():
  def init(self):
    self.api = {}
    self.settings = sublime.load_settings('API-Completions-Package.sublime-settings')
    self.API_Setup = self.settings.get('completion_active_list')

    # Caching completions
    if self.API_Setup:
      for API_Keyword in self.API_Setup:
        self.api[API_Keyword] = sublime.load_settings('API-completions-' + API_Keyword + '.sublime-settings')

    # Caching extended completions(deprecated)
    if self.settings.get('completion_active_extend_list'):
      for API_Keyword in self.settings.get('completion_active_extend_list'):
        self.api[API_Keyword] = sublime.load_settings('API-completions-' + API_Keyword + '.sublime-settings')



# In Sublime Text 3 things are loaded async, using plugin_loaded() callback before try accessing.
api = CoronaCompletionsPackage()

if int(sublime.version()) < 3000:
  api.init()
else:
  def plugin_loaded():
    global api
    api.init()



class CoronaCompletionsPackageEventListener(sublime_plugin.EventListener):
  global api

  def on_query_completions(self, view, prefix, locations):
    self.completions = []

    for API_Keyword in api.api:
      # If completion active
      if (api.API_Setup and api.API_Setup.get(API_Keyword)) or (api.settings.get('completion_active_extend_list') and api.settings.get('completion_active_extend_list').get(API_Keyword)):
        scope = api.api[API_Keyword].get('scope')
        if scope and view.match_selector(locations[0], scope):
          self.completions += api.api[API_Keyword].get('completions')

    if not self.completions:
      return []

    # extend word-completions to auto-completions
    compDefault = [view.extract_completions(prefix)]
    compDefault = [(item, item) for sublist in compDefault for item in sublist if len(item) > 3]
    compDefault = list(set(compDefault))
    completions = list(self.completions)
    completions = [tuple(attr) for attr in self.completions]
    completions.extend(compDefault)
    return (completions)
