import json


class SettingHandler:
    def __init__(self, main):
        self.main = main
        self.path = 'Assets/Misc/'
        self.settings, self.settings_default = self.load_settings()

    def load_settings(self):
        with open(self.path + 'settings.json') as json_file:
            settings = json.load(json_file)
        with open(self.path + 'settings_default.json') as json_file:
            settings_default = json.load(json_file)
        return settings, settings_default

    def save_settings(self):
        settings = {'Audio': self.main.audio_handler.audio_settings, 'Controls': self.main.controls_handler.controls_settings, 'Game': [],
                    'Video': self.main.window.video_settings}
        with open(self.path + 'settings.json', 'w') as fp:
            json.dump(settings, fp, indent=4)

    def update_default_settings(self):
        settings = {'Audio': self.main.audio_handler.audio_settings, 'Controls': self.main.controls_handler.controls_settings, 'Game': [],
                    'Video': self.main.window.video_settings}
        with open(self.path + 'settings_default.json', 'w') as fp:
            json.dump(settings, fp, indent=4)
        print('Default Settings Updated')
