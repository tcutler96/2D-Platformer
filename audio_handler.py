from audio_file import AudioFile


class AudioHandler:
    def __init__(self, main):
        self.main = main
        self.path = 'Assets/Audio/'
        self.audio_settings = self.main.settings_handler.settings['Audio']
        self.audio_settings_default = self.main.settings_handler.settings_default['Audio']
        self.music, self.sound = self.load_audio()
        self.music_theme = None
        self.music_deafen = False

    def load_audio(self):
        music = {None: []}
        for file in self.main.helper.get_files(self.path + 'Music/', 'wav'):
            file_name = file[:-4].split('_')
            name = '_'.join(file_name[:-1])
            path = self.path + 'Music/' + file
            volume = self.audio_settings['master_volume'] * self.audio_settings['music_volume']
            if name in music.keys():
                music[name].append(AudioFile(self.main, name, path, volume))
            else:
                music[name] = [AudioFile(self.main, name, path, volume)]
        sound = {}
        for file in self.main.helper.get_files(self.path + 'Sound/', 'wav'):
            file_name = file[:-4].split('_')
            name = '_'.join(file_name[:-1])
            path = self.path + 'Sound/' + file
            volume = self.audio_settings['master_volume'] * self.audio_settings['sound_volume']
            repeat = int(file_name[-1])
            sound[name] = AudioFile(self.main, name, path, volume, repeat)
        return music, sound

    def change_volume(self, name, value):
        music = False
        sound = False
        if name == 'master' and value != self.audio_settings['master_volume']:
            self.audio_settings['master_volume'] = value
            music = True
            sound = True
        elif name == 'music' and value != self.audio_settings['music_volume']:
            self.audio_settings['music_volume'] = value
            music = True
        elif name == 'sound' and value != self.audio_settings['sound_volume']:
            self.audio_settings['sound_volume'] = value
            sound = True
        self.update_volume(music, sound)

    def update_volume(self, music, sound):
        if music:
            for audio in self.music[self.music_theme]:
                audio.set_volume(self.audio_settings['master_volume'] * self.audio_settings['music_volume'])
        if sound:
            for audio in self.sound:
                self.sound[audio].set_volume(self.audio_settings['master_volume'] * self.audio_settings['sound_volume'])

    def play_sound(self, sound, fade=0, loops=0):
        self.sound[sound].play(fade, loops)

    def stop_sound(self, sound, fade=0):
        self.sound[sound].stop(fade)

    def switch_music(self, music_theme=None, fade=0):
        if music_theme != self.music_theme:
            if self.music_theme:
                for audio in self.music[self.music_theme]:
                    audio.stop(fade)
            if music_theme and music_theme in self.music.keys():
                self.music_theme = music_theme
                for audio in self.music[self.music_theme]:
                    audio.play(fade * 5, -1)
            else:
                self.music_theme = None

    def toggle_music_deafen(self):
        self.music_deafen = not self.music_deafen
        if self.music_theme:
            if self.music_deafen:
                self.change_volume('music', self.audio_settings['music_volume'] / 4)
            else:
                self.change_volume('music', self.audio_settings['music_volume'] * 4)

    def reset_settings(self):
        self.change_volume('master', self.audio_settings_default['master_volume'])
        self.change_volume('music', self.audio_settings_default['music_volume'])
        self.change_volume('sound', self.audio_settings_default['sound_volume'])
