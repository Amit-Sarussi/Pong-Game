import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode([1600, 900])
pygame.display.set_caption('Pong game')

playersWidth = 20
playersHeight = 130
playersOffset = 20

player1H = screen.get_height() / 2
player2H = screen.get_height() / 2
playerSpeed = 1.2

# Ball Properties
ballPos = [screen.get_width() / 2, screen.get_height() / 2]
ballVel = [0, 0]
ballSpeed = 0
acc = 0.002

# Game Properties
score = 0
fps = 165
phase = 0
winner = 0
running = True

# Movement
p1moveUP = False
p1moveDOWN = False
p2moveUP = False
p2moveDOWN = False


def startGame() -> None:
    global ballPos, ballVel, ballSpeed, player1H, player2H, score, phase

    # Reset Ball
    ballPos = [screen.get_width() / 2, screen.get_height() / 2]  # Centers the ball
    ballVel[0] = random.choice([random.randint(-98, -50), random.randint(50, 98)])
    ballSpeed = random.choice([random.randint(170, 180), random.randint(-180, -170)])
    while abs(ballVel[0]) >= abs(ballSpeed):
        ballSpeed = random.choice([random.randint(170, 180), random.randint(-180, -170)])

    ballVel[1] = random.choice([1, -1]) * (ballSpeed ** 2 - ballVel[0] ** 2) ** 0.5

    # Center players
    player1H = screen.get_height() / 2
    player2H = screen.get_height() / 2

    # Reset score & parameters
    score = 0
    phase = 1


def endGame(winPlayerNum: int) -> None:
    global phase, player1H, player2H, winner

    # Reset parameters
    phase = 0
    player1H = screen.get_height() / 2
    player2H = screen.get_height() / 2
    winner = winPlayerNum


def moveBall() -> None:
    global ballSpeed, ballVel, ballPos, acc

    # Calculate the velocity after the acceleration
    angle = math.atan(ballVel[0] / ballVel[1])
    ballVel = [math.sin(angle) * ballSpeed, math.cos(angle) * ballSpeed]
    if ballSpeed > 0:
        ballSpeed += acc
    else:
        ballSpeed -= acc

    # Move the ball
    ballPos[0] += ballVel[0] * 1 / fps
    ballPos[1] += ballVel[1] * 1 / fps


def checkCollision() -> None:
    global score, ballPos, ballVel, ballSpeed

    # Check for ceiling and floor
    if ballPos[1] > 900 - 10 or ballPos[1] < 10:
        ballVel[1] = -ballVel[1]
        ballSpeed = -ballSpeed

    # Check for collision in player walls (Losing / Winning):
    if ballPos[0] > 1600 - 10:
        endGame(1)  # player 2 lost
    if ballPos[0] < 10:
        endGame(2)  # player 1 lost

    # Check for collision of players:
    if playersWidth + playersOffset - 4 < ballPos[0] < playersWidth + playersOffset + 4:
        if player1H - playersHeight / 2 < ballPos[1] < player1H + playersHeight / 2:
            ballVel[0] = -ballVel[0]  # Turn the ball
            score += 1
    if screen.get_width() - playersWidth - playersOffset - 4 < \
            ballPos[0] < screen.get_width() - playersWidth - playersOffset + 4:
        if player2H - playersHeight / 2 < ballPos[1] < player2H + playersHeight / 2:
            ballVel[0] = -ballVel[0]  # Turn the ball
            score += 1


while running:
    if phase == 1:  # If in game

        # Moving The Players
        if p1moveUP and player1H >= 0 + playersHeight / 2:
            player1H -= playerSpeed
        if p1moveDOWN and player1H <= 900 - playersHeight / 2:
            player1H += playerSpeed
        if p2moveUP and player2H >= 0 + playersHeight / 2:
            player2H -= playerSpeed
        if p2moveDOWN and player2H <= 900 - playersHeight / 2:
            player2H += playerSpeed

        # Moving the ball
        checkCollision()
        moveBall()

    # Graphics:
    screen.fill((0, 0, 0))

    if phase == 1:  # If in game
        # Main ball
        pygame.draw.circle(screen, (255, 255, 255), ballPos, 20)

        # Dashed Center line
        lineSpace = 20
        for i in range(screen.get_height() // lineSpace):
            pygame.draw.line(screen, (255, 255, 255), (screen.get_width() / 2, i*lineSpace),
                             (screen.get_width() / 2, i*lineSpace+(lineSpace/2)), 3)

        # Score
        arcadeFont = pygame.font.Font('ARCADE.ttf', 50)
        pongScore = arcadeFont.render(f'Score: {score}', True, (255, 255, 255))
        pongScoreRect = pongScore.get_rect()
        pongScoreRect.center = (screen.get_width() // 2, 210)
        screen.blit(pongScore, pongScoreRect)

    # Player 1 and 2
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(
        playersOffset, player1H - (playersHeight / 2), playersWidth, playersHeight))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(
        screen.get_width() - playersWidth - playersOffset, player2H - (playersHeight / 2), playersWidth, playersHeight))

    # Title
    arcadeFont = pygame.font.Font('ARCADE.ttf', 140)
    pongTitle = arcadeFont.render('PONG', True, (255, 255, 255))
    pongTitleRect = pongTitle.get_rect()
    pongTitleRect.center = (screen.get_width() // 2, 140)
    screen.blit(pongTitle, pongTitleRect)

    if phase == 0:  # If not in game
        instFont = pygame.font.Font('ARCADE.TTF', 60)
        instTitle = instFont.render('Press SPACE to start', True, (255, 0, 0))
        instTitleRect = instTitle.get_rect()
        instTitleRect.center = (screen.get_width() // 2, screen.get_height() - 200)
        screen.blit(instTitle, instTitleRect)

        if winner != 0:
            winnerFont = pygame.font.Font('ARCADE.TTF', 70)
            if winner == 1:
                winnerTitle = winnerFont.render('Left Player Won', True, (0, 0, 255))
                winnerTitleRect = winnerTitle.get_rect()
                winnerTitleRect.center = (screen.get_width() // 2, 350)
                screen.blit(winnerTitle, winnerTitleRect)
            elif winner == 2:
                winnerTitle = winnerFont.render('Right Player Won', True, (0, 0, 255))
                winnerTitleRect = winnerTitle.get_rect()
                winnerTitleRect.center = (screen.get_width() // 2, 350)
                screen.blit(winnerTitle, winnerTitleRect)

    pygame.display.flip()

    # Input Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                p1moveUP = True
            if event.key == pygame.K_s:
                p1moveDOWN = True
            if event.key == pygame.K_UP:
                p2moveUP = True
            if event.key == pygame.K_DOWN:
                p2moveDOWN = True
            if event.key == pygame.K_SPACE and phase == 0:
                startGame()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                p1moveUP = False
            if event.key == pygame.K_s:
                p1moveDOWN = False
            if event.key == pygame.K_UP:
                p2moveUP = False
            if event.key == pygame.K_DOWN:
                p2moveDOWN = False

pygame.quit()
