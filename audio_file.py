import pygame as pg


class AudioFile:
    # music in music folder with file name format 'Theme_Number (int)', sound in sound folder with file name format 'Name_Repeat Option (bool)'
    def __init__(self, main, name, path, volume, repeat=False):
        self.main = main
        self.name = name
        self.audio = pg.mixer.Sound(path)
        self.audio.set_volume(volume)
        self.repeat = repeat

    def play(self, fade, loops):
        if self.repeat or not self.repeat and self.audio.get_num_channels() == 0:
            self.audio.play(loops=loops, fade_ms=int(fade * 1000))

    def stop(self, fade):
        if fade:
            self.audio.fadeout(int(fade * 1000))
        else:
            self.audio.stop()

    def set_volume(self, volume):
        self.audio.set_volume(volume)
