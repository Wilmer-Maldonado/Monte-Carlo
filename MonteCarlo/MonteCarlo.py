import pandas as pd
import numpy as np

class Die:
    '''
    PURPOSE: Given an array of faces, creates a Die class object.
    Die class object contains the Die's faces and corresponding weights.
    Also, can random sample from the vector of faces according to weights,
    to simulate rolling of die, and returns each roll's outcomes in list.
    
    INPUT
    array    array of faces
    
    OUTPUT
    Die      Die class object
    '''
    def __init__(self, array) :
        '''
        PURPOSE: Creates instance of Die object, by receiving argument of array of Die's faces.
        Weights of faces internally initializes as 1.0 for each face.
        Stores both faces and weights into a Private Dataframe, to be used in other methods.

        INPUT- arguments for method
        array      array of faces   

        OUTPUT- outputs and attributes
        self.__faces_weights <- private attribute/dataframe with Die object's faces and weights
                                to be used in other Die class methods.
        '''
        weights = np.array([1.0 for elem in array])
        self.__faces_weights = pd.DataFrame({'faces': array , 'weights': weights})
    
    def change_wt(self, face, new_weight):
        '''
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
        '''
        try:
            assert face in list(self.__faces_weights['faces'][:]), "Face entered not in Die!"
            type(float(new_weight))== float
            self.__faces_weights.loc[self.__faces_weights['faces'] == face, 'weights'] = float(new_weight)
        except AssertionError as e:
            print(e)
        except ValueError:
            print("New Weight is not float, and can't be converted to float")
            
    def roll_die(self, num_rolls=1):
        '''
        PURPOSE: Given number of rolls, returns outcome of each roll in list.
                 Roll is simulated by random sample of face vector according to weights.
                 Does not internally store results.

        INPUT- arguments for method
        num_rolls <- number of rolls, defaults to number of rolls = 1
           
        OUTPUT- outputs and attributes
        allrolls <- face outcome of each roll in list
        '''
        allfaces = self.__faces_weights['faces']
        allweights = self.__faces_weights['weights']
        allrolls = []
        while num_rolls>0:
            allrolls.append(list(allfaces.sample(weights = allweights))[0])
            num_rolls+=-1
        return allrolls
    
    def current_die(self):
        '''
        PURPOSE: Method returns Die class object's most current dataframe of faces and associated weights.

        INPUT- self argument only, ex. die_object.current_die()

        OUTPUT- outputs and attributes
        self.__faces_weights <- returns current private attribute/dataframe,
                                if applicable with updates made by change_wt method.
        '''
        return self.__faces_weights


class Game:
    '''
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
    '''
    def __init__(self, die_list):
        '''
        PURPOSE: Creates instance of Game class object, given list of already instantiated similar Die objects. 

        INPUT- arguments for method
        die_list <- list of already instantiated similar Die objects
           
        OUTPUT- outputs and attributes
        self.__dice <- private attribute containing list of Die objects.
                       Used in other methods for Game class.
        '''
        self.__dice = die_list#assumes argument is list of Die objects
    
    def play(self, total_rolls=1):
        '''
        PURPOSE: Stores face outcome of all dice for each roll in private dataframe, 
                 given number of total desired rolls. Dataframe has shape N rolls by M dice.
                 

        INPUT- arguments for method
        total_rolls <- defaults to 1, total rolls desired for play event with Dice in Game class object.
           
        OUTPUT- outputs and attributes
        self.__results <- private dataframe with play event results,
                          contains columns for roll number and die number, with corresponding face rolled as values. 
                          shape N rolls by M dice.
        '''
        results = pd.DataFrame(index=range(1, total_rolls+1), 
                          columns=[i for i in range(0, len(self.__dice))])
        results.index.name = 'roll_number'
        for i, die in enumerate(self.__dice):
            results[i] = die.roll_die(total_rolls)
        self.__results = results
    
    def show(self, form = 'wide'):
        '''
        PURPOSE: Displays dataframe containing results of most recent play.
                 Format of play results dataframe depends on parameter value of 'wide' or 'narrow'.

        INPUT- arguments for method
        form <- can be 'narrow' or 'wide to designate desired format of most recent play results.
                defaults as 'wide'.
                
        OUTPUT- outputs and attributes
        'narrow' form play results dataframe <- two column index with roll number and die number, and a column for face rolled
        
        'wide' form play results dataframe <- single column index with roll number, and each die number as a column
        '''
        try:
            assert form == 'wide' or form == 'narrow', "Invalid option, pass 'wide' or 'narrow' as argument!"
            if form == 'wide':
                return self.__results
            else:
                narrow = self.__results.reset_index()
                narrow1 = narrow.melt(id_vars='roll_number', var_name='die_number', value_name='face_rolled').set_index('roll_number')
                narrow2 = narrow1.set_index('die_number', append=True)
                return narrow2
        except AssertionError as e:
            print(e)


class Analyzer:
    '''
    PURPOSE: Given a single Game class object, computes various
    descriptive statistical properties about it.
    
    INPUT
    game_obj      Game class object    
    
    OUTPUT
    Analyzer      Analyzer class object
    '''
    def __init__(self, game_obj):
        '''
        PURPOSE: Creates instance of Analyzer class object, given instantiated Game class object. 

        INPUT- arguments for method
        game_obj <- instantiated Game class object
           
        OUTPUT- outputs and attributes
        self.__game <- private attribute containing argument of instantiated Game class object.
                       Used in other methods for Analyzer class.
        '''
        self.__game= game_obj
    
    def jackpot(self):
        '''
        PURPOSE: computes how many times the game resulted in all faces being identical. 

        INPUT- self argument only, ex. game_object.jackpot()
           
        OUTPUT- outputs and attributes
        self.jackpot_df <- public attribute stores rolls in game which resulted in all identical faces.
                           roll number as named index.
        
        len(self.jackpot_df) <- how many times a roll in a game resulted in identical faces,
                                computed by getting number of rolls in self.jackpot_df using len()
        '''
        wide_results=self.__game.show().copy(deep=True)
        jackpot_filter = wide_results.apply(lambda row: row.nunique() == 1, axis=1)
        self.jackpot_df = wide_results[jackpot_filter]
        return len(self.jackpot_df)
                
    def combo(self):
        '''
        PURPOSE: Given instantiated game class object, 
                 computes the distinct combinations of faces rolled, along with their counts. 

        INPUT- self argument only, ex. game_object.combo()
           
        OUTPUT- outputs and attributes
        self.combo_df <- public attribute containing dataframe,
                         with distinct combinations of faces rolled in game as a multi-columned index.
                         And a column containing counts of each combination.
        '''
        intial_df = self.__game.show().copy(deep=True)
        df2 = intial_df.apply(lambda x: tuple(sorted(tuple(x))), axis=1)
        #returns series so converted back to dataframe below
        df3 = pd.DataFrame({'roll_number':df2.index, 'combinations':df2.values}).set_index('roll_number')
        #getting counts
        freq = df3.apply(lambda x: tuple(x), axis=1).value_counts()
        df3['counts'] = df3.apply(lambda x: freq[tuple(x)], axis=1)
        #dropping extras now that counts has been made
        df3 = df3.drop_duplicates()
        #making tuples index instead of roll_number
        df3 = df3.set_index('combinations')
        # Index column combination tuples into MultiIndex
        new_index = pd.MultiIndex.from_tuples(df3.index)
        # Set multiindex as new index
        df3.index = new_index
        #get number of levels
        num_levels = df3.index.nlevels
        # sort multi index based on c=index column 0,1,2
        df3 = df3.sort_index(level=[x for x in range(0, num_levels)])
        self.combo_df = df3
        
    def face_counts_per_roll(self):
        '''
        PURPOSE: computes how many times a given face is rolled in each game event. 

        INPUT- self argument only, ex. game_object.face_counts_per_roll()
           
        OUTPUT- outputs and attributes
        self.face_counts_df <- public attribute storing dataframe displaying counts 
                               of each face for each roll in a game event.
                               Index of roll number and face values as columns(i.e. it is 'wide' form)
        '''
        show_results= self.__game.show().copy(deep=True)
        face_counts_df=show_results.apply(pd.Series.value_counts, axis=1)
        self.face_counts_df=face_counts_df.fillna(0)