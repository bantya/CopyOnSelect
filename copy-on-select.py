import sublime
import sublime_plugin
import functools


class CopyOnSelectCommand(sublime_plugin.EventListener):

    pending = 0

    def handleTimeout(self, view):
        self.pending = self.pending - 1
        if self.pending == 0:
            # There are no more queued up calls to handleTimeout, so it must have
            # been 1000ms since the last modification
            self.onIdle(view)

    def on_selection_modified(self, view):
        self.pending = self.pending + 1
        # Ask for handleTimeout to be called in 1000ms
        settings = sublime.load_settings("CopyOnSelect.sublime-settings")
        timeout = settings.get("copy_on_select_timeout", 1000)
        sublime.set_timeout_async(functools.partial(self.handleTimeout, view), timeout)

    def onIdle(self, view):
        string = ""
        for region in view.sel():
            if not region.empty():
                string += view.substr(region)
        if string != "":
            sublime.set_clipboard(string)
            # print(string)
