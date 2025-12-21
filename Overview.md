# Five Nights at Freddy's Custom Night

Hello and welcome to my repository on a simulation and analysis for Five Night's at Freddy's Custom Night, specifically for Bonnie and Chica. In this specific file, you will be able to find a detailed explanation of what the problem is, how the code works, as well as what results we can determine from these simulations. I will try to reference specific segments of code while explaining them (when that happens) as well as showing each of the graphs the code generates. There will be a lot to get through, so I'll shut up and refer you to the table of contents below!

## Table of Contents

| Link to Section                                     | Description of Segment                                                                                                                                                                                |
|-----------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Intro to Game / Problem](#Intro-to-Game-/-Problem) | A brief description on what this game is about as well as the specific question we are trying to answer.                                                                                              |
| [AI Breakdown](#AI-Breakdown)                       | A detailed explanation of how the AI works for each of the animatronics.                                                                                                                              |
| [Simulation Explanation](#Simulation-explanation)   | A detailed explanation for how the simulation works. First, the section starts off talking about the logic for how to set up these simulations, the explains how each of this is implemented in code. |
| [Results of Simulation](#Results-of-Simulation)     | Some graphs that are the result of running the simulation as well as some basic statistics from running the simulation many times over.                                                               |
| [Analysis of Results](#analysis-of-results)         | A broad overview of what the results actually mean, and what we can learn from them. This section also talks about how the simulation isn't exactly perfect and where it could be improved.           |
| [Conclusion](#conclusion)                           | Concluding remarks about everything, as well as my ending thoughts with regards to everything.                                                                                                        |

## Intro to Game / Problem

For those of you who don't know, Five Nights at Freddy's is a horror game made by Scott Cawthon in 2014. It is a point and click survival horror game where you play as a night guard for a pizzeria with 4 animatronics (technically 5, but I think the 5th one is just a suit and doesn't actually have an animatronic inside of it? Truthfully I'm not sure, I don't pay attention to the lore too heavily) possessed by the souls of dead children trying to kill you from 12am to 6am. During this time, the player is expected to use cameras set up around the pizzeria to keep track of the animatronics, large doors to prevent animatronics from getting in, and door lights to check to see if animatronics are actually at the door. The building has limited power with the doors, lights, and cameras costing some power per use, so the game becomes a cross of protecting yourself while also not running out of power. As the name suggests, in order to complete the main game, you have to survive 5 nights to complete the main story, with each night getting progressively more difficult. There is a bonus 6th night if you beat the first 5, and then a custom 7th night for completing that one as well. As you might have figured out by now, this custom night is the main topic of this project.

### Basic Description of Animatronics

Before getting the problem at hand, I do want to talk about the different animatronics at a surface level (for those of you who do know what this game is about, I promise I'll stop teasing you soon if you're actually reading this paragraph), those being: Bonnie, Chica, Foxy, and Freddy (the 5th one being 'Golden Freddy' but he doesn't really matter in the context of this project). Bonnie and Chica both wander around the pizzeria, occasionally making a pit stop at your door to kill you. I will talk more about their paths later in the project, but long story short: Chica stays on the right side of the building, while Bonnie teleports around the left side of the building. As you might imagine, Bonnie can only attack on the left door, and Chica can only attack on the right door. Freddy is a bit different, as he doesn't wander around, as much as he just bee-lines for the player through the right side of the building. You can delay him by watching him with the cameras, but if he makes progress, then he will not go back in his path (unlike Bonnie and Chica). He will continue this path until he's right outside your door, where he will try to attack you if you don't have your door up. Lastly, there is Foxy, who becomes more dangerous the longer you don't have the cameras up. If you look at the cameras (any camera will do), he will be delayed on acting, but the longer you keep the cameras off, then he has a higher chance of increasing his attack stage. This will continue until he gets pissed off enough to run at the player, where the only thing to prevent death is to close the door. This will drain progressively more power the more it happens.

### Question at Hand

Whew! That was a lot! But as mentioned before, this project specifically looks at the custom night for this game. Long story short, in the custom night, you can change the AI values of the animatronics on a value between 0 and 20 (inclusive), with a higher AI value corresponding to a more 'active' version of the animatronic. Naturally, many people like to try to challenge themselves, and want to tackle the games hardest challenge, which of course would be when all animatronics are most active, hence the famous '20/20/20/20' or '4/20' mode. It's a fun and not terribly hard challenge to do, and shows complete mastery of the game.

However, as the game got more popular (and older, combination of both really) people decompiled the code and saw how each of the animatronics work. Some have postulated that it would actually be more difficult to lower some of the AI values instead of having them all at 20. The logic is that for Bonnie and Chica, on a value of 20, they will always move, which means when they get to your door, they will always leave very quickly. Having a lower AI value would eliminate the guarantee that they leave quickly, and has a chance of just camping at the door, and thus draining more power. This comes at a cost, as if they have a chance to camp your door, then they have the same likelihood to camp any of the positions on their path as well. Basically, the theoretically hardest AI value would be one where they have a high enough chance to show up at your door quickly, but also not too high to leave immediately. So the logic goes at least. This leads to the question I plan on trying to answer in this project: <b>What combination of AI values would
make the hardest custom night? </b>

### Acknowledgements

Before jumping into actually talking about solving this problem, I do want to give credit for where this idea comes from. While I don't know who was the 'first' person to hypothesize this idea, I first heard of it from Tech Rule's video that gives a decent break down of the Five Nights at Freddy's AI (amongst other things). Admittedly, the biggest reason I wanted to look into this is because I kept seeing people repeat the idea as truth without seeing any proof as to what was actually true. Of course we're working with statistics, so I won't be able to 'prove' anything, just make really good educated guesses (assuming my code even remotely accurate of course), but I figured it would be at least to have <i>some</i> evidence for something. Plus, I am genuinely curious myself. It's a fun math problem, so here we are.

## AI Breakdown

For this part I want to do a few things. First I will talk about the AI in general (if you know anything about the technical side of Five Nights at Freddy's games, nothing will be new), and then breakdown how each animatronic works specifically. However, for each of the sections where I talk about the animatronics, I also provide a justification to remove them from the simulation (Spoilers: Foxy and Freddy) as we can logic out what the 'hardest' AI value is without any fancy simulations (although I bet you could do some Markov Chain analysis to eliminate the need for simulations
altogether, but whatever, this is more fun). Alright let's get started.

The animatronics cannot move whenever they want, they are locked to only moving on certain time intervals. Basically, every X seconds, an animatronic has an opportunity to move. Many people have dubbed these as 'movement opportunities', as they are not always guaranteed to be able to move. A table for the 4 animatronics' movement opportunities can be seen below.

| Foxy         | Freddy       | Bonnie       | Chica        |
|--------------|--------------|--------------|--------------|
| 5.01 seconds | 3.02 seconds | 4.97 seconds | 4.98 seconds |

Whether the animatronic moves depends on their AI value. The game chooses a random number between 1 and 20 (inclusive), then checks to see if that number is less than or equal to the animatronic's AI value. If the value is less than or equal to the AI value, then the animatronic progresses to their next position, otherwise, they don't move and stay where they are. You can think of these AI values as percent chances to move out of 20. So, for example, if Bonnie has an AI
value of 14, then every 4.97 seconds, Bonnie has a $14 / 20 = 0.70 \rightarrow 70\%$ chance to move. 'Moving' means different things for different animatronics (such as Foxy, who stays in one camera until he's in his kill phase), but all animatronics act this way for the entire game.

### Foxy

Earlier I said that 'moving' means different things for different animatronics, but really, it's just Foxy that is different. As will be seen later, Bonnie, Chica, and Freddy behave much more similarly. Anyway, Foxy has four different stages he can find himself in, with each successful movement opportunity progressing him to the next stage. The first stage is where Foxy starts off, the second and third show Foxy come out of his curtains more and more, and the last stage (stage 4) is when he is in his kill stage. However, Foxy will always fail a movement opportunity when the cameras are up. He is delayed by a random time between 0.83 seconds and 17.48 seconds when the cameras are put down, where he cannot progress. When Foxy is in stage 4, his curtains will be completely open with him absent as he runs to your door. Upon entering stage 4, the player has 1500 frames (25 seconds at the game's native 60 frames per second) before Foxy shows up at the door. This can be expeditated by looking at the left hallway where this will trigger Foxy running at the door immediately. After he has visited and knocked on the door, he will drain power based on this equation: $\text{Power Drain} = 5 \times (\text{Attack Number} - 1) + 1$. After successfully blocking Foxy from killing you, he will return to either stage 1 or 2. Lastly, Foxy's AI value will increase by 1 at 3am and 4am.

Now, I want to justify why Foxy isn't included in the simulation. Foxy is at his hardest when you need to be looking at him as often as possible, which happens at an AI value of 20. At this level, every time he can move (assuming he is not delayed and the cameras aren't up), he will. If the AI value were lower than 20, then you are more safer to dedicate your attention or power to something else besides the cameras as there is a chance he won't progress without you doing anything, which would make the night a bit easier. Thus, 20 is the hardest AI value for Foxy.

### Freddy

Unlike Foxy, Freddy can actually move on his movement opportunities. He also has a set path he moves along, and once he makes progress, he cannot go back, only forward. This path starts on the Show Stage in Camera 1A, and eventually ends with Freddy right outside your door in Camera 4B. The full path can be seen in the picture below.

need pic lmao

Alright so the way Freddy actually moves is a bit complicated for some reason. Every successful movement opportunity Freddy will be set to a "Might Move" state. When he is in this state, there is a counter that increases by 1 every 0.01 seconds. Once this counter exceeds a certain value, then Freddy will move to his next position. The certain value changes on his AI value and is determined by the following equation: $\text{Move Counter} = 1000 - 100 * \text{Freddy's AI}$. You might have figured this out because of the equation, but once Freddy's AI is greater than or equal to 10, this counter is 0. Last bit of information I want to talk about is that Freddy cannot moved while the camera systems are looking at him. Basically, you can stall Freddy in his place if you're quick enough with your camera flips. Unlike the rest of the animatronics, Freddy's AI does not increase throughout the night.

Lastly, I want to try and justify why we can ignore Freddy in this simulation as we know Freddy's hardest AI value. Essentially, Freddy can't kill us until he gets to Camera 4B, and once he gets there he will stay there and we always have to deal with him. So Freddy is at his hardest when he is able to get to our door the fastest. If Freddy's AI value is anything less than 20, then there is a non-zero chance that Freddy will just never get to our office (even if this chance is small, it's not non-zero). However, on 20 AI, Freddy will bee-line for our door as quickly as he can, only stopping when he is delayed by the cameras. Thus, Freddy's hardest AI value is 20.

### Bonnie

Bonnie is much more free-roam than Freddy to to speak. He has a list of rooms he can travel to and between (some of which involving teleportation), but stays on the left side of the pizzeria. He starts on the stage in camera 1A and then slowly moves towards your office as seen in the picture below.

I don't have the picture yet.

Some important things to note is that once Bonnie is offstage, he can't get back onstage (I guess that's not too important lol). However, the more important observation from this is that once Bonnie is in either the janitor's closet, the hallway or the hallway corner, he cannot return to the dining area or parts and service. In this sense, he gets trapped near the player and can only return to the dining area after trying (and failing) to attack you at your door. One can see how this would make Bonnie "attack" more often than Chica does (spoilers, sorry). I also think lines up with many people's experiences (I'm not going to do it here, but it's a fun exercise to actually prove that Bonnie shows up more often than Chica does. As many textbooks say, I'll leave it as an exercise for the reader hehe).

When Bonnie is at your door, he still follows the same movement opportunity rules as before, but with a twist. If the door is open on his next movement opportunity, then he will go into "kill mode". When in "kill mode", your left light and door will be disabled and Bonnie will kill you if you open and then close the cameras (he'll pull down the cameras if you spend too long in them). If your door is closed, then he will roll his AI value in 20 to move to the next position, which in this case is in camera 1B, where everything repeats until the night is over. For moments when he seems to camp at your door, that is Bonnie failing a lot of movement opportunities. Much like Foxy, his AI value also increases as the night progresses, having the most increase out of any character. Bonnie's AI increases by 1 at 2am, 3am, and 4am.

Now I want to justify why Bonnie is simulated here, as I want to make the claim that it isn't apparently obvious what his 'most difficult' setting is. If we consider Bonnie at 20 AI for the start of the night, then every 4.97 seconds, he will <i>always</i> move, which means he has a much higher chance getting to your door than lower AI values where he can take his sweet time. However, when Bonnie gets to your door, you know that he will immediately leave after closing the door on his movement interval. Basically, once he attacks, you know he's gone and you can open the door safely until he shows back up again. Contrast this to if Bonnie was at an AI value of 19. If Bonnie is at your door, then there is a chance he will just stay at your door every movement opportunity the door is close, so you have to leave your door closed (or close the door on every attack interval) until he goes away. Using this logic, it seems likely this would be a more difficult situation than just a pure 20 AI value. However, a lower AI value comes at the cost of Bonnie (on average) taking a longer time to get to your door in the first place, make it easier than a 20 AI value. So, which one is harder? In my opinion, this isn't immediately obvious! Hence why I'm adding Bonnie to the simulation.

### Chica

I think Chica gets done dirty in many of these explanations, as everyone chooses Bonnie as the main example when talking about how these animatronics work, and by the time they get to Chica, they're just repeating stuff. This explanation will be no different. She stays to the right side of the building (basically, all the cameras Bonnie doesn't get to except the stage and Pirates Cove), and starts on the stage and never returns when she leaves. A map of her movements around the pizzeria can be seen below.

I need this one too lmao

Chica does have some fun quirks that are worth noting however. I mentioned this before, but Chica can return to any of her positions without needing to attack your door. She could be in the right hallway corner, and then decide that she doesn't want anything to do with you and then move back to the dining hall or restrooms in less than 10 seconds. As mentioned before, this gives Chica a lower chance of appearing at your door, even if her AI matches that of Bonnie.

The reason Chica is included in the simulation is the exact same reason as Bonnie, so if you'd like an explanation for why, I'd encourage you to read Bonnie's.

## Simulation Explanation

So, we're going to simulate Bonnie and Chica, but do what with them? Here is where we need to think of exactly what information we want. We want to try and measure difficulty somehow, or at least showcase it in some way. The method I ended up going with is the notice that Bonnie and Chica are at their most difficult when they spend time at your door. My logic for this is that if they aren't at your door when you check the lights, then you don't have to do anything, but if they are there, then you'd have to shut the door to prevent death, which then drains power. Therefore, the information we want to see is when both of these goobers are at their respective doors. We can both look at what time both Bonnie and Chica show up, as well as how long they stay at the door. This will give us a rough estimate for difficulty, with the more difficult runs having Bonnie and Chica stay at the door. This isn't a perfect measure of difficulty, but I talk about that more in the Pitfalls of the Simulation section.

### Simulation Logic

The way I thought of difficulty for this game is how much power drain you have across the night. Technically, there is a passive power drain as the night progresses regardless if you do anything, but since you can't change this in the custom night, I'm going to politely ignore it. So how should we measure power drain? Well, I chose to do this indirectly by instead counting which movement opportunities both Bonnie and Chica spend at their door positions. The reason for this is because you will need to close the door and spend power blocking their attacks at these times. We can also ignore actions such as lights and camera flips as these will mostly remain constant regardless of the positions of the animatronics, as the only varying factor in a custom night will be Bonnie and Chica. 

There are a number of ways to measure how long both Bonnie and Chica remain at their respective door positions. The first method I initially chose was to measure it in time using a subdivision of $\frac{1}{300}$ seconds, which translated to the program checking the status of the animatronics $160500$ times. A tad excessive. The solution I ended up landing on was to iterate over the movement opportunities, as these will be the only times Bonnie or Chica could move. This ends up working out pretty well as Bonnie and Chica have the same number of movement opportunities across the entire night. Don't believe me? Check this out!

One night in FNAF 1 lasts $8$ minutes and $55$ seconds or $535$ seconds (the reason it's not a flush $9$ minutes is because of a slight off by one logic error in the code). To find the number of movement opportunities for each animatronic, we take the total time and divide it by the length of the movement opportunity of the animatronic and then floor it (since the extra bit would be an incomplete movement opportunity).

$$
\begin{aligned}
&\text{Bonnie MOs} = floor(535 / 4.97) = floor(107.6459...) = 107 \\
&\text{Chica MOs} = floor(535 / 4.98) = floor(107.4297...) = 107
\end{aligned}
$$

Basically, while both Bonnie and Chica will appear and disappear from your door at different times, the total movement opportunities are pretty much the same, at least as far as the simulation is concerned. This is an easy conversion to time as well as we just need to count how many movement opportunities Bonnie and Chica spend at your door, then just multiply these values by their respective time durations. For example, if Bonnie spends $6$ movement opportunities at the door and Chica spends $4$ movement opportunities at the door, then the total time you'd need to spend having the doors closed would be $6*4.97 + 4*4.98$ (technically, you only need to close the door at the *end* of the movement opportunity which means you could get away with just having the door closed for a second for each animatronic MO at the door, but this would still scale with the total MOs, which in the example previous would be $6 + 4$). 

We also want this simulation to increase the AI value for Bonnie and Chica across the night at the proper times (2, 3 and 4 am for Bonnie and 3 and 4 am for Chica). Fortunately, because of the movement opportunity system, things work out very well. Namely the number of movement opportunities that pass per in game hour is the same for both Bonnie and Chica. This allows us to use this as a tracker for time when looping the simulation.

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

Alright there are A LOT of different information we can take from this simulation. For most of these cases, I tend to use $1,000,000$ simulations of a specific custom night. This is long enough to be mostly accurate of what we're looking at, while not spending too might time to generate each graph. The first graphs I want to look at won't directly answer our question, but I want to use them to just investigate different AI value distributions and other fun things. Later on, I'll make composition graphs of the actual problem we're investigating.

We can also make our lives a bit easier while generating and looking at each graph, but assuming the randomly generate numbers for Bonnie and Chica are independent of one another. Basically, regardless of what Chica's AI value is, the distribution of time spent at the door for Bonnie will remain the same if his AI value doesn't change (i.e. Bonnie would work the same if the night settings were Bonnie: 3, Chica 7 and Bonnie 3, Chica 20).

### Fun Graphs

#### Door Visit Distribution
The first type of graphs I want to look at is when Bonnie and Chica are even at the door. The idea behind these graphs was to create 107 bins, one for each movement opportunity, and if Bonnie or Chica was at the door on a given movement opportunity, then $1$ would be added to that specific bin. For example, say we ran a simulation where Bonnie was at the door on the 26th, 57th, and 106th movement opportunity, then we would add one to the 26th bin, 57th bin, and the 106th bin. Repeating this process $1,000,000$ gives us a distribution of when Bonnie and Chica are at the door at any one particular time. 

Since the data itself is discrete, I ended up using a box plot to create these plots. It still reads like a histogram in some way as it shows a distribution over time, but is still a box plot at it's core. I also wanted to showcase how I made this graph in code, so we're all on the same page. The first step is to create a list of all the movement opportunities for both Bonnie and Chica. To do this, I created a generic MO list consisting of integers 1 through 107. From here, I created two new lists which converted each movement opportunity for Bonnie and Chica into their respective hour time in which it happens, rounded to the hundredths place (i.e. Bonnie's 36th MO is converted to ~2 am). Lastly, I create two empty lists (one for Bonnie and one for Chica) which will be the bins we store the data into.

```python
MO = [i for i in range(1, 108)]  
bonnie_mo = []  
chica_mo = []  
for i in range(1, 108):  
    bonnie_mo.append(round(mo_to_hour(i, "b"), 2))  
    chica_mo.append(round(mo_to_hour(i, "c"), 2))

bonnie_data = [0 for i in range(1, 108)]
chica_data = [0 for i in range(1, 108)]
```

Now that we have empty lists, we need to fill them with data. Here I created a NightSim for $1,000,000$ times and stored the visit data for Bonnie and Chica into a temporary variable. I looped through the visit data for the night, and added $1$ to the bin of the movement opportunity in which Bonnie or Chica was at the door. It works out rather conveniently that the MO value lines up with $1$ more than the index of the list, which allows me to use it as an index when determining which bin to add $1$ to.

```python
for _ in range(total_sim):  
    x = NightSim.NightSim(bonnie_ai, chica_ai)
    visits = x.simulate()
    
    for time in visits[0]:
	    bonnie_data[time - 1] += 1
	for time in visits[1]:
		chica_data[time - 1] += 1
```

The final part is to actually plot these graphs. For sake of brevity, I'm only showing the code made for Bonnie's graph. I promise the one for Chica is virtually identical with very minor changes made. Regardless, here is the code used to made the visit distribution.

```python
plt.figtext(0.144, 0.85, "# of Sims: " + str(total_sim), size=14)  
plt.figtext(0.13,0.8, "Bonnie's AI: " + str(bonnie_ai), size=14)  
plt.xlabel("Night Hour (0 = 12AM)", size=16)  
plt.ylabel("Relative Frequency", size=16)  
plt.ylim(0, max(bonnie_first_visits)*1.15)  
plt.title("Bonnie's First Visit Distribution", size=20)  
plt.bar(bonnie_mo, bonnie_first_visits, width=0.04)
```

Alright it's time to actually look at some graphs now. For each graph, the number of simulations and the AI value are labeled in the top left hand corner of the graph.

##### Bonnie Visit Distribution
|                   AI Value 0                   |                  AI Value1 1                   |
| :--------------------------------------------: | :--------------------------------------------: |
| ![](images/visit_dist/bonnie0_visit_dist.png)  | ![](images/visit_dist/bonnie1_visit_dist.png)  |
|                   AI Value 5                   |                  AI Value 10                   |
| ![](images/visit_dist/bonnie5_visit_dist.png)  | ![](images/visit_dist/bonnie10_visit_dist.png) |
|                  AI Value 15                   |                  AI Value 20                   |
| ![](images/visit_dist/bonnie15_visit_dist.png) | ![](images/visit_dist/bonnie20_visit_dist.png) |

##### Chica Visit Distribution
|                  AI Value 0                   |                  AI Value 1                   |
| :-------------------------------------------: | :-------------------------------------------: |
| ![](images/visit_dist/chica0_visit_dist.png)  | ![](images/visit_dist/chica1_visit_dist.png)  |
|                  AI Value 5                   |                  AI Value 10                  |
| ![](images/visit_dist/chica5_visit_dist.png)  | ![](images/visit_dist/chica10_visit_dist.png) |
|                  AI Value 15                  |                  AI Value 20                  |
| ![](images/visit_dist/chica15_visit_dist.png) | ![](images/visit_dist/chica20_visit_dist.png) |

#### First Visit Distribution
The other graph I wanted to look at purely for the sake of it is the distribution of the first time Bonnie and Chica show up at the door. It is very similar to the general visit distribution, but instead of looking at every time Bonnie or Chica show up at the door, we only care about the first time it happens. If Bonnie or Chica never show up at the door, then we don't have to add anything. Since the set up is the same, I used the same MO code that I used for the general visit distribution.

```python
MO = [i for i in range(1, 108)]  
bonnie_mo = []  
chica_mo = []  
for i in range(1, 108):  
    bonnie_mo.append(round(mo_to_hour(i, "b"), 2))  
    chica_mo.append(round(mo_to_hour(i, "c"), 2))

bonnie_first_visits = [0 for i in range(1, 108)]
chica_first_visits = [0 for i in range(1, 108)]
```

The simulation code is different however. I still run it for $1,000,000$ simulations, but now we first have to check to see if there is at least one visit for both Bonnie and Chica, then simply add one to whichever MO bin it lands on. Like last time, since the MO's value is one more than it's index in the list, we can use it as a locator for finding it's bin.

```python
for _ in range(total_sim):  
    x = NightSim.NightSim(bonnie_ai, chica_ai)
    visits = x.simulate()  
    
    if (len(visits[0]) > 0):
	    bonnie_first_visits[visits[0][0] - 1] += 1
	if (len(visits[1]) > 0):
		chica_first_visits[visits[1][0] - 1] += 1
```

Now that we have this data we can plot it, which I do using the code below. Like last time, this is just the code for Bonnie, as the code for Chica is remarkably similar.

```python
plt.figtext(0.131, 0.85, "# of Sims: " + str(total_sim), size=14)  
plt.figtext(0.13,0.8, "Chica's AI: " + str(chica_ai), size=14)  
plt.xlabel("Night Hour (0 = 12AM)", size=16)  
plt.ylabel("Relative Frequency", size=16)  
plt.ylim(0, max(chica_first_visits)*1.15)  
plt.title("Chica's First Visit Distribution", size=20)  
plt.bar(chica_mo, chica_first_visits, width=0.04)
```

Now it's time for the plots themselves! Truthfully, these are my favorite plots to look at, as for lower AI values, it is really obvious when the increase in the AI value happens.

##### Bonnie's First Visit Distribution
|                         AI Value 0                         |                         AI Value 1                         |
| :--------------------------------------------------------: | :--------------------------------------------------------: |
| ![](images/first_visit_dist/bonnie0_first_visit_dist.png)  | ![](images/first_visit_dist/bonnie1_first_visit_dist.png)  |
|                         AI Value 5                         |                        AI Value 10                         |
| ![](images/first_visit_dist/bonnie5_first_visit_dist.png)  | ![](images/first_visit_dist/bonnie10_first_visit_dist.png) |
|                        AI Value 15                         |                        AI Value 20                         |
| ![](images/first_visit_dist/bonnie15_first_visit_dist.png) | ![](images/first_visit_dist/bonnie20_first_visit_dist.png) |

##### Chica's First Visit Distribution
|                        AI Value 0                         |                        AI Value 1                         |
| :-------------------------------------------------------: | :-------------------------------------------------------: |
| ![](images/first_visit_dist/chica0_first_visit_dist.png)  | ![](images/first_visit_dist/chica1_first_visit_dist.png)  |
|                        AI Value 5                         |                        AI Value 10                        |
| ![](images/first_visit_dist/chica5_first_visit_dist.png)  | ![](images/first_visit_dist/chica10_first_visit_dist.png) |
|                        AI Value 15                        |                        AI Value 20                        |
| ![](images/first_visit_dist/chica15_first_visit_dist.png) | ![](images/first_visit_dist/chica20_first_visit_dist.png) |

### Custom Night Graphs

Alright enough delay, let's take a look at the actual question at hand. We want to find the total time spent at the door for both Bonnie and Chica for all AI values (0 through 20). To do this, I created an empty list for each AI value. Then, I ran a simulation of $100,000$ nights per AI value (doing $1,000,000$ per AI value was taking way too long), and for each night, I appended the length of the visit list to get the total MOs spent at the door. After I plotted the distribution for each AI value in a box plot together to see the larger trend. The code for this can be seen below.

```python
bonnie_time_all_ai = dict(enumerate([[] for i in range(21)]))  
chica_time_all_ai = dict(enumerate([[] for i in range(21)]))  
  
for i in range(21):  
    for _ in range(total_sim):  
        x = NightSim.NightSim(i, i)  
        visits = x.simulate()  
  
        bonnie_time_all_ai[i].append(len(visits[0]))  
        chica_time_all_ai[i].append(len(visits[1]))

plt.figure(figsize=(10, 6))  
plt.figtext(0.644, 0.85, "# of Sims: " + str(total_sim), size=14)  
plt.xlabel("AI Value", size=16)  
plt.ylabel("MOs Spent At Door", size=16)  
plt.title("Chica's Time At Door For An AI Value", size=20)  
plt.boxplot(chica_time_all_ai.values(), tick_labels=chica_time_all_ai.keys(), showmeans=True)
  
plt.figure(figsize=(10, 6))  
plt.figtext(0.644, 0.85, "# of Sims: " + str(total_sim), size=14)  
plt.xlabel("AI Value", size=16)  
plt.ylabel("MOs Spent At Door", size=16)  
plt.title("Bonnie's Time At Door For An AI Value", size=20)  
plt.boxplot(bonnie_time_all_ai.values(), tick_labels=bonnie_time_all_ai.keys(), showmeans=True)
```

As a quick aside, I wanted to give a brief justification for what a box plot is. If you're familiar with this then you can skip the next little bit and jump straight to the graphs. Basically, it's a nice way to look at data in terms of it's quartiles. In the plot below, you can see a side by side of what the bar plot looks like along with it's equivalent box plot. The left tail represents the bottom 25% of the data, the middle rectangle represents the middle 50% of the data, and the right tail represents the top 25% of the data. The orange line represents the medium (middle of the data set), and the black dots represent outliers of the dataset.

|              Bar Plot               |              Box Plot               |
| :---------------------------------: | :---------------------------------: |
| ![](images/bonnie_MO_at_door_1.png) | ![](images/bonnie_MO_at_door_3.png) |

Hopefully the side-by-side helps with the comparison between the two (keep in mind the x-axis for the box plot is 10 movement opportunities bigger than the bar plot because the simulation happened to role a *really* unlucky situation where Bonnie camped at the door for a while). The two graphs represent mostly the same thing, just a different way of representing it. For the final graphs I will use a vertical version, where instead of the left side of the plot being 0, the bottom is 0 instead. Why I am choosing to do this will be more clear soon. Example is shown below.

|         Horizontal Box Plot         |          Vertical Box Plot          |
| :---------------------------------: | :---------------------------------: |
| ![](images/bonnie_MO_at_door_3.png) | ![](images/bonnie_MO_at_door_2.png) |

Alright enough of that, let's see the actual plots. As mentioned I used the vertical box plot because it makes more sense to me to have the x - axis be the AI values. For these plots, I also added the mean to the graph, which is noted by the center of the green triangles. Lastly, I couldn't decide if I liked with outliers or without outliers more, so I decided to make a graph for both.

#### Bonnie's Time Spent At Door For Each AI Value
|         Without Outliers         |              With Outliers               |
| :------------------------------: | :--------------------------------------: |
| ![](images/bonnie_door_dist.png) | ![](images/bonnie_door_dist_outlier.png) |
Since it is kind of difficult to see, I also wanted to list the exact means for each of the AI values, which is found in the table below.

| AI Value | Mean MO Spent At Door |
| -------- | --------------------- |
| 0        | 5.16489               |
| 1        | 9.07587               |
| 2        | 11.64847              |
| 3        | 13.11544              |
| 4        | 13.92042              |
| 5        | 14.40443              |
| 6        | 14.7232               |
| 7        | 14.94985              |
| 8        | 15.12798              |
| 9        | 15.26798              |
| 10       | 15.40443              |
| 11       | 15.46504              |
| 12       | 15.55292              |
| 13       | 15.60678              |
| 14       | 15.65878              |
| 15       | 15.72077              |
| 16       | 15.75654              |
| 17       | 15.78552              |
| 18       | 15.81775              |
| 19       | 15.83322              |
| 20       | 15.87482              |

#### Chica's Time Spent At Door For Each AI Value
|        Without Outliers         |              With Outliers               |
| :-----------------------------: | :--------------------------------------: |
| ![](images/chica_door_dist.png) | ![](images/chica_door_dist_outliers.png) |
Since it is kind of difficult to see, I also wanted to list the exact means for each of the AI values, which is found in the table below.

| AI Value | Mean MO Spent At Door |
| -------- | --------------------- |
| 0        | 0.59368               |
| 1        | 3.0403                |
| 2        | 4.92326               |
| 3        | 5.97047               |
| 4        | 6.52226               |
| 5        | 6.873                 |
| 6        | 7.11486               |
| 7        | 7.30053               |
| 8        | 7.42895               |
| 9        | 7.52868               |
| 10       | 7.58297               |
| 11       | 7.66861               |
| 12       | 7.71179               |
| 13       | 7.77222               |
| 14       | 7.78996               |
| 15       | 7.82894               |
| 16       | 7.86401               |
| 17       | 7.89597               |
| 18       | 7.91724               |
| 19       | 7.94253               |
| 20       | 7.94869               |

## Analysis of Results

This section will only be an analysis of the problem at hand. While I think there are fun parts to analyze for the other graphs I made, I'm going to stick with the total MOs spent at the doors. The first part I want to look at is the averages for both Bonnie and Chica. Both Bonnie and Chica's median and mean increases as the AI level increase, with the later strictly increasing.

### Median
Starting with the median first, Bonnie's median stays at a constant 16 MOs from AI 14 and above while Chica's median stays at a constant 8 MOs from AI 15 and above. Both of these values make sense, especially if you look at the steadily increasing mean. Since the median is the data point in the middle of the data, it has to take the value of a data point, and because all data points integers, the median can only increase in integer steps. It's also worth noting that until the median levels out, it is consistently lower than the mean, indicated a left-skewed set of data. This also makes sense as since the median and mean are much closer to the minimum (0 MOs spent at the door) than the maximum (104 MOs spent at the door). That's about all I have to say about the median for both Bonnie and Chica. Ordinarily I would do a t-test to determine if the two values are statistically different, but for the higher AI values, they are quite literally the same.

### Mean
Alright so the mean is a lot more tricky. As mentioned before, the mean MO spent at the door for both Bonnie and Chica strictly increases as the AI value increases, with a maximum at an AI value of 20. This seems to be a strong case that an AI value of 20 is the most difficult for this reason. However, before coming to any conclusions, we need to make sure that these values are statistically significant from each other and not due to random variations. To do this, I used a t-test between the data sets with an AI value of 19 and 20 for both Bonnie and Chica. The reason for this and not something like an ANOVA test is because if an AI value of 20 is different than 19, then clearly it will be different from all AI values below 19. The t-test will generate a p-value, which means the probability that the different in the means happens by random chance. This value will never be exactly 0, so to determine if the two values are statistically significant, a cut-off value is used, usually designated with the Greek letter $\alpha$. Personally, I like to use $\alpha = 0.01$, which means our p-value needs to be below $0.01$ for the difference to be significant. Anyway enough delay, for the data that was represented in the results section, the results are as follows.

$$
\begin{aligned}
\text{P Value for Bonnie MO Means (AI 19 and 20)} &= 0.000653219009700692 \\
\text{P Value for Chica MO Means (AI 19 and 20)} &= 0.7368695937071894
\end{aligned}
$$

Bonnie's p-value is much lower than what we need it to be, by almost a factor of 100. Chica's p-value on the other hand is very high being no where close to out $0.01$ cut-off. Effectively, this means that the difference between the mean time spent at the door is very significant for Bonnie when switching between an AI of 19 and 20, however, statistically, there is no difference between 19 and 20 for Chica. This can be seen by looking at a 99% confidence interval around the means which shows significant overlap between the values.

| AI Value | Bonnie / Chica | Mean MO at Door |               99% Confidence Interval               |
| :------: | :------------: | :-------------: | :-------------------------------------------------: |
|    19    |     Bonnie     |    15.846519    | $$ 15.829116707882946 < \mu < 15.857843292117053 $$ |
|    19    |     Chica      |    7.936391     | $$ 7.918399650257855 < \mu < 7.9612203497421445 $$  |
|    20    |     Bonnie     |    15.875243    | $$ 15.857581343718456 < \mu < 15.885038656281543 $$ |
|    20    |     Chica      |     7.95256     |  $$ 7.919435203463387 < \mu < 7.961284796536614 $$  |

Ordinarily, this is where a general analysis would end, but since we can generate however many cycles of simulations we want, it is very easy to keep re-rolling the simulation with different random seeds until we get a p-value that we want. For example, while testing the plots, I found the following p-values for a differently generated set of data.

$$
\begin{aligned}
\text{2nd Run: P Value for Bonnie MO Means (AI 19 and 20)} &= 0.000769368789118122 \\
\text{2nd Run: P Value for Chica MO Means (AI 19 and 20)} &= 0.039834379715173965
\end{aligned}
$$

While this run tells a very similar story for Bonnie, it doesn't for Chica. Now Chica is below our cut-off value and is thus significantly different between an AI value of 19 and 20. While it is significantly more difficult, I have seen at least one instance of Bonnie's p-value also not meeting the cut-off as well.

So what does this mean? Are these two values significantly different? The honest answer is: I don't know. In general, re-rolling randomness until you get the result you want to see is a classic example of cherry picking, which is something I don't want to do. That being said, Chica's status of significantly different flip flops between random seeds almost like a coin toss, so it's not *completely* far-fetched to indicate that it is significantly different. In general, this is where things would end, if we didn't have the option of increasing the number of simulations we can generate. For all 4 p-values calculated above, I was using a total simulation count of $100,000$ because it was lumped in with all 21 different AI values. However, if we focus on just 19 and 20, we can finish $1,000,000$ and beyond in a *reasonable* time (this is where my choice of python is biting me in the butt). Anyway, the means calculated for $1,000,000$ simulations along with their confidence interval and p-values for the new t-test are below.

| AI Value | Bonnie / Chica | Mean MO at Door |               99% Confidence Interval               |
| :------: | :------------: | :-------------: | :-------------------------------------------------: |
|    19    |     Bonnie     |    15.846519    | $$ 15.841964953812903 < \mu < 15.851073046187098 $$ |
|    19    |     Chica      |    7.936391     |  $$ 7.929613037475604 < \mu < 7.943168962524397 $$  |
|    20    |     Bonnie     |    15.875243    | $$ 15.870895798621266 < \mu < 15.879590201378733 $$ |
|    20    |     Chica      |     7.95256     |   $$ 7.94595275403383 < \mu < 7.95916724596617 $$   |

$$
\begin{aligned}
\text{P Value for Bonnie MO Means (AI 19 and 20)} &= 6.918448031273796e-32 \\
\text{P Value for Chica MO Means (AI 19 and 20)} &= 1.0824275002262571e-05
\end{aligned}
$$

Now both p-values are well under our $0.01$ cut-off, by a couple order of magnitudes. It took increasing the total sample size by a couple orders of magnitude, or many in the case for Bonnie. Like last time, there are pretty big deviations in the p-value depending on the seed, so the ones that you're seeing are the result of running 5 different $1,000,000$ sized simulations and taking the simulation that contained the largest p-value. This was my attempt at getting to a pretty confident answer while accounting for the deviations in the p-values. 

It should be noted that the data here are a different data set from what was seen in the results section, but behaves in a vastly similar way. I did not include the graphs for this as they look exactly the same, but just with much more data points. Mostly leaving this here, because this action would *definitely* not fly in a peer reviewed paper, but to be honest, I have no idea the proper actions outside of what I chose to do since the data sets are generated and not taken from a population. 

### Outliers
This will be less formal, but something I wanted to touch on. I'll talk a bit more about the general implied difficulty of this, but I wanted to at least mention before I get too far. The trend of the outliers for the data slowly get more compressed as the AI value for both Bonnie and Chica increase. The outliers themselves seem to peak for the lower AI values, which makes sense to some extent. The AI values are low enough where it is easier for Bonnie and Chica to stay at the door, but not low enough for them to never get there. In fact, the longest time spent at the door happens when Bonnie's AI value is at 3 and when Chica's AI value is at 2. In general, it also happens that the highest chance of getting an animatronic to stay at the door for long periods of time only happens at low AI values. For example, while they are outliers, the only AI values that have nights where Bonnie or Chica remain at the door for longer than 40 MOs are below 5, while this effectively never happens for larger AI values (keep in mind, these outliers were found when doing $100,000$ simulations for each AI value).

### Pitfalls of Simulation
Believe it or not, this simulation isn't perfect. These pitfalls of this simulation are a mix of changes I either do not know how to fix or was too lazy to implement.

#### Game vs Python Randomness
I have no idea how this one is impacted on the simulation, but it should be noted that the random numbers generated by Python is not exactly the same as Click Team Fusion. Technically, this could deviate in a number of ways, but I don't know nearly enough about random numbers in Click Team Fusion to say how it is impacted. If I had to guess, it is mostly similar to each other, but it's at least something to keep in mind.

#### Movement Delay Glitch
I knew about this before making the simulation, but chose not to implement it because I was lazy. Basically, in Five Nights at Freddy's Bonnie and Chica share the same variable that stores the random number that chooses whether they move or not. The program first calculates Chica's move and then overwrites the value with Bonnie's move. This is fine for a vast majority of the program, but for times where Bonnie's and Chica's MO overlap on intervals smaller than a frame, if Chica has a successful movement opportunity, then the program won't have time to calculate Bonnie's and thus Bonnie doesn't move. You can see this yourself if you set both Bonnie and Chica to an AI value of 20. Theoretically, both Bonnie and Chica will move on the first MO, but because of this glitch, Chica will move forward and Bonnie will stay on stage. I am fairly certain that this glitch will only happen on the first MO, but nonetheless I was too lazy to implement it and the plots don't show this. That begin said, I doubt it would change much, but it would destroy the fact that Bonnie and Chica's movements are independent of each other which would be a monumental hassle, so I assumed otherwise (especially since it's effectively true, kind of like ignoring air friction).

#### Difficulty
This is less about the simulation and more about the premise behind it. Throughout this entire process, I assumed that the most difficult setting is when Bonnie and Chica are at your door, but I don't think this is entirely true. For example, if Bonnie and Chica rush to your door as soon as possible and stay there, the optimal play is to just close the doors and wait. That doesn't scream difficulty to me, more so just putting you in an impossible situation. But as mentioned before, for higher AI values, if you know they're going to leave immediately, what's the difficulty if they're so predictable? All this is to say, I don't think this is a perfect measure of difficulty, and maybe we're barking up the wrong tree because the difficulty doesn't actually change with AI value when you get high enough. The strategy for beating the night doesn't change, just how lucky you are to finish. That being said, I do think if you're going to try and measure the difficulty then this is the best way to do it, but I completely understand how people would say otherwise.

## Conclusion

I had a lot of fun on this investigation and learned a great deal about the original FNAF game than I originally anticipated. Truthfully, I went in thinking (and hoping) that the most difficult AI value would in fact be 19 or 18 or something similar, but I believe that the results show otherwise. I mentioned this in the [Difficulty](#difficulty) section, but I personally believe that this is one of the better ways to measure difficulty for this game (if it can be measured). I think the *best* way would be to be combining time spent at the door along with frequent trips to the door, but I daresay the end result would be the same. The results show that the hardest measurable AI value for both Bonnie and Chica ends up being 20 for both of them, even if the difference between 20 and 19 is so miniscule that we had to greatly increase the number of simulated nights to show it. 

Besides the pitfalls mentioned previously, I do want to at least point out that lower AI values *do* have a higher chance of producing situations. Looking at the plots, the outliers for an AI value of 19 reach higher than the highest outliers for an AI value of 20. However, I think it's a bit unfair to focus on the outliers for examples like this, as technically, you could argue that an AI value of 2 for Bonnie and 3 for Chica would be the hardest as they have the highest chance out of all to have insane times spent at the door. Moreover, an AI value of 19 has a much higher chance of rolling lower MOs spent at the door than an AI value of 20, as the lower outliers for 19 are smaller than the lowest outlier for 20. All this is to say that, on average, an AI value for 20 (for both Bonnie and Chica) shows the highest mean time spent at the door, but also the most consistent. Lowering the AI value will not increase the average time spent at the door, just increase your likelihood of having more difficult nights, but will also increase your likelihood of having easier nights. Does that make it more difficult? In my personal opinion no (mostly due to the mean), but at the end of the day, it's entirely up to you.

## References

### Python Libraries
1. Matplotlib for plots: [J. D. Hunter, "Matplotlib: A 2D Graphics Environment", Computing in Science & Engineering, vol. 9, no. 3, pp. 90-95, 2007](https://doi.org/10.1109/MCSE.2007.55)
2. Numpy for math: Harris, C.R., Millman, K.J., van der Walt, S.J. et al. _Array programming with NumPy_. Nature 585, 357–362 (2020). DOI: [10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2). ([Publisher link](https://www.nature.com/articles/s41586-020-2649-2))
3. Scipy for statistics: Pauli Virtanen, Ralf Gommers, Travis E. Oliphant, Matt Haberland, Tyler Reddy, David Cournapeau, Evgeni Burovski, Pearu Peterson, Warren Weckesser, Jonathan Bright, Stéfan J. van der Walt, Matthew Brett, Joshua Wilson, K. Jarrod Millman, Nikolay Mayorov, Andrew R. J. Nelson, Eric Jones, Robert Kern, Eric Larson, CJ Carey, İlhan Polat, Yu Feng, Eric W. Moore, Jake VanderPlas, Denis Laxalde, Josef Perktold, Robert Cimrman, Ian Henriksen, E.A. Quintero, Charles R Harris, Anne M. Archibald, Antônio H. Ribeiro, Fabian Pedregosa, Paul van Mulbregt, and SciPy 1.0 Contributors. (2020) **SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python**. _Nature Methods_, 17(3), 261-272. DOI: [10.1038/s41592-019-0686-2](https://doi.org/10.1038/s41592-019-0686-2)

### Images
1. 

