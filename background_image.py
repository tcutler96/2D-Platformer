import pygame as pg


class BackgroundImage:
    # image name format 'Order_X Parallax_Y Parallax_Background/ Foreground (0/ 1)', fill empty space with (255, 255, 255)
    def __init__(self, main, path, parallax=(0, 0)):
        self.main = main
        if isinstance(path, str):
            self.image = self.main.helper.load_image(path)
        else:
            self.image = path
        self.size = (self.image.get_width(), self.image.get_height())
        self.parallax = parallax
        self.debug_colour = (225, 225, 225)

    def draw(self, display):
        # doesn't work properly with current background, edge backgrounds being drawn in
        anchor = round(display.scroll[0] * self.parallax[0] / self.size[0]), round(display.scroll[1] * self.parallax[1] / self.size[1])
        for x in range(anchor[0] - 1, anchor[0] + display.main.display_size[0] // self.size[0] + 1):
            for y in range(anchor[1] - 1, anchor[1] + display.main.display_size[1] // self.size[1] + 1):
                display.display.blit(self.image, ((x * self.size[0]) - int(display.scroll[0] * self.parallax[0]), (y * self.size[1]) - int(display.scroll[1] * self.parallax[1])))
                if self.main.debug_mode:
                    pg.draw.rect(display.display, self.debug_colour, pg.Rect((x * self.size[0]) - int(display.scroll[0] * self.parallax[0]),
                                                                             (y * self.size[1]) - int(display.scroll[1] * self.parallax[1]), self.size[0], self.size[1]), 1)
