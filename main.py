from livewires import games, color
import random
import math

games.init(screen_width=640, screen_height=480, fps=50)

class Lazer(games.Sprite):
    image = games.load_image('img/lazer.png')

    BUFFER = 40
    VELOCITY_FACTOR = 7
    LIFETIME = 20

    def __init__(self, ship_x, ship_y, ship_angle):

        angle = ship_angle * math.pi / 180

        buffer_x = Lazer.BUFFER * math.sin(angle)
        buffer_y = Lazer.BUFFER * -math.cos(angle)
        x = ship_x + buffer_x
        y = ship_y + buffer_y

        dx = Lazer.VELOCITY_FACTOR * math.sin(angle)
        dy = Lazer.VELOCITY_FACTOR * -math.cos(angle)

        super(Lazer, self).__init__(image=Lazer.image,
                                      x=x, y=y,
                                      dx=dx, dy=dy)
        self.lifetime = Lazer.LIFETIME

        self.score = games.Text(value=0,
                                size=35,
                                color=color.white,
                                top=5,
                                right=games.screen.width - 10)

        games.screen.add(self.score)

    def update(self):

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.destroy()


        self.lifetime -=1
        if self.lifetime == 0:
            self.destroy()

        self.check_catch()

    def check_catch(self):
        for cheese in self.overlapping_sprites:
            cheese.die()
            self.score.value +=1



class Robot(games.Sprite):
    image = games.load_image('img/robot.png')

    lazer_d = 25

    def __init__(self, game, x, y):
        super(Robot, self).__init__(image=Robot.image, x=x, y=y)
        self.game = game
        self.lazer_wait = 0

    def update(self):
        if self.lazer_wait > 0:
            self.lazer_wait -=1

        if games.keyboard.is_pressed(games.K_w):
            self.y -= 1
        if games.keyboard.is_pressed(games.K_s):
            self.y += 1
        if games.keyboard.is_pressed(games.K_a):
            self.x -= 1
        if games.keyboard.is_pressed(games.K_d):
            self.x += 1

        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += 1
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= 1

        if games.keyboard.is_pressed(games.K_1):
            self.angle = 0
        if games.keyboard.is_pressed(games.K_2):
            self.angle = 90
        if games.keyboard.is_pressed(games.K_3):
            self.angle = 180
        if games.keyboard.is_pressed(games.K_4):
            self.angle = 270

        self.check_collision()

        if self.top > games.screen.height:
            self.bottom = 0
        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width
        if games.keyboard.is_pressed(games.K_SPACE) and self.lazer_wait==0:
            new_lazer = Lazer(self.x, self.y, self.angle)
            games.screen.add(new_lazer)
            self.lazer_wait = Robot.lazer_d

    def check_collision(self):
        for i in self.overlapping_sprites:
            i.collision()
            self.destroy()
            self.end_game()
            self.stop()

    @staticmethod
    def end_game():
        end_msg = games.Message(value='Вы проиграли!',
                                size=40,
                                color=color.blue,
                                x=games.screen.width / 2,
                                y=games.screen.height / 2,
                                lifetime= 3 * games.screen.fps,
                                after_death=games.screen.quit)

        games.screen.add(end_msg)

class Virus(games.Sprite):

    SMALL = 1
    LARGE = 2
    images = {SMALL: games.load_image('img/virus.png'),
              LARGE: games.load_image('img/virus_large.png')}

    SPEED = 2
    SPAWN = 2

    def __init__(self, x, y, size):
        super(Virus, self).__init__(
            image=Virus.images[size],
            x=x, y=y,
            dx=random.choice([1,-1]) * Virus.SPEED * random.random() / size,
            dy=random.choice([1, -1]) * Virus.SPEED * random.random() / size
        )
        self.size = size

    def die(self):
        if self.size != Virus.SMALL:
            for i in range(Virus.SPAWN):
                new_virus = Virus(x=self.x, y=self.y, size=self.size-1)
                games.screen.add(new_virus)
        self.destroy()

    def update(self):
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        if self.bottom < 0 or self.top > games.screen.height:
            self.dy = -self.dy


class Game():
    def __init__(self):
        games.music.load('music/whatislove.mp3')
        games.music.play(-1)

        self.robot = Robot(game=self,
                         x=games.screen.width / 2,
                         y=games.screen.height)
        games.screen.add(self.robot)

    def play(self):
        stomach_image = games.load_image('img/stomach.jpg', transparent=False)
        games.screen.background = stomach_image

        for i in range(8):
            x = random.randrange(games.screen.width)
            y = random.randrange(games.screen.height)
            size = random.choice([Virus.SMALL, Virus.LARGE])
            new_virus = Virus(x=x, y=y, size=size)
            games.screen.add(new_virus)


        games.screen.mainloop()

def main():
    robot_vs_viruses = Game()
    robot_vs_viruses.play()


if __name__ == '__main__':
    main()