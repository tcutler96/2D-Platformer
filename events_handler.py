import pygame as pg


class EventsHandler:
    def __init__(self, main):
        self.main = main
        self.keys_pressed = []
        self.keys_held = []
        self.keys_unpressed = []
        self.mouse_pos_window = (0, 0)
        self.mouse_pos = (0, 0)
        self.mouse_moved = False
        self.timer_data = {}
        self.timer_count = True

    def update(self):
        self.reset()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.main.change_state(state_name='Quit')
            if event.type == pg.KEYDOWN:
                input = pg.key.name(event.key)
                self.add_key(input)
                self.add_key(input, 'held')
            if event.type == pg.KEYUP:
                input = pg.key.name(event.key)
                self.add_key(input, 'unpressed')
                self.remove_key(input)
            if event.type == pg.MOUSEBUTTONDOWN:
                input = f'mouse{event.button}'
                self.add_key(input)
                self.add_key(input, 'held')
            if event.type == pg.MOUSEBUTTONUP:
                input = f'mouse{event.button}'
                self.add_key(input, 'unpressed')
                self.remove_key(input)
            if event.type == pg.MOUSEMOTION:
                self.mouse_pos_window = pg.mouse.get_pos()
                self.mouse_pos = (self.mouse_pos_window[0] / self.main.window.display_scale, self.mouse_pos_window[1] / self.main.window.display_scale)
                self.mouse_moved = True

            if event.type in [pg.JOYDEVICEADDED, pg.JOYDEVICEREMOVED]:
                self.main.controls_handler.update_joysticks()
            if event.type == pg.JOYBUTTONDOWN and event.instance_id == self.main.controls_handler.main_joystick:
                input = f'controller{event.button}'
                self.add_key(input)
                self.add_key(input, 'held')
            if event.type == pg.JOYBUTTONUP and event.instance_id == self.main.controls_handler.main_joystick:
                input = f'controller{event.button}'
                self.add_key(input, 'unpressed')
                self.remove_key(input)
            if event.type == pg.JOYAXISMOTION:
                if event.axis < 4:
                    if abs(event.value) > self.main.controls_handler.analogue_dead_zone:
                        if event.value < 0:
                            input = f'controller{-2 * event.axis - 1}'
                        else:
                            input = f'controller{-2 * event.axis - 2}'
                        if input not in self.keys_held:
                            self.add_key(input)
                            self.add_key(input, 'held')
                    else:
                        if event.value < 0:
                            input = f'controller{-2 * event.axis - 1}'
                        else:
                            input = f'controller{-2 * event.axis - 2}'
                        if input in self.keys_held:
                            self.add_key(input, 'unpressed')
                            self.remove_key(input)
                else:
                    if event.value > self.main.controls_handler.trigger_dead_zone:
                        input = f'controller{-event.axis - 5}'
                        if input not in self.keys_held:
                            self.add_key(input)
                            self.add_key(input, 'held')
                    else:
                        input = f'controller{-event.axis - 5}'
                        if input in self.keys_held:
                            self.add_key(input, 'unpressed')
                            self.remove_key(input)

            if pg.USEREVENT <= event.type < pg.NUMEVENTS:
                timer_id = event.type
                # this works but loses sync when moving between game states, need to make own timer handler using self.main.dt to increment timers ourselves
                # have option for timer to only be incremented when in same game state or universally...
                # have same functionality as we have here already
                if timer_id in self.timer_data and self.timer_data[timer_id][3] == self.main.state_name and self.timer_count:
                    self.timer_data[timer_id][0] = True
                    self.timer_data[timer_id][1] += 1

    def reset(self):
        self.keys_pressed = []
        self.keys_unpressed = []
        self.mouse_moved = False

    def add_key(self, input, action='pressed'):
        action_list = self.get_action_list(action)
        if input:
            if isinstance(input, list):
                for k in input:
                    if k not in action_list:
                        action_list.append(k)
            else:
                if input not in action_list:
                    action_list.append(input)

    def remove_key(self, input, action='held'):
        action_list = self.get_action_list(action)
        if input:
            if isinstance(input, list):
                for k in input:
                    if k in action_list:
                        action_list.remove(k)
            else:
                if input in action_list:
                    action_list.remove(input)

    def check_key(self, input, action='pressed'):
        action_list = self.get_action_list(action)
        if input:
            if isinstance(input, list) and set(input) & set(action_list):
                return True
            elif input in action_list:
                return True

    def get_action_list(self, action):
        if action == 'pressed':
            action_list = self.keys_pressed
        elif action == 'held':
            action_list = self.keys_held
        elif action == 'unpressed':
            action_list = self.keys_unpressed
        else:
            action_list = []
        return action_list
