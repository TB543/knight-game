from map.Background import Background
from map.Scene import Scene
from characters.Character import Character


player = Character('../assets/samurai/player', .3, (10, 0), 10, 0, 0)
bg = Background('../assets/background/forest', [0, 0, .5, .6, .7, .7, .8, .9, .9, 1, 1, 1.1])
s = Scene(bg, player, [Character('../assets/castle/knight', .2, (10, 0), 10, 0, 0), Character('../assets/samurai/sensei', .3, (20, 0), 10, 0, 0), Character('../assets/forest/wizard', .3, (30, 0), 10, 0, 0), Character('../assets/dungeon/demon', .2, (40, 0), 10, 0, 0), Character('../assets/dungeon/skeleton', .2, (50, 0), 10, 0, 0), Character('../assets/castle/king', .2, (60, 0), 10, 0, 0)])

s.master.bind("<KeyRelease-space>", lambda event: player.key_binds(y='up off'))
s.master.bind("<space>", lambda event: player.key_binds(y='up on'))
s.master.bind("<KeyRelease-w>", lambda event: player.key_binds(y='up off'))
s.master.bind("<KeyPress-w>", lambda event: player.key_binds(y='up on'))
s.master.bind("<KeyPress-s>", lambda event: player.key_binds(y='down on'))
s.master.bind("<KeyRelease-s>", lambda event: player.key_binds(y='down off'))
s.master.bind("<KeyPress-a>", lambda event: player.key_binds(x='left on'))
s.master.bind("<KeyRelease-a>", lambda event: player.key_binds(x='left off'))
s.master.bind("<KeyPress-d>", lambda event: player.key_binds(x='right on'))
s.master.bind("<KeyRelease-d>", lambda event: player.key_binds(x='right off'))
s.master.bind("<Button-1>", lambda event: player.key_binds(attack_level=1))
s.master.bind("<Button-3>", lambda event: player.key_binds(attack_level=2))
s.master.bind("<Button-2>", lambda event: player.key_binds(attack_level=3))

s.start()
s.mainloop()
