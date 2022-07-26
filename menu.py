from menu_button import MenuButton
import pygame as pg
import random
from background_image import BackgroundImage


class Menu:
    # menu data format: [Title (string), Title Type ('image', 'small', 'big', None)], [{Button Index (int): [Name (string), Options ([strings]), Current Option (int),
    # Default Option (int), Wrap Options (bool)}, Initial Button (int), Back Option (bool), Escape Option (bool)], Background (class/ None)
    def __init__(self, main, title_data, button_data, reset_background):
        self.main = main
        self.title_data = title_data
        if self.title_data[1] == 'image':
            self.title_image = self.main.helper.outline_image(self.title_data[0], outline_size=2, outline_colour=self.main.window.menu_colour_2)
            self.title_size = 1
            self.title_increase = True
            self.title_pos = 10
        elif self.title_data[1] == 'small':
            self.title_pos = 120
            self.title_scale = 1
            self.title_spacing = 3
            self.fleur_image = self.main.helper.outline_image('Assets/Misc/menu_fleur_small.png', outline_colour=self.main.window.menu_colour_2)
            self.fleur_pos = 135
        elif self.title_data[1] == 'big':
            self.title_pos = 75
            self.title_scale = 3
            self.title_spacing = 2
            self.fleur_image = self.main.helper.outline_image('Assets/Misc/menu_fleur_big.png', outline_size=2, outline_colour=self.main.window.menu_colour_2)
            self.fleur_pos = 120
        self.button_pos = 150
        self.debug_colour = (143, 188, 143)
        self.button_data = button_data[0]
        self.button_scale = 1
        self.button_spacing = 2
        self.button_height = self.main.font.font_image_height * self.button_scale
        self.button_gap = 6
        self.max_buttons = int((self.main.display_size[1] - self.button_pos) / (self.button_height + self.button_gap)) - 2
        self.default_button = button_data[1]
        self.buttons = self.create_buttons(button_data[2])
        self.escape = button_data[3]
        self.accept_user_input = False
        self.input_delay = self.main.fps // 4
        self.input_timer = 1
        self.button_selected = 0
        self.button_triggered = False
        self.button_collided = -1
        self.option_changed = False
        self.option_delay = 0.2
        self.option_timer = 0
        self.options_reset = False
        self.menu_keys = ['up', 'down', 'left', 'right', 'return', 'escape']
        self.menu_movement = [False, False, False, False]
        self.reset_background = reset_background

    def create_buttons(self, back):
        reset = False
        longest_name = 0
        longest_option = 0
        for button_index in self.button_data:
            button_data = self.button_data[button_index]
            if button_data[1]:
                reset = True
                longest_name = max(longest_name, self.main.font.get_width(button_data[0], self.button_spacing))
                longest_option = max(longest_option, self.main.font.get_width(max(button_data[1], key=len), self.button_spacing))
                if len(button_data[1]) == 1:
                    button_type = 'input'
                else:
                    button_type = 'scroll'
            else:
                button_type = 'simple'
            button_data.append(button_type)
        if reset:
            self.button_data[len(self.button_data)] = ['Reset to Defaults', None, 0, 0, False, 'simple']
        if back:
            self.button_data[len(self.button_data)] = ['Back', None, 0, 0, False, 'simple']
        buttons = []
        for button_index in self.button_data:
            button_data = self.button_data[button_index]
            if button_data[5] in ['input', 'scroll']:
                if button_index == 0:
                    left = '> ' + str(button_data[0]) + ':'
                    right = button_data[1][button_data[2]] + ' <'
                else:
                    left = '  ' + str(button_data[0]) + ':'
                    right = button_data[1][button_data[2]] + '  '
                text = [left, right]
                width = max(longest_name + longest_option + 50, int(self.main.display_size[0] * 0.35))
            else:
                if button_index == 0:
                    text = '> ' + button_data[0] + ' <'
                else:
                    text = '  ' + button_data[0] + '  '
                width = (self.main.font.get_width(text, self.button_spacing) - self.button_spacing) * self.button_scale
            if button_data[0] == 'Reset to Defaults':
                self.button_pos = 150 + (self.button_height + self.button_gap) * (self.max_buttons - 1)
            elif button_data[0] == 'Back':
                self.button_pos = 150 + (self.button_height + self.button_gap) * self.max_buttons
            buttons.append(MenuButton(self.main, button_data[5], text, (self.main.display_size[0] / 2, self.button_pos), self.main.window.menu_colour_1, self.main.window.menu_colour_2,
                                      self.button_scale, self.button_spacing, width, self.button_height, self.debug_colour))
            self.button_pos += self.button_height + self.button_gap
        return buttons

    def draw(self, display):
        if self.title_data[1] == 'image':
            display.display.blit(self.title_image, ((self.main.display_size[0] - self.title_image.get_size()[0]) / 2, self.title_pos))
        elif self.title_data[1] in ['small', 'big']:
            if self.title_data[0]:
                self.main.font.draw(display.display, self.title_data[0], (self.main.display_size[0] / 2, self.title_pos), self.main.window.menu_colour_1,
                                    self.main.window.menu_colour_2, self.title_scale, self.title_spacing, 'shadow', self.title_scale, 'centre')
            display.display.blit(self.fleur_image, ((self.main.display_size[0] - self.fleur_image.get_width()) / 2, self.fleur_pos))
        if self.buttons:
            for index, button_data in enumerate(self.buttons):
                button_data.draw(display, index == self.button_selected)

    def update(self):
        if not self.accept_user_input:
            if self.main.events_handler.mouse_moved or self.main.events_handler.check_key(['mouse1', 'mouse3'], 'pressed'):
                self.button_collided = -1
                for index, button in enumerate(self.buttons):
                    button.update()
                    if button.collide:
                        self.button_collided = index
                        self.change_button(mouse=True)
                        break
                if self.main.state.display.mouse:
                    if self.main.controls_handler.check_activity('menu_select_mouse'):
                        if self.button_collided > -1:
                            self.trigger_button(mouse=True)
                    if self.main.controls_handler.check_activity('menu_back_mouse'):
                        if self.button_collided > -1:
                            self.trigger_button(mouse=True, positive=False)
                        elif self.escape:
                            self.back()
                            self.main.state.particles_handler.add_particle(10, [self.main.events_handler.mouse_pos[0] - 10, self.main.events_handler.mouse_pos[0] + 10, 0],
                                                                           [self.main.events_handler.mouse_pos[1] - 10, self.main.events_handler.mouse_pos[1] + 10, 0],
                                                                           [-0.5, 0.5, 0], [-0.5, 0.5, 0], 0, 0, [1, 3, 1], [0, 0.05, 0], 1, False, self.main.window.menu_colour_1, 1, self.main.window.menu_colour_2)
                else:
                    self.main.state.display.mouse = True
            if self.main.controls_handler.check_activity('menu_back') and self.escape:
                self.back()
            if self.main.controls_handler.check_activity('menu_select'):
                self.trigger_button(mouse=False)
            if self.main.controls_handler.check_activity('menu_up'):
                self.menu_movement[0] = True
            elif self.main.controls_handler.check_activity('menu_up', 'unpressed'):
                self.menu_movement[0] = False
                self.option_timer = 0
            if self.main.controls_handler.check_activity('menu_down'):
                self.menu_movement[1] = True
            elif self.main.controls_handler.check_activity('menu_down', 'unpressed'):
                self.menu_movement[1] = False
                self.option_timer = 0
            if self.main.controls_handler.check_activity('menu_left'):
                self.menu_movement[2] = True
            elif self.main.controls_handler.check_activity('menu_left', 'unpressed'):
                self.menu_movement[2] = False
                self.option_timer = 0
            if self.main.controls_handler.check_activity('menu_right'):
                self.menu_movement[3] = True
            elif self.main.controls_handler.check_activity('menu_right', 'unpressed'):
                self.menu_movement[3] = False
                self.option_timer = 0
            if self.menu_movement[0] and not self.menu_movement[1]:
                self.change_button(mouse=False, positive=False)
            elif self.menu_movement[1] and not self.menu_movement[0]:
                self.change_button(mouse=False, positive=True)
            elif self.menu_movement[2] and not self.menu_movement[3]:
                self.change_option(mouse=False, positive=False)
            elif self.menu_movement[3] and not self.menu_movement[2]:
                self.change_option(mouse=False, positive=True)
        else:
            self.input_timer -= 1
            if self.input_timer == 0:
                self.input_timer = self.input_delay
                if self.buttons[self.button_selected].text[1] == '  <':
                    self.buttons[self.button_selected].text[1] = '_ <'
                else:
                    self.buttons[self.button_selected].text[1] = '  <'
                    self.main.state.particles_handler.add_particle(2, [self.buttons[self.button_selected].pos_x - self.buttons[self.button_selected].width / 3,
                                                                       self.buttons[self.button_selected].pos_x + self.buttons[self.button_selected].width / 3, 0],
                                                                   [self.buttons[self.button_selected].pos_y, self.buttons[self.button_selected].pos_y + self.buttons[self.button_selected].height, 0],
                                                                   [-0.5, 0.5, 0], [-0.5, 0.5, 0], 0, 0, [1, 3, 1], [0, 0.05, 0], 1, False, self.main.window.menu_colour_1, 1, self.main.window.menu_colour_2)
            if self.main.events_handler.keys_pressed:
                self.accept_user_input = False
                self.main.audio_handler.play_sound('menu_option_click')
                key = self.main.events_handler.keys_pressed[0]
                old_key = self.button_data[self.button_selected][1][0]
                valid, exists = self.main.controls_handler.change_control(self.button_data[self.button_selected][0], key, 'controller' not in old_key, True)
                if valid:
                    self.option_changed = True
                    for activity in exists:
                        for button_index in self.button_data:
                            button_data = self.button_data[button_index]
                            if button_data[0] == self.main.controls_handler.convert_activity_name(activity, True):
                                button_data[1][0] = old_key
                                self.buttons[button_index].text[1] = old_key + '  '
                    self.button_data[self.button_selected][1][0] = key
                    self.main.state.particles_handler.add_particle(10, [self.buttons[self.button_selected].pos_x - self.buttons[self.button_selected].width / 3,
                                                                        self.buttons[self.button_selected].pos_x + self.buttons[self.button_selected].width / 3, 0],
                                                                   [self.buttons[self.button_selected].pos_y, self.buttons[self.button_selected].pos_y + self.buttons[self.button_selected].height, 0],
                                                                   [-0.5, 0.5, 0], [-0.5, 0.5, 0], 0, 0, [1, 3, 1], [0, 0.05, 0], 1, False, self.main.window.menu_colour_1, 1, self.main.window.menu_colour_2)
                self.buttons[self.button_selected].text[1] = self.button_data[self.button_selected][1][0] + ' <'
        if random.uniform(0, 1) > 0.5:
            self.main.state.particles_handler.add_particle(1, [-50, self.main.display_size[0] + 50, 1], self.main.display_size[1] + 25, [-0.25, 0.25, 0], [-0.5, 0, 0], [-0.0005, 0.0005, 0], [-0.01, 0, 0], [2, 8, 1],
                                                           [0.01, 0.055, 0], 5, True, self.main.window.menu_colour_1, 1, self.main.window.menu_colour_2)

    def trigger_button(self, mouse=True, positive=True):
        if len(self.buttons):
            if self.button_data[self.button_selected][5] == 'simple' and positive:
                self.main.audio_handler.play_sound('menu_button_click')
                if self.button_data[self.button_selected][0] == 'Reset to Defaults':
                    self.reset_options()
                elif self.button_data[self.button_selected][0] == 'Back':
                    self.back(sound=False)
                else:
                    self.button_triggered = True
            elif self.button_data[self.button_selected][5] == 'input' and positive:
                self.main.audio_handler.play_sound('menu_option_click')
                self.accept_user_input = True
                self.main.state.display.mouse = False
                self.main.state.particles_handler.add_particle(10, [self.buttons[self.button_selected].pos_x - self.buttons[self.button_selected].width / 3,
                                                                    self.buttons[self.button_selected].pos_x + self.buttons[self.button_selected].width / 3, 0],
                                                               [self.buttons[self.button_selected].pos_y, self.buttons[self.button_selected].pos_y + self.buttons[self.button_selected].height, 0],
                                                               [-0.5, 0.5, 0], [-0.5, 0.5, 0], 0, 0, [1, 3, 1], [0, 0.05, 0], 1, False, self.main.window.menu_colour_1, 1, self.main.window.menu_colour_2)
            elif mouse:
                self.change_option(mouse, positive)

    def back(self, sound=True):
        if sound:
            self.main.audio_handler.play_sound('menu_button_click')
        self.main.exit_state_number = 1

    def change_button(self, mouse=True, positive=True, reset=False):
        if len(self.buttons):
            if reset:
                new_button = self.default_button
            else:
                if mouse:
                    new_button = self.button_collided
                else:
                    new_button = self.button_selected
                    self.main.state.display.mouse = False
                    if self.option_timer <= 0:
                        self.option_timer = self.option_delay * self.main.fps
                        if positive:
                            new_button += 1
                            if new_button > len(self.button_data) - 1:
                                new_button = 0
                        else:
                            new_button -= 1
                            if new_button < 0:
                                new_button = len(self.button_data) - 1
                    else:
                        self.option_timer -= self.main.dt
            if new_button != self.button_selected:
                if not reset:
                    self.main.audio_handler.play_sound('menu_button_change')
                if self.button_data[self.button_selected][5] == 'simple':
                    self.buttons[self.button_selected].text = ' ' + self.buttons[self.button_selected].text[1:-1] + ' '
                elif self.button_data[self.button_selected][5] in ['scroll', 'input']:
                    self.buttons[self.button_selected].text = [' ' + self.buttons[self.button_selected].text[0][1:], self.buttons[self.button_selected].text[1][:-1] + ' ']
                self.button_selected = new_button
                if self.button_data[self.button_selected][5] == 'simple':
                    self.buttons[self.button_selected].text = '>' + self.buttons[self.button_selected].text[1:-1] + '<'
                elif self.button_data[self.button_selected][5] in ['scroll', 'input']:
                    self.buttons[self.button_selected].text = ['>' + self.buttons[self.button_selected].text[0][1:], self.buttons[self.button_selected].text[1][:-1] + '<']
                self.main.state.particles_handler.add_particle(5, [self.buttons[self.button_selected].pos_x - self.buttons[self.button_selected].width / 3,
                                                                   self.buttons[self.button_selected].pos_x + self.buttons[self.button_selected].width / 3, 0],
                                                               [self.buttons[self.button_selected].pos_y, self.buttons[self.button_selected].pos_y + self.buttons[self.button_selected].height, 0],
                                                               [-0.5, 0.5, 0], [-0.5, 0.5, 0], 0, 0, [1, 3, 1], [0, 0.05, 0], 1, False, self.main.window.menu_colour_1, 1, self.main.window.menu_colour_2)

    def change_option(self, mouse, positive=True):
        if len(self.buttons):
            if self.button_data[self.button_selected][5] == 'scroll':
                new_option = self.button_data[self.button_selected][2]
                if not mouse:
                    self.main.state.display.mouse = False
                if self.option_timer <= 0 or mouse:
                    self.option_timer = self.option_delay * self.main.fps
                    if positive:
                        new_option += 1
                        if new_option > len(self.button_data[self.button_selected][1]) - 1:
                            if self.button_data[self.button_selected][4]:
                                new_option = 0
                            else:
                                new_option = len(self.button_data[self.button_selected][1]) - 1
                    else:
                        new_option -= 1
                        if new_option < 0:
                            if self.button_data[self.button_selected][4]:
                                new_option = len(self.button_data[self.button_selected][1]) - 1
                            else:
                                new_option = 0
                else:
                    self.option_timer -= self.main.dt
                if new_option != self.button_data[self.button_selected][2]:
                    self.main.audio_handler.play_sound('menu_option_click')
                    self.option_changed = True
                    self.button_data[self.button_selected][2] = new_option
                    self.buttons[self.button_selected].text[1] = self.button_data[self.button_selected][1][self.button_data[self.button_selected][2]] + ' <'
                    self.main.state.particles_handler.add_particle(10, [self.buttons[self.button_selected].pos_x - self.buttons[self.button_selected].width / 3,
                                                                        self.buttons[self.button_selected].pos_x + self.buttons[self.button_selected].width / 3, 0],
                                                                   [self.buttons[self.button_selected].pos_y, self.buttons[self.button_selected].pos_y + self.buttons[self.button_selected].height, 0],
                                                                   [-0.5, 0.5, 0], [-0.5, 0.5, 0], 0, 0, [1, 3, 1], [0, 0.05, 0], 1, False, self.main.window.menu_colour_1, 1, self.main.window.menu_colour_2)

    def reset_options(self):
        for button_index in self.button_data:
            button_data = self.button_data[button_index]
            if button_data[5] in ['scroll', 'input'] and button_data[1][button_data[2]] != button_data[3]:
                print(button_data)
                self.options_reset = True
                if button_data[3] not in button_data[1]:
                    button_data[1] = [button_data[3]]
                button_data[2] = button_data[1].index(button_data[3])
                self.buttons[button_index].text[1] = button_data[3] + '  '
                self.main.state.particles_handler.add_particle(10, [self.buttons[button_index].pos_x - self.buttons[button_index].width / 3,
                                                                    self.buttons[button_index].pos_x + self.buttons[button_index].width / 3, 0],
                                                               [self.buttons[button_index].pos_y, self.buttons[button_index].pos_y + self.buttons[button_index].height, 0],
                                                               [-0.5, 0.5, 0], [-0.5, 0.5, 0], 0, 0, [1, 3, 1], [0, 0.05, 0], 1, False, self.main.window.menu_colour_1, 1, self.main.window.menu_colour_2)

    def reset(self, enter=False):
        self.main.state.display.mouse = False
        self.menu_movement = [False, False, False, False]
        if enter:
            self.change_button(reset=True)
            if self.reset_background:
                if self.main.state_dict[self.main.state_order[-2]].menu:
                    self.main.state.background = self.main.state_dict[self.main.state_order[-2]].background
                    self.main.state.particles_handler = self.main.state_dict[self.main.state_order[-2]].particles_handler
                else:
                    self.main.state.background.images_bg = [self.main.state_dict[self.main.state_order[-2]].background.images_bg[0]]
                    self.main.state.background.images_bg = [BackgroundImage(self.main, pg.transform.smoothscale(pg.transform.smoothscale(
                        self.main.state_dict[self.main.state_order[-2]].display.display, (int(self.main.display_size[0] / 2), int(self.main.display_size[1] / 2))), self.main.display_size))]
