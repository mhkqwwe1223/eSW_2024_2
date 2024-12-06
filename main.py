import time
import random
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw

# 버튼 설정
BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 게임 설정
width, height = 128, 64
player_pos = [20, height - 10]
player_jump = False
obstacles = [[width, height - 10]]

# 화면 설정
my_image = Image.new("1", (width, height))
my_draw = ImageDraw.Draw(my_image)

def draw_player():
    my_draw.rectangle([player_pos[0], player_pos[1], player_pos[0] + 10, player_pos[1] + 10], fill=255)

def draw_obstacles():
    global obstacles
    for obs in obstacles:
        my_draw.rectangle([obs[0], obs[1], obs[0] + 10, obs[1] + 10], fill=255)

def move_obstacles():
    global obstacles
    for obs in obstacles:
        obs[0] -= 2
    obstacles = [obs for obs in obstacles if obs[0] > 0]
    if random.random() < 0.01:  # 새로운 장애물 생성 확률
        obstacles.append([width, height - 10])

def check_collision():
    global player_pos, obstacles
    for obs in obstacles:
        if player_pos[0] < obs[0] + 10 and player_pos[0] + 10 > obs[0] and player_pos[1] < obs[1] + 10 and player_pos[1] + 10 > obs[1]:
            return True
    return False

def main():
    global player_pos, player_jump, obstacles

    while True:
        my_draw.rectangle([0, 0, width, height], fill=0)  # 배경 초기화

        # 점프 처리
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            if not player_jump:
                player_pos[1] -= 20
                player_jump = True

        if player_pos[1] < height - 10:
            player_pos[1] += 2  # 떨어지는 속도
        else:
            player_jump = False

        # 장애물 이동 및 충돌 확인
        move_obstacles()
        if check_collision():
            print("Game Over!")
            break

        # 화면에 그리기
        draw_player()
        draw_obstacles()

        # 디스플레이 갱신
        my_image.show()
        time.sleep(0.1)

if __name__ == "__main__":
    main()
