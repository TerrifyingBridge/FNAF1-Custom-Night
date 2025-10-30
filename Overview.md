# Five Nights at Freddy's Custom Night 
Hello and welcome to my repository on a simulation and analysis for Five Night's at Freddy's Custom Night, specifically for Bonnie and Chica. In this specific file, you will be able to find a detailed explanation of what the problem is, how the code works, as well as what results we can determine from these simulations. I will try to reference specific segments of code while explaining them (when that happens) as well as showing each of the graphs the code generates. There will be a lot to get through, so I'll shut up and refer you to the table of contents below!

## Table of Contents

| Link to Section                                     | Description of Segment                                                                                                                                                                                |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Intro to Game / Problem](#Intro-to-Game-/-Problem) | A brief description on what this game is about as well as the specific question we are trying to answer.                                                                                              |
| [AI Breakdown](#AI-Breakdown)                       | A detailed explanation of how the AI works for each of the animatronics.                                                                                                                              |
| [Simulation Explanation](#Simulation-explanation)   | A detailed explanation for how the simulation works. First, the section starts off talking about the logic for how to set up these simulations, the explains how each of this is implemented in code. |
| [Results of Simulation](#Results-of-Simulation)     | Some graphs that are the result of running the simulation as well as some basic statistics from running the simulation many times over.                                                               |
| [Analysis of Results](#analysis-of-results)         | A broad overview of what the results actually mean, and what we can learn from them. This section also talks about how the simulation isn't exactly perfect and where it could be improved.           |
| [Conclusion](#conclusion)                           | Concluding remarks about everything, as well as my ending thoughts with regards to everything.                                                                                                        |

## Intro to Game / Problem
For those of you who don't know, Five Nights at Freddy's is a horror game made by Scott Cawthon in 2014. It is a point and click survival horror game where you play as a night guard for a pizzeria with 4 (technically 5, but I think the 5th one is just a suit and doesn't actually have an animatronic inside of it? Truthfully I'm not sure, I don't pay attention to the lore too heavily) animatronics possessed by the souls of dead children trying to kill you from 12am to 6am. During this time, the player is expected to use cameras set up around the pizzeria to keep track of the animatronics, large doors to prevent animatronics from getting in, and door lights to check to see if animatronics are actually at the door. The building has limited power with the doors, lights, and cameras costing some power per use, so the game becomes a cross of protecting yourself while also not running out of power. As the name suggests, in order to complete the main game, you have to survive 5 nights to complete the main story, with each night getting progressively more difficult. There is a bonus 6th night if you beat the first 5, and then a custom 7th night for completing that one as well. As you might have figured out by now, this custom night is the main topic of this project.

### Basic Description of Animatronics
Before getting the problem at hand, I do want to talk about the different animatronics at a surface level (for those of you who do know what this game is about, I promise I'll stop teasing you soon if you're actually reading this paragraph), those being: Bonnie, Chica, Foxy, and Freddy (the 5th one being 'Golden Freddy' but he doesn't really matter in the context of this project). Bonnie and Chica both wander around the pizzeria, occasionally making a pit stop at your door to kill you.  I will talk more about their paths later in the project, but long story short: Chica stays on the right side of the building, while Bonnie teleports around the left side of the building. As you might imagine, Bonnie can only attack on the left door, and Chica can only attack on the right door. Freddy is a bit different, as he doesn't wander around, as much as he just bee-lines for the player through the right side of the building. You can delay him by watching him with the cameras, but if he makes progress, then he will not go back in his path (unlike Bonnie and Chica). He will continue this path until he's right outside your door, where he will try to attack you if you don't have your door up. Lastly, there is Foxy, who becomes more dangerous the longer you don't have the cameras up. If you look at the cameras (any camera will do), he will be delayed on acting, but the longer you keep the cameras off, then he has a higher chance of increasing his attack stage. This will continue until he gets pissed off enough to run at the player, where the only thing to prevent death is to close the door. This will drain progressively more power the more it happens.

### Question at Hand
Whew! That was a lot! But as mentioned before, this project specifically looks at the custom night for this game. Long story short, in the custom night, you can change the AI values of the animatronics on a value between 0 and 20 (inclusive), with a higher AI value corresponding to a more 'active' version of the animatronic. Naturally, many people like to try to challenge themselves, and want to tackle the games hardest challenge, which of course would be when all animatronics are most active, hence the famous '20/20/20/20' or '4/20' mode. It's a fun and not terribly hard challenge to do, and shows complete mastery of the game.

However, as the game got more popular (and older, combination of both really) people decompiled the code and saw how each of the animatronics work. Some have postulated that it would actually be more difficult to lower some of the AI values instead of having them all at 20. The logic is that for Bonnie and Chica, on a value of 20, they will always move, which means when they get to your door, they will always leave very quickly. Having a lower AI value would eliminate the guarantee that they leave quickly, and has a chance of just camping at the door, and thus draining more power. This comes at a cost, as if they have a chance to camp your door, then they have the same likelihood to camp any of the positions on their path as well. Basically, the theoretically hardest AI value would be one where they have a high enough chance to show up at your door quickly, but also not too high to leave immediately. So the logic goes at least. This leads to the question I plan on trying to answer in this project: <b>What combination of AI values would make the hardest custom night? </b>

### Acknowledgements
Before jumping into actually talking about solving this problem, I do want to give credit for where this idea comes from. While I don't know who was the 'first' person to hypothesize this idea, I first heard of it from Tech Rule's video that gives a decent break down of the Five Nights at Freddy's AI (amongst other things). Admittedly, the biggest reason I wanted to look into this is because I kept seeing people repeat the idea as truth without seeing any proof as to what was actually true. Of course we're working with statistics, so I won't be able to 'prove' anything, just make really good educated guesses (assuming my code even remotely accurate of course), but I figured it would be at least to have <i>some</i> evidence for something. Plus, I am genuinely curious myself. It's a fun math problem, so here we are. 

## AI Breakdown
For this part I want to do a few things. First I will talk about the AI in general (if you know anything about the technical side of Five Nights at Freddy's games, nothing will be new), and then breakdown how each animatronic works specifically. However, for each of the sections where I talk about the animatronics, I also provide a justification to remove them from the simulation (Spoilers: Foxy and Freddy) as we can logic out what the 'hardest' AI value is without any fancy simulations (although I bet you could do some Markov Chain analysis to eliminate the need for simulations altogether, but whatever, this is more fun). Alright let's get started.

The animatronics cannot move whenever they want, they are locked to only moving on certain time intervals. Basically, every X seconds, an animatronic has an opportunity to move. Many people have dubbed these as 'movement opportunities', as they are not always guaranteed to be able to move. A table for the 4 animatronics' movement opportunities can be seen below.

| Foxy         | Freddy       | Bonnie       | Chica        |
| ------------ | ------------ | ------------ | ------------ |
| 5.01 seconds | 3.02 seconds | 4.97 seconds | 4.98 seconds |

Whether the animatronic moves depends on their AI value. The game chooses a random number between 1 and 20 (inclusive), then checks to see if that number is less than or equal to the animatronic's AI value. If the value is less than or equal to the AI value, then the animatronic progresses to their next position, otherwise, they don't move and stay where they are. You can think of these AI values as percent chances to move out of 20. So, for example, if Bonnie has an AI value of 14, then every 4.97 seconds, Bonnie has a $14 / 20 = 0.70 \rightarrow 70\%$ chance to move. 'Moving' means different things for different animatronics (such as Foxy, who stays in one camera until he's in his kill phase), but all animatronics act this way for the entire game. 

### Foxy
Earlier I said that 'moving' means different things for different animatronics, but really, it's just Foxy that is different. As will be seen later, Bonnie, Chica, and Freddy behave much more similarly. Anyway, Foxy has four different stages he can find himself in, with each successful movement opportunity progressing him to the next stage. The first stage is where Foxy starts off, the second and third show Foxy come out of his curtains more and more, and the last stage (stage 4) is when he is in his kill stage. However, Foxy will always fail a movement opportunity when the cameras are up. He is delayed by a random time between 0.83 seconds and 17.48 seconds when the cameras are put down, where he cannot progress. When Foxy is in stage 4, his curtains will be completely open with him absent as he runs to your door. Upon entering stage 4, the player has 1500 frames (25 seconds at the game's native 60 frames per second) before Foxy shows up at the door. This can be expeditated by looking at the left hallway where this will trigger Foxy running at the door immediately. After he has visited and knocked on the door, he will drain power based on this equation: $\text{Power Drain} = 5 \times (\text{Attack Number} - 1) + 1$. After successfully blocking Foxy from killing you, he will return to either stage 1 or 2. Lastly, Foxy's AI value will increase by 1 at 3am and 4am. 

Now, I want to justify why Foxy isn't included in the simulation. Foxy is at his hardest when you need to be looking at him as often as possible, which happens at an AI value of 20. At this level, every time he can move (assuming he is not delayed and the cameras aren't up), he will. If the AI value were lower than 20, then you are more safer to dedicate your attention or power to something else besides the cameras as there is a chance he won't progress without you doing anything, which would make the night a bit easier. Thus, 20 is the hardest AI value for Foxy.

### Freddy
Unlike Foxy, Freddy can actually move on his movement opportunities. He also has a set path he moves along, and once he makes progress, he cannot go back, only forward.  This path starts on the Show Stage in Camera 1A, and eventually ends with Freddy right outside your door in Camera 4B. The full path can be seen in the picture below.

need pic lmao

Alright so the way Freddy actually moves is a bit complicated for some reason. Every successful movement opportunity Freddy will be set to a "Might Move" state. When he is in this state, there is a counter that increases by 1 every 0.01 seconds. Once this counter exceeds a certain value, then Freddy will move to his next position. The certain value changes on his AI value and is determined by the following equation: $\text{Move Counter} = 1000 - 100 * \text{Freddy's AI}$. You might have figured this out because of the equation, but once Freddy's AI is greater than or equal to 10, this counter is 0. Last bit of information I want to talk about is that Freddy cannot moved while the camera systems are looking at him. Basically, you can stall Freddy in his place if you're quick enough with your camera flips. Unlike the rest of the animatronics, Freddy's AI does not increase throughout the night.

Lastly, I want to try and justify why we can ignore Freddy in this simulation as we know Freddy's hardest AI value. Essentially, Freddy can't kill us until he gets to Camera 4B, and once he gets there he will stay there and we always have to deal with him. So Freddy is at his hardest when he is able to get to our door the fastest. If Freddy's AI value is anything less than 20, then there is a non-zero chance that Freddy will just never get to our office (even if this chance is small, it's not non-zero). However, on 20 AI, Freddy will bee-line for our door as quickly as he can, only stopping when he is delayed by the cameras. Thus, Freddy's hardest AI value is 20.

### Bonnie
Bonnie is much more free-roam than Freddy to to speak. He has a list of rooms he can travel to and between (some of which involving teleportation), but stays on the left side of the pizzeria. He starts on the stage in camera 1A and then slowly moves towards your office as seen in the picture below.

I don't have the picture yet.

Some important things to note is that once Bonnie is offstage, he can't get back onstage (I guess that's not too important lol). However, the more important observation from this is that once Bonnie is in either the janitor's closet, the hallway or the hallway corner, he cannot return to the dining area or parts and service. In this sense, he gets trapped near the player and can only return to the dining area after trying (and failing) to attack you at your door. One can see how this would make Bonnie "attack" more often than Chica does (spoilers, sorry). I also think lines up with many people's experiences (I'm not going to do it here, but it's a fun exercise to actually prove that Bonnie shows up more often than Chica does. As many textbooks say, I'll leave it as an exercise for the reader hehe). 

When Bonnie is at your door, he still follows the same movement opportunity rules as before, but with a twist. If the door is open on his next movement opportunity, then he will go into "kill mode".  When in "kill mode", your left light and door will be disabled and Bonnie will kill you if you open and then close the cameras (he'll pull down the cameras if you spend too long in them). If your door is closed, then he will roll his AI value in 20 to move to the next position, which in this case is in camera 1B, where everything repeats until the night is over. For moments when he seems to camp at your door, that is Bonnie failing a lot of movement opportunities. Much like Foxy, his AI value also increases as the night progresses, having the most increase out of any character. Bonnie's AI increases by 1 at 2am, 3am, and 4am. 

Now I want to justify why Bonnie is simulated here, as I want to make the claim that it isn't apparently obvious what his 'most difficult' setting is. If we consider Bonnie at 20 AI for the start of the night, then every 4.97 seconds, he will <i>always</i> move, which means he has a much higher chance getting to your door than lower AI values where he can take his sweet time. However, when Bonnie gets to your door, you know that he will immediately leave after closing the door on his movement interval. Basically, once he attacks, you know he's gone and you can open the door safely until he shows back up again. Contrast this to if Bonnie was at an AI value of 19. If Bonnie is at your door, then there is a chance he will just stay at your door every movement opportunity the door is close, so you have to leave your door closed (or close the door on every attack interval) until he goes away. Using this logic, it seems likely this would be a more difficult situation than just a pure 20 AI value. However, a lower AI value comes at the cost of Bonnie (on average) taking a longer time to get to your door in the first place, make it easier than a 20 AI value. So, which one is harder? In my opinion, this isn't immediately obvious! Hence why I'm adding Bonnie to the simulation.

### Chica
I think Chica gets done dirty in many of these explanations, as everyone chooses Bonnie as the main example when talking about how these animatronics work, and by the time they get to Chica, they're just repeating stuff. This explanation will be no different. She stays to the right side of the building (basically, all the cameras Bonnie doesn't get to except the stage and Pirates Cove), and starts on the stage and never returns when she leaves. A map of her movements around the pizzeria can be seen below.

I need this one too lmao

Chica does have some fun quirks that are worth noting however. I mentioned this before, but Chica can return to any of her positions without needing to attack your door. She could be in the right hallway corner, and then decide that she doesn't want anything to do with you and then move back to the dining hall or restrooms in less than 10 seconds. As mentioned before, this gives Chica a lower chance of appearing at your door, even if her AI matches that of Bonnie. 

The reason Chica is included in the simulation is the exact same reason as Bonnie, so if you'd like an explanation for why, I'd encourage you to read Bonnie's. 

## Simulation Explanation
So, we're going to simulate Bonnie and Chica, but do what with them? Here is where we need to think of exactly what information we want. We want to try and measure difficulty somehow, or at least showcase it in some way. The method I ended up going with is the notice that Bonnie and Chica are at their most difficult when they spend time at your door. My logic for this is that if they aren't at your door when you check the lights, then you don't have to do anything, but if they are there, then you'd have to shut the door to prevent death, which then drains power. Therefore, the information we want to see is when both of these goobers are at their respective doors. We can both look at what time both Bonnie and Chica show up, as well as how long they stay at the door. This will give us a rough estimate for difficulty, with the more difficult runs having Bonnie and Chica stay at the door. This isn't a perfect measure of difficulty, but I talk about that more in the Pitfalls of the Simulation section.

### Simulation Logic
logic of the simulation

### Simulation Code
Since we're simulating a custom night multiple times, I ended up creating a Night class which I named NightSim. This way, I could create NightSim objects to simulate one night, grab the results of the simulation data. This process can be repeated multiple times to get a large amount of data where we can actually see results. Anyway, the first part I did was create variables to store important movement opportunity values. Namely, one variable for the total movement opportunities in a night, one variable the number of movement opportunities before 2am, one variable for 3am, and one for 4am.

```python
TOTAL_MOV_OP = 107  
MOV_OP_BEFORE_2AM = 36  
MOV_OP_BEFORE_3AM = 53  
MOV_OP_BEFORE_4AM = 71
```

The other static variables (technically they're not, because I coded in Python, but whatever) I created were the paths for both Bonnie and Chica. I ended up using dictionaries for this, where the key is the current position and the items in the dictionary is the new locations where that key could go to.

```python
BONNIE_PATH = {"1A": ["5", "1B"], "1B": ["5", "2A"], "5": ["1B", "2A"], "2A": ["3", "2B"], "3": ["2A", "D"], "2B": ["3", "D"], "D": ["1B", "1B"]}  
CHICA_PATH = {"1A": ["1B", "1B"], "1B": ["7", "6"], "7": ["4A", "6"], "6": ["7", "4A"], "4A": ["1B", "4B"], "4B": ["4A", "D"], "D": ["4A", "4A"]}
```

Alright time for the constructor for this class. To start with, I had this class take in two arguments, one for Bonnie's AI value and one for Chica's AI value. This is so I could easily change the values when running the simulations later. These values are also stored in variables to be used by the object. The next segment of code puts both Bonnie and Chica in their starting position at Camera 1A, and initializes the current movement opportunity to 1 (since both Bonnie and Chica cannot move at 0.00 seconds into the night). After that, I create three more variables for whether the current movement opportunity is past 2am, 3am, and 4am, and lastly, I create two empty lists which will store the movement opportunities that Bonnie and Chica spend at the door.

```python
def __init__(self, bonnie_ai, chica_ai):  
    self.bonnie_ai = bonnie_ai  
    self.chica_ai = chica_ai  
  
    self.bonnie_pos = "1A"  
    self.chica_pos = "1A"  
    self.current_mov_op = 1  
  
    self.two_am = False  
    self.three_am = False  
    self.four_am = False  
  
    self.bonnie_at_door = []  
    self.chica_at_door = []
```

Now that the constructor is out of the way, let's get into the class methods. I'll go over each individual one, and then talk about how they all come together to create a proper night simulation. The first method is probably the most intuitive. Namely, if Bonnie and/or Chica are currently at the door (or at position "D" in the dictionary), then append the current movement opportunity to the proper list. 

```python
def check_at_door(self):  
    if (self.bonnie_pos == "D"):  
        self.bonnie_at_door.append(self.current_mov_op)  
  
    if (self.chica_pos == "D"):  
        self.chica_at_door.append(self.current_mov_op)
```

The next method I wanted to talk about is the method for updating the AI. As mentioned in the descriptions for Bonnie and Chica, Bonnie increases his AI value by 1 at 2am, 3am, and 4am and Chica increases her AI value by 1 at 3am and 4am. This specific method does exactly that. It checks to see if the current movement opportunity is above the cap for 2am, 3am, and 4am and then sets the respective variable to True.

```python
def update_ai(self):  
    if (self.current_mov_op > self.MOV_OP_BEFORE_2AM):  
        self.two_am = True  
  
    if (self.current_mov_op > self.MOV_OP_BEFORE_3AM):  
        self.three_am = True  
  
    if (self.current_mov_op > self.MOV_OP_BEFORE_4AM):  
        self.four_am = True
```

This next method actually calculates the next position for both Bonnie and Chica. I tried to keep it as similar to the way FNAF calculates the movement chance (mostly because I thought it would be fun). Basically, it takes the current AI value of the animatronic and adds 1 (True) if it is currently past 3am or 4am (or 2am for Bonnie) and then rolls a random number between 1 and 20 (inclusive). If this number is below the AI value (plus the 2am/3am/4am boost), then the animatronic will move, otherwise, they stay still. If the movement opportunity is successful, then the animatronic's current position is then recalculated using the dictionary mentioned before with a coin toss to determine which direction to go to (which is how the actual game determines it as well).

```python
def update_movement(self):  
    bonnie_roll = random.randint(1, 20)  
    if (self.bonnie_ai + self.two_am + self.three_am + self.four_am >= bonnie_roll):  
        self.bonnie_pos = self.BONNIE_PATH[self.bonnie_pos][random.randint(0, 1)]  
  
    chica_roll = random.randint(1, 20)  
    if (self.chica_ai + self.three_am + self.four_am >= chica_roll):  
        self.chica_pos = self.CHICA_PATH[self.chica_pos][random.randint(0, 1)]
```

Those are all the methods I've created that focus on individual parts, and now we can create the main loop. My logic was to start by updating the AI at the very start. That way if the current movement opportunity is past a milestone (2am/3am/4am) then it would immediately update to the proper value. The next step was to then calculate whether the animatronic would move on the current movement opportunity, and then to calculate the new position if they succeeded. Then we check to see if the new position is at the door, and log it if so. Lastly, we update our current movement opportunity to the next one.

```python
def update(self):  
    self.update_ai()  
    self.update_movement()  
    self.check_at_door()  
    self.current_mov_op += 1
```

One last method to bring it all together! the update() method just runs one loop, and in order to simulate the entire night, we want to repeat this for a total of 107 movement opportunities. That's what this next method does. It repeats the update() method until the night is out of movement opportunities, then returns the data for when Bonnie and Chica visited the door.

```python
def simulate(self):  
    while (self.current_mov_op <= self.TOTAL_MOV_OP):  
        self.update()  
    return [self.bonnie_at_door, self.chica_at_door]
```

From here we can do all sorts of fun stuff, which we'll see in the next section.
## Results of Simulation
blah blah blah I need this for spacing

### Fun Graphs
Some random graphs I wanted to make that don't directly relate to the problem at hand

### Custom Night Graphs
graphs that directly relate to the problem at hand

## Analysis of Results
what the title says stupid

### What I think this says
title. read it dummy

### Pitfalls of Simulation
Yea okay whatever

## Conclusion
The end