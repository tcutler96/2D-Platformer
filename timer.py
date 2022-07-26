
class Timer:
    def __init__(self, main, interval, repeat, state):
        self.main = main
        self.triggered = False
        self.timer = 0
        self.interval = interval
        self.current_interval = interval
        self.repeat = repeat
        self.current_repeat = 0
        if state == 'current':
            self.states = [self.main.state_name]
        elif state == 'universal':
            self.states = list(self.main.state_dict.keys())
        else:
            self.states = state

    def update(self):
        self.triggered = False
        if self.main.state_name in self.states:
            self.timer += self.main.dt_s
            if self.timer >= self.current_interval:
                self.triggered = True
                self.current_interval += self.interval
                self.current_repeat += 1
