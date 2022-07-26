import pygame as pg


class ControlsHandler:
    # controller button index:name; 0:cross, 1:circle, 2:square, 3:triangle, 4:share, 5:ps, 6:options, 7:l3, 8:r3, 9:l1, 10:r1, 11:up, 12:down, 13:left, 14:right, 15:touch,
    # (axis buttons) -1:left_analogue_left, -2:left_analogue_right, -3:left_analogue_up, -4:left_analogue_down,
    # -5:right_analogue_left, -6:right_analogue_right, -7:right_analogue_up, -8:right_analogue_down, -9:l2, -10:r2
    def __init__(self, main):
        self.main = main
        self.path = 'Assets/Misc/ps4_button_icons.png'
        self.controls_settings = self.main.settings_handler.settings['Controls']
        self.controls_settings_default = self.main.settings_handler.settings_default['Controls']
        self.joysticks = {}
        self.joysticks_update = True
        self.main_joystick = 0
        self.invalid_keys = ['escape']
        self.analogue_dead_zone = 0.5
        self.trigger_dead_zone = -0.25
        self.controller_buttons = {'controller0': 'cross', 'controller1': 'circle', 'controller2': 'square', 'controller3': 'triangle', 'controller4': 'share', 'controller5': 'ps',
                                   'controller6': 'options', 'controller7': 'l3', 'controller8': 'r3', 'controller9': 'l1', 'controller10': 'r1', 'controller11': 'd_pad_up',
                                   'controller12': 'd_pad_down', 'controller13': 'd_pad_left', 'controller14': 'd_pad_right', 'controller15': 'touch', 'controller16': 'd_pad',
                                   'controller-1': 'left_stick_left', 'controller-2': 'left_stick_right', 'controller-3': 'left_stick_up', 'controller-4': 'left_stick_down',
                                   'controller-5': 'right_stick_left', 'controller-6': 'right_stick_right', 'controller-7': 'right_stick_up', 'controller-8': 'right_stick_down',
                                   'controller-9': 'l2', 'controller-10': 'r2', 'controller-11': 'left_stick', 'controller-12': 'right_stick'}
        self.colour = (255, 0, 0)
        self.get_button_icons()

    def get_button_icons(self):
        # can get keyboard icons as well if wanted
        button_icons = self.main.helper.load_image(self.path)
        button_icons_height = button_icons.get_height()
        x = -1
        for button in self.controller_buttons:
            start_x = x
            while True:
                x += 1
                if button_icons.get_at((x, 0))[0:-1] == self.colour:
                    button_icon = pg.Surface((x - start_x - 1, button_icons_height))
                    button_icon.blit(button_icons, (0, 0), (start_x + 1, 0, x - start_x - 1, button_icons_height))
                    button_icon.set_colorkey((0, 0, 0))
                    self.controller_buttons[button] = [self.controller_buttons[button], button_icon]
                    break

    def check_activity(self, activity, action='pressed'):
        action_list = self.main.events_handler.get_action_list(action)
        if activity in self.controls_settings:
            for input in self.controls_settings[activity]:
                if ' + ' in input:
                    inputs = input.split(' + ')
                    if set(inputs[:-1]).issubset(self.main.events_handler.get_action_list('held')) and inputs[-1] in self.main.events_handler.get_action_list('pressed'):
                        return True
                if input in action_list:
                    return True

    def change_control(self, activity, new_input, keyboard=True, convert_activity=True):
        control_loc = int(not keyboard)
        old_input = self.controls_settings[self.convert_activity_name(activity)][control_loc]
        invalid_keys = self.invalid_keys.copy()
        invalid_keys.append(old_input)
        if ('controller' in old_input) == ('controller' in new_input) and new_input not in invalid_keys:
            valid = True
        else:
            valid = False
        exists = []
        if valid:
            if convert_activity:
                activity = self.convert_activity_name(activity)
            for key in self.controls_settings:
                if new_input in self.controls_settings[key] and key.split('_')[0] == activity.split('_')[0]:
                    exists.append(key)
            if valid:
                self.controls_settings[activity][control_loc] = new_input
                if exists:
                    for activity in exists:
                        self.controls_settings[activity][control_loc] = old_input
        return valid, exists

    def convert_activity_name(self, name, to_menu=False):
        if to_menu:
            name = name.replace('_', ' ').title()
        else:
            name = name.lower().replace(' ', '_')
        return name

    def update_joysticks(self):
        if self.joysticks_update:
            self.joysticks = {}
            self.joysticks_update = False
            self.main_joystick = None
            joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
            for joystick in joysticks:
                self.joysticks[joystick.get_instance_id()] = joystick
            if joysticks:
                self.main_joystick = min(list(self.joysticks.keys()))

    def reset(self):
        self.joysticks_update = True

    def reset_settings(self, activities, keyboard=True):
        control_loc = int(not keyboard)
        activity_types = []
        for activity in activities:
            activity_type = self.convert_activity_name(activity).split('_')[0]
            if activity_type not in activity_types:
                activity_types.append(activity_type)
        for activity_type in activity_types:
            for activity in self.controls_settings:
                if activity_type in activity:
                    self.change_control(activity, self.controls_settings_default[activity][control_loc], keyboard, False)
