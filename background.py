from background_image import BackgroundImage


class Background:
    # theme as folder name
    def __init__(self, main, theme):
        self.main = main
        self.theme = theme
        if self.theme:
            self.path = 'Assets/Backgrounds/' + self.theme + '/'
        self.images_bg, self.images_fg = self.load()

    def load(self):
        images_bg = []
        images_fg = []
        if self.theme:
            for file in self.main.helper.get_files(self.path, 'png'):
                file_name = file[:-4].split('_')
                parallax = (float(file_name[1]), float(file_name[2]))
                if file_name[3] == '0':
                    images_bg.append(BackgroundImage(self.main, self.path + file, parallax))
                elif file_name[3] == '1':
                    images_fg.append(BackgroundImage(self.main, self.path + file, parallax))
        return images_bg, images_fg

    def draw(self, display, bg=True):
        if bg:
            for image in self.images_bg:
                image.draw(display)
        else:
            for image in self.images_fg:
                image.draw(display)
