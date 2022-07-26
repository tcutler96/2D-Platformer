import pygame as pg
from game_object import GameObject


class Player(GameObject):
    # player sprite parameters: idle/ collision size (17, 30), head size ~(17, 17)
    # need to have consistent head/ body size and head/ cape/ sword colour
    def __init__(self, main, position, flip_h=False):
        super().__init__(main=main, name='Player', position=position, track_player_collision=False, flip_h=flip_h)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.collision_type = {'up': False, 'down': False, 'down_feet': False, 'left': False, 'right': False}
        self.velocity = [0, 0]
        self.added_velocity = [0, 0]
        self.walk_speed = 3
        self.grounded = False
        self.jump_speed = 5
        self.air_timer = 0
        self.jump_slack = int(self.main.fps / 10)
        self.jump_max_count = 2
        self.jump_counter = self.jump_max_count
        self.jump_timer = 0
        self.jump_max_duration = 15
        self.double_jump_delay = 5
        self.double_jump_timer = 0
        self.gravity = 1
        self.gravity_rising = 0.5
        self.max_fall_speed = 5
        self.dash_speed = 10
        self.dash_max_count = 1
        self.dash_counter = self.dash_max_count
        self.dash_timer = 0
        self.dash_max_duration = 10
        self.god_mode = False
        self.god_mode_faster = False

    def update_player(self, tile_rects, game_objects):
        if self.main.controls_handler.check_activity('god_mode'):
            self.god_mode = not self.god_mode
        self.added_velocity = [0, 0]
        if self.god_mode:
            if self.main.controls_handler.check_activity('god_mode_faster'):
                self.god_mode_faster = not self.god_mode_faster
            if self.main.controls_handler.check_activity('god_mode_flip_v'):
                self.flip_v = not self.flip_v
            if self.main.controls_handler.check_activity('god_mode_flip_h'):
                self.flip_h = not self.flip_h
            if self.main.controls_handler.check_activity('god_mode_up', 'held'):
                self.added_velocity[1] -= self.walk_speed + self.god_mode_faster * self.walk_speed
            if self.main.controls_handler.check_activity('god_mode_left', 'held'):
                self.added_velocity[0] -= self.walk_speed + self.god_mode_faster * self.walk_speed
            if self.main.controls_handler.check_activity('god_mode_down', 'held'):
                self.added_velocity[1] += self.walk_speed + self.god_mode_faster * self.walk_speed
            if self.main.controls_handler.check_activity('god_mode_right', 'held'):
                self.added_velocity[0] += self.walk_speed + self.god_mode_faster * self.walk_speed
            self.velocity = self.added_velocity
        else:
            # horizontal
            if self.main.controls_handler.check_activity('player_left', 'held'):
                self.added_velocity[0] -= self.walk_speed
            if self.main.controls_handler.check_activity('player_right', 'held'):
                self.added_velocity[0] += self.walk_speed
            self.velocity[0] = self.added_velocity[0]
            if self.grounded:
                if self.state == 'turning' and self.loops == 1:
                    self.change_state('leaning')
                if self.state == 'leaning' and self.loops == 1:
                    self.change_state('running')
                else:
                    if self.velocity[0] == 0:
                        # stop run, inside function check x and y velocity, if both zero (minus gravity) then set to idle
                        self.change_state('idle')
                    else:
                        self.start_run()
            if self.velocity[0] < 0:
                self.flip_h = True
            elif self.velocity[0] > 0:
                self.flip_h = False
            if self.state == 'running':
                # could just start sound, have it loop forever until specifically told to stop
                self.main.audio_handler.play_sound('player_run')
            else:
                self.main.audio_handler.stop_sound('player_run', 0.25)
            # vertical
            if self.main.controls_handler.check_activity('player_jump'):
                self.start_jump()
            if self.main.controls_handler.check_activity('player_dash'):
                self.start_dash()
            self.air_timer += int(self.main.dt)
            if self.grounded and self.air_timer > self.jump_slack + self.main.dt:
                # if in running state, call stop run function to at least stop running sound
                self.grounded = False
                self.change_state('falling')
            if self.state in ['jumping', 'doublejumping']:
                if self.state == 'doublejumping' and self.double_jump_timer < self.double_jump_delay:
                    self.main.state.particles_handler.add_particle(2, [self.pos_x, self.pos_x + self.sprite_width, 0], [self.pos_y + self.sprite_height - 5, self.pos_y + self.sprite_height + 5, 0],
                                                                   0, 0, 0, 0.05, [1, 5, 0], [0.05, 0.15, 0], 0, False, (194, 74, 112), 1, (255, 255, 255), None, True)
                    self.double_jump_timer += 1
                    self.added_velocity[1] += self.gravity
                    self.velocity[1] += self.added_velocity[1]
                else:
                    self.main.state.particles_handler.add_particle(2, [self.pos_x, self.pos_x + self.sprite_width, 0], self.pos_y + self.sprite_height,
                                                                   0, 0, 0, 0.05, [1, 5, 0], [0.15, 0.30, 0], 0, False, (20, 40, 60), 1, (255, 255, 255), None, True)
                    self.added_velocity[1] -= self.jump_speed
                    self.jump_timer += int(self.main.dt)
                    if self.jump_timer >= self.jump_max_duration:
                        self.stop_jump()
                    if self.main.controls_handler.check_activity('player_jump', 'unpressed'):
                        self.stop_jump(sharp=True)
                    self.velocity[1] = self.added_velocity[1]
            elif self.state == 'rising':
                self.added_velocity[1] += self.gravity_rising
                self.velocity[1] += self.added_velocity[1]
                if self.velocity[1] >= 0:
                    self.change_state('falling')
            elif self.state == 'dashing':
                self.main.state.particles_handler.add_particle(5, [[self.pos_x if not self.flip_h else self.pos_x + self.sprite_width][0], [self.pos_x + 10 if not self.flip_h else self.pos_x + self.sprite_width - 10][0], 0],
                                                               [self.pos_y, self.pos_y + self.sprite_height, 0], 0, 0, 0, 0.05, [1, 5, 0], [0.05, 0.15, 0], 0, False, (194, 74, 112), 1, (255, 255, 255), None, True)
                self.dash_timer += int(self.main.dt)
                self.air_timer += int(self.main.dt)
                if self.dash_timer >= self.dash_max_duration:
                    self.stop_dash()
                else:
                    if self.flip_h:
                        self.velocity[0] = -self.dash_speed
                    else:
                        self.velocity[0] = self.dash_speed
                    self.velocity[1] = self.added_velocity[1]
            else:
                self.added_velocity[1] += self.gravity
                self.velocity[1] += self.added_velocity[1]
            if self.velocity[1] > self.max_fall_speed:
                self.velocity[1] = self.max_fall_speed
        self.resolve_movement([[] if self.god_mode else tile_rects][0], game_objects)
        if self.god_mode:
            self.update_sprite()
        else:
            self.update()

    def resolve_movement(self, tile_rects, game_objects):
        self.collision_type = {'up': False, 'down': False, 'down_feet': False, 'left': False, 'right': False}
        velocity = self.velocity.copy()
        while velocity[0] < 0:
            velocity[0] += 1
            self.pos_x -= 1
            if self.collision_test_tiles(tile_rects):
                velocity[0] = 0
                self.pos_x += 1
                self.collision_type['left'] = True
        while velocity[0] > 0:
            velocity[0] -= 1
            self.pos_x += 1
            if self.collision_test_tiles(tile_rects):
                velocity[0] = 0
                self.pos_x -= 1
                self.collision_type['right'] = True
        while velocity[1] < 0:
            velocity[1] += 1
            self.pos_y -= 1
            if self.collision_test_tiles(tile_rects):
                velocity[1] = 0
                self.pos_y += 1
                self.collision_type['up'] = True
        while velocity[1] > 0:
            velocity[1] -= 1
            self.pos_y += 1
            if self.collision_test_tiles(tile_rects):
                velocity[1] = 0
                self.pos_y -= 1
                self.collision_type['down'] = True
        tile_collisions = self.collision_test_tiles(tile_rects)
        if tile_collisions:
            if tile_collisions['left']:
                self.pos_x -= 1
            elif tile_collisions['right']:
                self.pos_x += 1
            elif tile_collisions['top']:
                self.pos_y -= 1
            elif tile_collisions['bottom']:
                self.pos_y += 1
        if self.collision_type['left']:
            self.velocity[0] = 0
        if self.collision_type['right']:
            self.velocity[0] = 0
            self.main.state.particles_handler.add_particle(1, self.pos_x + self.main.state.display.scroll[0], self.pos_y + self.main.state.display.scroll[1], 0, 0, 0, 0, 1, 0.025, 0, False, (255, 0, 0), 1, (0, 255, 0))
        if self.collision_type['up']:
            self.velocity[1] = 0
            self.change_state('falling')
        if self.collision_type['down']:
            if not self.grounded:
                self.jump_counter = self.jump_max_count
                self.dash_counter = self.dash_max_count
                self.grounded = True
                # print(self.velocity[1], self.air_timer)
                # use current y downward velocity, time in air, time at max velocity to determine type of landing (hard, soft)
                # or use time since jump, which is reset with double jump
                # time since entered falling state, length of fall
                # have start fall function that starts fall counter...
                if self.velocity[1] > 3:
                    # have really hard landing if falling for more than ~5 seconds that enters fall recover/ crouch state that lasts ~1 second and accepts no user input until animation finished
                    # shake screen when hard landing
                    # have falling time determine particle parameters (amount, variation in movement)
                    # self.main.state.particles_handler.add_particle(self.air_timer * 5 // self.main.fps_base, [self.pos_x + self.collide_rect_pos1[0], self.pos_x + self.collide_rect_pos1[0] + self.collide_rect_width, 0],
                    #                                                self.pos_y + self.collide_rect_pos2[1], [-2, 2, 0], [-3, 0, 0], 0, 0.1, [1, 2, 0], [0.01, 0.025, 0], 0, False, (69, 128, 61), 1, (25, 25, 25), 'add', True)
                    if self.air_timer > 5 * self.main.fps_base:
                        pass
                    elif self.air_timer > 0.5 * self.main.fps_base:
                        self.main.audio_handler.play_sound('player_land')
                    else:
                        # play small landing sound and spawn less particles
                        pass
            self.velocity[1] = 0
            self.air_timer = 0
        self.collision_test_objects(game_objects)

    def collision_test_tiles(self, tile_rects):
        self.collide_rect = self.get_rect(True)
        tile_collisions = {}
        for tile_rect in tile_rects:
            if tile_rect.colliderect(self.collide_rect):
                tile_mask = pg.mask.from_surface(pg.Surface((tile_rect.w, tile_rect.h)))
                player_mask = pg.mask.from_surface(pg.Surface((self.collide_rect.w, self.collide_rect.h)))
                tile_collision_pos = tile_mask.overlap(player_mask, (self.collide_rect.x - tile_rect.x, self.collide_rect.y - tile_rect.y))
                tile_collisions['top'] = True if tile_collision_pos[1] < tile_rect.h / 5 else False
                tile_collisions['bottom'] = [True if tile_collision_pos[1] > 4 * tile_rect.h / 5 else False][0]
                tile_collisions['left'] = [True if tile_collision_pos[0] < tile_rect.w / 5 else False][0]
                tile_collisions['right'] = [True if tile_collision_pos[0] > 4 * tile_rect.w / 5 else False][0]
                return tile_collisions

    def collision_test_objects(self, game_objects):
        self.sprite_rect = self.get_rect()
        if game_objects:
            for game_object in game_objects:
                game_object_rect = game_object.collide_rect
                game_object.player_collision = False
                # game_object.player_collision_pos = None
                if game_object_rect.colliderect(self.sprite_rect):
                    game_object.player_collision = True
                    # game_object_collision_pos = game_object.sprite_mask.overlap(self.sprite_mask, (self.sprite_rect.x - game_object_rect.x, self.sprite_rect.y - game_object_rect.y))
                    # if game_object_collision_pos:
                    #     game_object.player_collision = True
                    #     game_object.player_collision_pos = game_object_collision_pos

    def start_run(self):
        # start running sound
        if self.state == 'idle':
            if (self.velocity[0] < 0) != self.flip_h:
                self.change_state('turning')
            else:
                self.change_state('leaning')
        elif self.state == 'falling':
            self.change_state('running')

    def stop_run(self):
        # we stop running, if no movement keys held, jump/ dash initiated, fall off edge
        # check x and y velocity, if both zero (minus gravity) then set to idle, else do nothing (ie let other functions handle changing state)
        # stop running sound
        # use grounded variable and x velocity to determine if player is moving along ground or not
        if self.state == 'running':
            self.state = 'idle'

    def start_jump(self):
        if self.state not in ['jumping', 'dashing']:
            if self.state == 'falling' and self.jump_counter == self.jump_max_count:
                self.jump_counter -= 1
            if self.jump_counter:
                self.jump_counter -= 1
                self.jump_timer = 0
                if self.jump_counter == self.jump_max_count - 1:
                    self.main.audio_handler.play_sound('player_jump')
                    self.change_state('jumping')
                else:
                    self.main.audio_handler.play_sound('player_double_jump', 0.25)
                    self.double_jump_timer = 0
                    self.change_state('doublejumping')
                    # self.main.state.particles_handler.add_particle(10, self.pos_x + self.sprite_width // 2, self.pos_y + self.sprite_height // 2, [-2, 2, 0], [0, 2, 0], 0, 0, 1, 0, 1, False, (194, 74, 112), 1, (25, 25, 25), 'add', True)
                self.grounded = False

    def stop_jump(self, sharp=False):
        if self.state in ['jumping', 'doublejumping']:
            self.change_state('rising')
            if sharp:
                self.added_velocity[1] /= 1.5
                if self.state == 'jumping':
                    self.main.audio_handler.stop_sound('player_jump', 0.25)
                else:
                    self.main.audio_handler.stop_sound('player_double_jump', 0.5)

    def start_dash(self):
        if self.dash_counter:
            self.dash_counter -= 1
            self.dash_timer = 0
            self.change_state('dashing')
            self.main.audio_handler.play_sound('player_dash', 0.1)
            self.grounded = False
            # self.main.state.particles_handler.add_particle(10, self.pos_x + self.sprite_width // 2, self.pos_y + self.sprite_height // 2, [-2, 2, 0], [0, 2, 0], 0, 0.1, 1, 0, 1, False, (194, 74, 112), 1, (25, 25, 25), 'add', True)

    def stop_dash(self):
        if self.state == 'dashing':
            self.change_state('falling')
