# Combat Tank Pong (Refactored)

Released in 1977, “Combat” was one of nine games released with the Atari 2600 and is a 2D tank shooter developed and published by Atari.


<a href="https://github.com/JupiterIvy"><img src="https://user-images.githubusercontent.com/65917017/217365957-7e7c30db-d92e-4895-82bf-fad1a480860a.png" width="300px;" alt=""/></a>

# CONTRIBUTORS
<table>
<tr>
    <td align="center"><a href="https://github.com/JupiterIvy"><img src="https://media.licdn.com/dms/image/D4D03AQHt30NNq_kSvQ/profile-displayphoto-shrink_400_400/0/1670128148472?e=1677110400&v=beta&t=0qSqk2zVgjYNNHqF8_p3BtYed18SuSrGcR6_Obe7vIU" width="100px;" alt=""/><br /><sub><b>Evelyn Bessa</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/JuanCarloPaes"><img src="https://avatars.githubusercontent.com/u/46506431?v=4" width="100px;" alt=""/><br /><sub><b>Juan Paes</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/sweilos"><img src="https://avatars.githubusercontent.com/u/54459008?v=4" width="100px;" alt=""/><br /><sub><b>Yago Nunes</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/giseledesa"><img src="https://avatars.githubusercontent.com/u/120344151?v=4" width="100px;" alt=""/><br /><sub><b>Gisele de Sá</b></sub></a><br /></td>
    
</table>

## Goals

The objective of the game is to hit the opposing player's tank with as many shots as possible, so that one player has enough hit advantage over the other to win the match.

## Movements

The player can only move forwards to the direction it's facing, the angle can be changed using the other arrows.

There's two controllers the player can use to move the tank: using the Keyboard or a Gamepad

Arrows:

<a href="https://github.com/JupiterIvy"><img src="https://user-images.githubusercontent.com/65917017/217358011-bf3dd10f-7a01-491a-a5a1-62d48986e0f6.png" width="300px;" alt=""/></a>

Gamepad:

<table>
<td align="center"><a href="https://github.com/JupiterIvy"><img src="https://user-images.githubusercontent.com/65917017/217358573-2e8f43e6-a45e-4549-9ac0-f76d264c87e8.png" width="200px;" alt=""/></a></td>
<td align="center"><a href="https://github.com/JupiterIvy"><img src="https://user-images.githubusercontent.com/65917017/217361633-f6c0d823-5505-4c3e-9b70-b8d462bf657f.png" width="200px;" alt=""/></a></td>
</table>

## Shoot

In gamepads, the tank can shoot a bullet pressing 'x', while in keyboard it's the SpaceBar

<table>
<td align="center"><a href="https://github.com/JupiterIvy"><img src="https://user-images.githubusercontent.com/65917017/217363480-314367cb-f0b6-43f4-af56-cc957bc80b22.png" width="200px;" alt=""/></a></td>
<td align="center"><a href="https://github.com/JupiterIvy"><img src="https://user-images.githubusercontent.com/65917017/217364043-75eff46f-00cf-4a03-aaa4-635462afb4c5.png" width="200px;" alt=""/></a></td>
</table>

## Arena

This game contains two arenas, they can be changed in the line
```
## Game.py line 21
self.map = 2*SCREEN_RECTS
```
For arena 1, leave as it is (SCREEN_RECTS), while for arena 2, change the line to
```
## Game.py line 21
self.map = 2*SCREEN_RECTS_2
```

Enjoy.

