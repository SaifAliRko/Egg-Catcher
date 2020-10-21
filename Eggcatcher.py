from itertools import cycle
from random import randrange # for random selection of things
from tkinter import Tk , Canvas , messagebox , font  # messagebox displays messages


# if you get confuse see the Tkinter coordinate system pic in the same folder




# we require more eggs moving on our game and thats why width will be greater
canvas_width = 800
canvas_height = 400


# now need to create a window
win = Tk()
#creating canvas
c = Canvas(win , width = canvas_width ,  height = canvas_height , background = 'deep sky blue')
# creating green thing below
c.create_rectangle(-5, canvas_height - 100 , canvas_width + 5 , canvas_height + 5 , fill='sea green', width=0)
# creating the sun now part of it should be invisible thats why we will have first two coordinates negative
c.create_oval(-80,-80,120,120,fill='orange' , width=0)
# packing all figures created
c.pack()
# moving a cycle to pick an entity from the list
color_cycle = cycle(['light blue' , 'light pink' , 'light yellow','light green' , 'red', 'blue' , 'green','black'])
# defining egg paramters that will be used later
egg_width = 45
egg_height = 55
egg_score = 10
# for egg speed we just need to define the pixels that egg will jump
egg_speed = 500
egg_interval = 4000
difficulty_factor = 0.95
# defining the parameters of our catcher that will catch eggs
catcher_color = 'blue'
# as our catcher is an arc but still it has height and width ie vertical and horizontal distance
catcher_width = 100
catcher_height = 100
# starting value of x of the arc , and it should be
catcher_start_x = canvas_width / 2 - catcher_width / 2 # starting value 400/2 -100/2 = 350 ie x coordinate
catcher_start_y = canvas_height -catcher_height - 20 # 400 - (100-20) = 320
catcher_start_x2 = catcher_start_x + catcher_width # 450
catcher_start_y2 = catcher_start_y + catcher_height # 420
# after getting all of the paramters we create an arc shape in canvas . from what angle will arc start is 'start' , now add the
# angle of 140 degree to get extent ie 200 + 140 , arc will be started from 200 deg and end at 340 deg
catcher = c.create_arc(catcher_start_x ,catcher_start_y ,catcher_start_x2,catcher_start_y2 , start=200 , extent = 140 , style='arc' , outline=catcher_color , width=3)
# declaring a displaying the score
score = 0
# 10 from x 10 from y and north west corner
score_text = c.create_text(10,10,anchor='nw' , font=('Arial',18,'bold'),fill='darkblue',text='Score : ' + str(score))
# now lets display our lives remaining
lives_remaning = 3
# now this text should be on north east and 10 px lesser than canvas_width
lives_text = c.create_text(canvas_width-10,10,anchor='ne' , font=('Arial',18,'bold'),fill='darkblue',text='Lives : ' + str(lives_remaning))

# now lets add the eggs in an empty list
eggs = []
# now create eggs to append them to upper list
def create_eggs():
    # eggs must vary horizontally but not vertically so x is random
    x = randrange(10,740)
    y = 40
    # now create a new oval , which will pick different colors
    # we dont want to pick random colors instead the very next color in the list of color_cycle
    new_egg = c.create_oval(x,y,x+egg_width,y+egg_height,fill=next(color_cycle),width=0)# x n y are pixels and when you add width and heigh to them you get 2 new diff pixels
    # append newly created in eggs empty list
    eggs.append(new_egg)
    # now keep creating eggs after a certain interval
    win.after(egg_interval,create_eggs)

# now we
def move_eggs():
    for egg in eggs:
        # give coordinates to our created eggs first
        (egg_x,egg_y,egg_x2,egg_y2) = c.coords(egg)
        # now we want our egg not to move along x axis but should move further 10 pixels downwards by 10 px maybe
        c.move(egg,0,10)
        # now collapse the egg only if the ending y pixel of egg that it has covered increases the total canvas height
        if egg_y2 > canvas_height:
            egg_dropped(egg)
    win.after(egg_speed,move_eggs)

def egg_dropped(egg):
    # remove and delete that particular egg
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaning == 0:
        # now need to pop a message box saying....
        messagebox.showinfo('GAME OVER!' , 'Final Score : ' + str(score))
        win.destroy()

def lose_a_life():
    global lives_remaning
    lives_remaning -= 1
    # now we need to change our created item in canvas which is lives_text
    c.itemconfigure(lives_text , text='Lives : ' + str(lives_remaning))

def catch_check():
    (catcher_x,catcher_y,catcher_x2,catcher_y2) = c.coords(catcher)
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2) = c.coords(egg)
        # now to state the condition where an egg reaches within the boundries of catcher
        if catcher_x < egg_x and egg_x2  < catcher_x2 and catcher_y2 - egg_y2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            # increase score with every egg
            increase_score(egg_score)
    # check after every 100 milli sec wheather there was a catch or not
    win.after(100,catch_check)

def increase_score(points):
    global score , egg_speed , egg_interval
    score += points
    # after every increase in score we will change the speed and interval by increasing their respective variables
    egg_speed = int(egg_speed * difficulty_factor)
    egg_interval = int(egg_interval * difficulty_factor)
    # updating every item in canvas
    c.itemconfigure(score_text , text='Score : ' + str(score))

def move_left(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    # if x1 of catcher is 0 this means catcher is already on the boundry and cant move left so we give condition like
    if x1 > 0:
        # decrease the value of x but don't change y
        c.move(catcher,-20,0)

def move_right(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    # x2 = canvas_width means catcher is already on the right boundry
    if x2 < canvas_width:
        # dont move in y direction rather increment 20 in x towards right
        c.move(catcher,20,0)

c.bind('<Left>' , move_left)
c.bind('<Right>' , move_right)
# now when keep pressing the button , you want catcher to move move and move not to stop
c.focus_set()
#after every second create egg , then move egg , then check if egg is caught or not
win.after(1000,create_eggs)
win.after(1000,move_eggs)
win.after(1000,catch_check)

win.mainloop()
