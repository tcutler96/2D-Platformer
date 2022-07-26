from timer import Timer


class TimerHandler:
    def __init__(self, main):
        self.main = main
        self.timers = {}

    def update(self):
        for timer_id in self.timers:
            timer = self.timers[timer_id]
            timer.update()

    def add_timer(self, interval, repeat=1, state='current'):
        timer_id = 0
        while timer_id in self.timers:
            timer_id += 1
        self.timers[timer_id] = Timer(self.main, interval, repeat, state)
        return timer_id

    def check_timer(self, timer_id):
        if timer_id in self.timers:
            timer = self.timers[timer_id]
            if timer.triggered:
                if timer.current_repeat == timer.repeat:
                    self.remove_timer(timer_id)
                return True
        return False

    def remove_timer(self, timer_id):
        if isinstance(timer_id, list):
            for t_id in timer_id:
                if t_id in self.timers:
                    self.timers.pop(t_id)
        else:
            if timer_id in self.timers:
                self.timers.pop(timer_id)
