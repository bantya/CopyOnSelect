# This plugin is greatly inspired by https://github.com/chrifpa/CopyOnSelect
import sublime
import sublime_plugin
import functools

def load_settings():
    return sublime.load_settings('CopyOnSelect.sublime-settings')

def get_setting(setting, default = ''):
    return load_settings().get(setting, default)

def save_settings(status):
    load_settings().set('to_enable', status)
    sublime.save_settings('CopyOnSelect.sublime-settings')
    sublime.status_message('CopyOnSelect: Toggled plugin status successfully!')
    print("\n[CopyOnSelect: Toggled plugin status successfully!]\n")

class CopyOnSelectCommand(sublime_plugin.EventListener):
    @property
    def delay(self):
        delay = get_setting("delay", 1000)

        if delay:
            try:
                return int(delay)
            except:
                pass
        return 1000

    # number of pending calls to handle_timeout
    pending = 0

    def handle_timeout(self, view):
        self.pending = self.pending - 1
        if self.pending == 0:
            # There are no more queued up calls to handle_timeout, so it must have
            # been {delay}ms since the last modification
            self.on_idle(view)

    def on_selection_modified(self, view):
        if get_setting('to_enable', True) == False:
            return

        self.pending = self.pending + 1
        # Ask for handle_timeout to be called in DELAY ms
        sublime.set_timeout(functools.partial(self.handle_timeout, view), self.delay)

    def on_idle(self, view):
        string = ""
        for region in view.sel():
            if not region.empty():
                string += view.substr(region)
        if string != "":
            sublime.set_clipboard(string)

class ToggleCopyOnSelectCommand(sublime_plugin.WindowCommand):
    def run(self):
        if get_setting('to_enable') == False:
            save_settings(True)
        elif get_setting('to_enable') == True:
            save_settings(False)
