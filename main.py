from m5stack import *
from m5ui import *
from uiflow import *

class Rect:
  color = 0xffffff
  def __init__(self, x, y, width, height, color):
    self.x = x;
    self.y = y;
    self.width = width
    self.height = height
    self.color = color
    
WHITE = 0xbbbbbb
GREEN = 0x00ffff
RED = 0xff0000
direction = 2
x = None
y = None
press = False
pause = False
run = True

def buttonA_wasPressed():
  global pause, press, x, y, run
  pause = not pause
  if not run:
    press = True
    run = True
  pass
btnA.wasPressed(buttonA_wasPressed)

def buttonB_wasPressed():
  global press, run
  press = True
  pass
btnB.wasPressed(buttonB_wasPressed)

imu0 = imu.IMU()
x = "%.3f"%float((imu0.ypr[1]))
y = "%.3f"%float((imu0.ypr[2]))
lcd.clear()
setScreenColor(0x000000)
axp.setLcdBrightness(75)
import math
import random
wait(1)

while run:
  press = False
  pause = False
  snake = [Rect(40,8,4,4, WHITE), Rect(40,12,4,4, WHITE), Rect(40,16,4,4, WHITE), Rect(40,20,4,4, WHITE), Rect(44,20,4,4, GREEN)]
  apple = Rect(random.randrange(0, 76, 4), random.randrange(0, 156, 4), 4, 4, RED)
  lcd.print("START", 20, 80, 0xffffff)
  wait(2)
  while run:
    lcd.clear()
    if not pause:
      rectangle = M5Rect(apple.x, apple.y, apple.width, apple.height, apple.color, apple.color)
      for block in snake:
        rectangle = M5Rect(block.x, block.y, block.width, block.height, block.color, block.color)
      
      if apple.x == block.x and apple.y == block.y:
        newTail = Rect(snake[0].x, snake[0].y, snake[0].width, snake[0].height, snake[0].color)
        if snake[0].x == snake[1].x:
          if snake[0].y > snake[1].y:
            newTail.y += 4
          else:
            newTail.y -= 4
        else:
          if snake[0].x > snake[1].x:
            newTail.x += 4
          else:
            newTail.x -= 4
        snake.insert(0, newTail)
        rectangle = M5Rect(snake[0].x, snake[0].y, snake[0].width, snake[0].height, snake[0].color, snake[0].color)
        foundSpot = False
        temp = apple
        while not foundSpot:
          foundSpot = True
          apple = Rect(random.randrange(0, 76, 4), random.randrange(0, 156, 4), 4, 4, RED)
          for block in snake:
            if apple.x == block.x and apple.y == block.y:
              foundSpot = False
          if apple.x == temp.x and apple.y == temp.y:
            foundSpot = False

      wait_ms(100)
      x = "%.3f"%float((imu0.ypr[1]))
      y = "%.3f"%float((imu0.ypr[2]))
      
      newBlock = Rect(block.x, block.y, block.width, block.height, GREEN)
      if float(x) >= 20 and not direction == 0:
        newBlock.y += 4
        direction = 2
      elif float(x) <= -20 and not direction == 2:
        newBlock.y -= 4
        direction = 0
      elif float(y) >= 20 and not direction == 3:
        newBlock.x += 4
        direction = 1
      elif float(y) <= -20 and not direction == 1:
        newBlock.x -= 4
        direction = 3
      else:
        if direction == 0:
          newBlock.y -= 4
        elif direction == 1:
          newBlock.x += 4
        elif direction == 2:
          newBlock.y += 4
        else:
          newBlock.x -= 4
          
      
      snake[len(snake)-1].color = WHITE
      rectangle = M5Rect(snake[len(snake)-1].x, snake[len(snake)-1].y, snake[len(snake)-1].width, snake[len(snake)-1].height, snake[len(snake)-1].color, snake[len(snake)-1].color)
      snake.append(newBlock)
      snake.pop(0)
      
      hit = False
      if newBlock.x < 0 or newBlock.x > 76 or newBlock.y < 0 or newBlock.y > 156:
        hit = True
      if not hit:
        for piece in snake:
          if not hit and not newBlock == piece:
            if newBlock.x == piece.x and newBlock.y == piece.y:
              hit = True
      if hit:
        run = False
    else:
      lcd.print("PAUSED", 10, 70, 0xffffff)
      wait_ms(250)
      lcd.clear()
  lcd.clear()
  lcd.print("GAME", 20, 40, 0xffffff)
  lcd.print("OVER", 20, 60, 0xffffff)
  lcd.print("Score: ", 5, 90, 0xffffff)
  lcd.print(len(snake)-5, 60, 90, 0xffffff)
  snake = []
  while not press:
    wait_ms(500)
  lcd.clear()
