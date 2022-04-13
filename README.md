# Racing SIM 9000

## Plan

Make a simple car game where you dodge the obstacles.

| Version | Changes                                                                                                                                                                        |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1       | Set up basic functionally for displaying the vehicle and been able to move it and displaying the obstacle. I also setup basic game logic such as pregame, game, end and reset. |
| 2       | Added basic obstacle generation and making it fall down the screen towards to the vehicle. I added a road background as well.                                                  |
| 3       | Added basic collision detection based on rectangles. Made the full game logic work but not perfect. Added a basic score system that counts the amount of obstacles pasted.     |
| 4       | Created a more advanced collision detection using meshes. This means there is pixel prefect collision detection.                                                               |
| 5       | I made the road loop forever.                                                                                                                                                  |
| 6       | Added more cars and obstacles.                                                                                                                                                 |

## Problems

- Sometimes it is imposable to survive.

# Testing

## Pixel Perfect collision detection

![img](https://i.imgur.com/Wp7JAYN.png)

I Made sure the collisions are determined by the mask and not a rectangle. I tested it all [here](https://youtu.be/7_uHLqEpxuE).

## Obstacles don't overlap

![img](https://i.imgur.com/Vkr1zHn.png)

![img](https://i.imgur.com/LvUpjjn.png)

Made sure the obstacles don't overlap

## High score

![img](https://i.imgur.com/wRMdu4x.png)

High score system that is loaded form a file so it saves even when the game is closed and opened again.

![img](https://i.imgur.com/mmE4A24.png)

## More testing

| Test                           | Expected                           | Correct | Notes                                                           |
| ------------------------------ | ---------------------------------- | ------- | --------------------------------------------------------------- |
| Left arrow key and a key       | car moves left                     | yes     |                                                                 |
| Right arrow key and d key      | car moves right                    | yes     |                                                                 |
| Up arrow key and w key         | car moves up                       | yes     |                                                                 |
| Down arrow key and s key       | car moves down                     | yes     |                                                                 |
| Pressing esc                   | game quits                         | yes     |                                                                 |
| Car hits left side of screen   | car stops moving                   | yes     |                                                                 |
| Car hits right side of screen  | car stops moving                   | yes     |                                                                 |
| Car hits top side of screen    | car stops moving                   | yes     |                                                                 |
| Car hits bottom side of screen | car stops moving                   | yes     |                                                                 |
| Obstacle generation            | obstacle generates                 | yes     |                                                                 |
| Obstacle over lap              | Obstacles overlap sometimes        | no      | Added a check function. ![img](https://i.imgur.com/MkJAzT2.png) |
| Obstacle collision             | game stop when hit obstacle        | yes     |                                                                 |
| High score                     | high score saved to file           | yes     |                                                                 |
| Car speed                      | car speed increases every 5 points | yes     |                                                                 |
