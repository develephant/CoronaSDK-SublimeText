import sublime
import sublime_plugin


sublime_version = 2

if not sublime.version() or int(sublime.version()) > 3000:
    sublime_version = 3

try:
    # Python 3
    from .grab.commands.grab_command import GrabCommand
    from .grab.commands.grab_get_command import GrabNewFileCommand
    from .grab.commands.grab_get_command import GrabGetCommand

except (ValueError):
    # Python 2
    from grab.commands.grab_command import GrabCommand
    from grab.commands.grab_get_command import GrabNewFileCommand
    from grab.commands.grab_get_command import GrabGetCommand

