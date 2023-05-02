## Monte-Carlo Repo

# <u>Metadata</u>
* Project Name: **MonteCarlo Simulator**
* Creation Date: 05/02/2023
* Author Name: Wilmer Maldonado
* Author ID: etc7fq
* GitHub Repo URL: https://github.com/Wilmer-Maldonado/Monte-Carlo


# <u>Synopsis</u>

Installing Package:
* MonteCarlo Folder in Monte-Carlo Directory holds module package files:
    * \_\_init\_\_py, setup.py, MonteCarlo.py, montecarlo_tester.py
* First, to install package clone Monte-Carlo repo
* Second, set directory to /Monte-carlo
* Third, execute -> !cd MonteCarlo/; pip install -e .

Importing Package:
* Once MonteCarlo package is installed, can import package and all its classes by executing:
    * execute -> from MonteCarlo import \*
* Three classes in Module: Die, Game, Analyzer, import a specific class from package by executing:
    * execute -> from MonteCarlo import Die
    * execute -> from MonteCarlo import Game
    * execute -> from MonteCarlo import Analyzer
    
Creating Dice Demo:
* After package imported, can start creating Die class objects.
    * execute -> die1 = Die(np.array([1, 2, 3]))
                 die2 = Die(np.array([1, 2, 3]))
                 die3 = Die(np.array([1, 2, 3]))
                 
* To change weight associated with the face of a Die object
    
    For example, to change weight of face 2 of die2 to 1.5:
    * execute -> die2.current_wt(2, 1.5)

Playing Games Demo:
* Use die objects from above die1, die2, die3, to create instance of Game class:
    * Pass list of die objects into Game class:
        * execute -> game1 = Game([die1, die2, die3])
* To create a play event, use play method under Game class:
    * Pass total number of desired rolls in play event, For example 20 rolls:
        * execute -> game1.play(20)
* Stores most recent play event results, use show method under Game class to display results.
    * If you want play results in 'wide' format pass 'wide' into show method (Note: defaults to 'wide' with no arg):
        * execute -> game1.show('wide')
    * if you want play results in 'narrow' format:
        * execute -> game1.show('narrow')

Analyzing Games Demo:
* Use Game object frome above, game1, to create instance of Analyzer class:
    * Pass Game object, game1 into Analyzer class:
        * execute -> analyzer1 = Analyzer(game1)
* To get number of jackpots in game1, all faces in a roll of similar dice identical:
    * Utilize jackpot method under Analyzer class:
        * execute -> analyzer1.jackpot()
    * To get dataframe in wide format of jackpot rows, use attribute jackpot_df:
        * execute -> analyzer1.jackpot_df
* To get dataframe with distinct combinations of rolls in a Game as multi-columned index, along with a counts column.
    * utilize combo method under Analyzer class:
        * execute -> analyzer1.combo()
                     analyzer1.combo_df
* To get dataframe with face counts per roll in a game, with roll number as index, faces as columns.
    * Utilize face_counts_per_roll method under Analyzer class:
        * execute -> analyzer1.face_counts_per_roll()
                     analyzer1.face_counts_df

# <u>API Description</u>

All classes with their public methods and attributes:

Note: Below each class and method
* docstring
* input parameters and their descriptions (datatypes and defaults) under INPUT information
* Public attributes and their descriptions under OUTPUT information
* return values described under OUTPUT information
* Included private attribute description if they are integral or are the return value of a method

class Die:

    PURPOSE: Given an array of faces, creates a Die class object.
    Die class object contains the Die's faces and corresponding weights.
    Also, can random sample from the vector of faces according to weights,
    to simulate rolling of die, and returns each roll's outcomes in list.
    
    INPUT
    array    array of faces
    
    OUTPUT
    Die      Die class object
    
    
def change_wt(self, face, new_weight):
    
    PURPOSE: Given face in instantiated Die object and desired weight for face,
    updates Die's dataframe for faces and weights accordingly.

    INPUT- arguments for method
    face <- face in instantiated Die object
    new_weight <- desired new weight for face in argument


    OUTPUT- outputs and attributes
    face Argument Error message <- if face passed not in Die's array of faces/weights,
    returns "Face entered not in Die!"

    new_weight Argument Error message <- if new_weight passed is not a float and cannot be converted to float, 
    returns "New Weight is not float, and can't be converted to float"

    self.__faces_weights <- private attribute/dataframe updated with new_weight for face argument
       

def roll_die(self, num_rolls=1):

    PURPOSE: Given number of rolls, returns outcome of each roll in list.
             Roll is simulated by random sample of face vector according to weights.
             Does not internally store results.

    INPUT- arguments for method
    num_rolls <- number of rolls, defaults to number of rolls = 1

    OUTPUT- outputs and attributes
    
def current_die(self):
        
    PURPOSE: Method returns Die class object's most current dataframe of faces and associated weights.

    INPUT- self argument only, ex. die_object.current_die()

    OUTPUT- outputs and attributes
    self.__faces_weights <- returns current private attribute/dataframe,
                            if applicable with updates made by change_wt method.
        

class Game:

    PURPOSE: Given a list of already instantiated similar Die objects 
    (similar means same number of sides and associated faces), 
    returns Game class object. Each Die object may have different weights.
    Die class object contains the Die's faces and corresponding weights.
    Also, can random sample from each die's vector of faces according to weights,
    to simulate rolling od dice. Stores most recent results of play.
    
    INPUT
    die_list    list of already instantiated similar Die objects.
    
    OUTPUT
    Game        Game class object
    
    
def play(self, total_rolls=1):
    
    PURPOSE: Stores face outcome of all dice for each roll in private dataframe, 
             given number of total desired rolls. Dataframe has shape N rolls by M dice.


    INPUT- arguments for method
    total_rolls <- defaults to 1, total rolls desired for play event with Dice in Game class object.

    OUTPUT- outputs and attributes
        self.__results <- private dataframe with play event results,
                          contains columns for roll number and die number, with corresponding face rolled as values. 
                          shape N rolls by M dice.

def show(self, form = 'wide'):
    
    PURPOSE: Displays dataframe containing results of most recent play.
             Format of play results dataframe depends on parameter value of 'wide' or 'narrow'.

    INPUT- arguments for method
    form <- can be 'narrow' or 'wide to designate desired format of most recent play results.
            defaults as 'wide'.

    OUTPUT- outputs and attributes
    'narrow' form play results dataframe <- two column index with roll number and die number, and a column for face rolled

    'wide' form play results dataframe <- single column index with roll number, and each die number as a column


class Analyzer:
    
    PURPOSE: Given a single Game class object, computes various
    descriptive statistical properties about it.
    
    INPUT
    game_obj      Game class object    
    
    OUTPUT
    Analyzer      Analyzer class object
    
def jackpot(self):
    
    PURPOSE: computes how many times the game resulted in all faces being identical. 

    INPUT- self argument only, ex. game_object.jackpot()

    OUTPUT- outputs and attributes
    self.jackpot_df <- public attribute stores rolls in game which resulted in all identical faces.
                       roll number as named index.

    len(self.jackpot_df) <- how many times a roll in a game resulted in identical faces,
                            computed by getting number of rolls in self.jackpot_df using len()
                
def combo(self):

    PURPOSE: Given instantiated game class object, 
             computes the distinct combinations of faces rolled, along with their counts. 

    INPUT- self argument only, ex. game_object.combo()

    OUTPUT- outputs and attributes
    self.combo_df <- public attribute containing dataframe,
                     with distinct combinations of faces rolled in game as a multi-columned index.
                     And a column containing counts of each combination.
        
def face_counts_per_roll(self):
    
    PURPOSE: computes how many times a given face is rolled in each game event. 

    INPUT- self argument only, ex. game_object.face_counts_per_roll()

    OUTPUT- outputs and attributes
    self.face_counts_df <- public attribute storing dataframe displaying counts 
                           of each face for each roll in a game event.
                           Index of roll number and face values as columns(i.e. it is 'wide' form)



# <u>Manifest</u>

Monte-Carlo Repo:

* MonteCarlo package folder -> description: MonteCarlo package
    * \_\_init\_\_.py
    * setup.py
    * MonteCarlo.py
    * montecarlo_tester.py

* FinalProjectV1.ipynb -> description: FINAL PROJECT SUBMISSION JUPYTER NOTEBOOK W/ SCENARIO SCRIPT

* montecarlo_testresults.txt -> description: command line results of MonteCarlo unittest tester module

* MIT LICENSE -> description: permissive License for open source software

* README.md -> description: Contains detailed information on every file and module in Monte-Carlo Repo


