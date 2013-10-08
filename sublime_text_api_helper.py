import sublime, sublime_plugin
import json, os

class SublimeTextApiHelperCommand(sublime_plugin.TextCommand):
    def run(self, edit, module=None):
        data = json.loads(sublime.load_resource('Packages/%s/3.json' % os.path.basename(os.path.dirname(__file__))))
        functions = []
        for key, value in data.items():
            if module == None or module == key:
                for function in value['functions']:
                    functions.append([key] + function)

        if module:
            items = [["%s: %s" % (_[1], _[2]), _[3][0:200]] for _ in functions]
        else:
            items = [["%s: %s: %s" % (_[0], _[1], _[2]), _[3][0:200]] for _ in functions]

        def on_done(index):
            if index >= 0:
                self.view.run_command("sublime_text_api_helper_output", {"text": functions[index][1]})
                for s in self.view.sel():
                    self.view.insert(edit, s.a, function_name)
        self.view.window().show_quick_panel(items, on_done)

class SublimeTextApiHelperOutputCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        for s in self.view.sel():
            self.view.replace(edit, s, text)