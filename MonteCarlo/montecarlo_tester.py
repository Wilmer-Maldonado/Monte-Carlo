import pandas as pd
import numpy as np
from MonteCarlo import Die
from MonteCarlo import Game
from MonteCarlo import Analyzer
import unittest

class MonteCarloTestSuite(unittest.TestCase):
    '''
        PURPOSE: Tests each method in each class to validate methods receive correct inputs and return valid outputs.
                 Tests build on each other, Die objects used for Game object, and Game object used for Analyzer class.
                 This validates all classes are working properly and not erroring upon use of classes and attributes.
    '''
    #DIE CLASS TESTS
    def test_1_change_wt(self):
        '''
        PURPOSE: Test 1 change_wt method, verifying only a incorrect entry message is outputted
                 but test does not raise an Error. Incorrect entry message occurs,
                 when face passed is not in Die object dataframe's faces column.
                 
                 Incorrect entry message: "Face entered not in Die!"
        '''
        # Create Die instance
        global six_sided
        six_sided=Die(np.array(["one", "two", "three", "four", "five", "six"]))
        six_sided.change_wt("eight", 1.0)
        self.assertTrue("eight" not in six_sided.current_die()['faces'][:])
        
    def test_2_change_wt(self):
        '''
        PURPOSE: Test 2 change_wt method, verifying only a incorrect entry message is outputted,
                 but test does not raise an Error. Incorrect entry message occurs
                 when new_weight passed is not float, and cannot be converted to float.
                 
                 Incorrect entry message: "New Weight is not float, and can't be converted to float"
        '''
        # uses six_sided Die object.
        err_output2 = six_sided.change_wt("four", 'x')
        #Test-check new weight, 'x', passed cannot be converted to float
        #err_output2 should match message in expected variable
        self.assertTrue("x" not in six_sided.current_die()['weights'][:])
    
    def test_3_change_wt(self):
        '''
        PURPOSE: Test 3 change_wt method, verifying when change_wt method is called,
                 dataframe containing face and weights updated accordingly.
        '''
        # uses six_sided Die object
        six_sided.change_wt("one", "3")
        six_sided.change_wt("three", 4)
        six_sided.change_wt("six", 2.7)
        #checks weight column to see if changes were made accordingly
        #unchanged weights remain 1.0, changed weights from above reflected in list as floats
        expected = [3.0,1.0,4.0,1.0,1.0,2.7]
        self.assertEqual(list(six_sided.current_die()['weights']), expected)
        
    def test_4_roll_die(self):
        '''
        PURPOSE: Test 4 roll_die method, verifies there is an outcome for each roll in list,
                 when roll_die method is used. Matches list length of outcomes with num_rolls argument.
        '''
        # uses six_sided Die object
        list_roll_outcomes = six_sided.roll_die(10)
        #Test-check length of outputted list from roll_die method matches argument # of rolls
        self.assertTrue(len(list_roll_outcomes)==10)
        
    def test_5_current_die(self):
        '''
        PURPOSE: Test 5 current_die method, verifying updated dataframe of Die object containing faces and weights,
                 has updated weights after change_wt method used in test_3_change_wt.
        '''
        # uses six_sided Die object
        output_die_df = six_sided.current_die()
        #made expected df of six_sided object
        expected = pd.DataFrame({'faces': np.array(["one", "two", "three", "four", "five", "six"]) , 
                                 'weights': np.array([3.0,1.0,4.0,1.0,1.0,2.7])})
        # Test-check if expected df matches df output when current_die method is called
        self.assertTrue((list(output_die_df['faces']) == list(expected['faces'])) &
                       (list(output_die_df['weights']) == list(expected['weights'])))
    #GAME CLASS TESTS
    def test_6_play(self):
        '''
        PURPOSE: Test 6 play method, verifying list of Die objects can be passed to game class.
                 And play method results dataframe's shape matches expected shape of N rolls by M dice.
        '''
        #all_six_sided is list of already instantiated similar Die objects
        six_sided1=Die(np.array(["one", "two", "three", "four", "five", "six"]))
        six_sided2=Die(np.array(["one", "two", "three", "four", "five", "six"]))
        six_sided3=Die(np.array(["one", "two", "three", "four", "five", "six"]))
        all_six_sided=[six_sided1, six_sided2, six_sided3]
        #game1 is Game class object
        global game_1
        game_1 = Game(all_six_sided)
        rolls_play=20
        game_1.play(rolls_play)
        #to verify play method must call show method since play method has no public attribute for play results
        #show method by default contains results from play 
        #and Test-check shape of play results to see if it matches 20 rolls by 3 Die objects as expected
        #will test play() further using show method with 'wide' argument in next test
        #since show('wide') contains public attribute directly displaying play() df stored in private attribute
        expected = game_1.show().shape
        self.assertEqual((rolls_play, len(all_six_sided)), expected)
        
    def test_7_show(self):
        '''
        PURPOSE: Test 7 show method, verifies structure is correct for resulting dataframe of play results.
                 Specifically, index_name is only roll_number for 'wide' form.
        '''
        #game1 is class object
        play_results_wide_df = game_1.show('wide')
        #test-check if index name is roll_number
        self.assertTrue(play_results_wide_df.index.name == 'roll_number')
        
    def test_8_show(self):
        '''
        PURPOSE: Test 8 show method, verifies structure is correct for resulting dataframe of play results.
                 Specifically, if 'narrow' form has roll_number and die_number as two-columned index.
        '''
        #game1 is class object
        play_results_narrow_df = game_1.show('narrow')
        #test-check if index name is roll_number and die_number for narrow format
        self.assertTrue(play_results_narrow_df.index.names == ['roll_number', 'die_number'])
    
    def test_9_show(self):
        '''
        PURPOSE: Test 9 show method, verifies structure is correct for resulting dataframe of play results.
                 Specifically, shape matches expected for narrow format two column index.
                 number of rows is equal to number of rolls times number of die.
                 only 'face_rolled' is a column, roll number and die number are indexes and not included in shape
        '''
        #game1 is class object
        play_results_narrow_df = game_1.show('narrow')
        #test-check shape matches expected for narrow format
        #two column index, do not count as columns when calling df.shape, so only 'face_rolled' is a column
        #number of rows is equal to 20 rolls times 3 die so 60 rows in narrow format for game1 object
        self.assertTrue(play_results_narrow_df.shape == (60,1))
        
    def test_10_jackpot(self):
        '''
        PURPOSE: Test 10 jackpot method, verifies Analyzer class can take game object as argument.
                 test also checks return from jackpot method is integer, 
                 representing number of times a roll resulted in all dice having same face outcome.
        '''
        #Analyzer class takes game1 Game class object from previous tests as argument
        global analyzer1
        analyzer1 = Analyzer(game_1)
        #Test checks if return from jackpot method is integer
        self.assertTrue(type(analyzer1.jackpot()) == int)
    
    def test_11_jackpot(self):
        '''
        PURPOSE: Test 11 jackpot method, verifies public attribute jackpot_df can be called and has correct structure.
                 Specifically, roll_number is index.      
        '''
        #analyzer1 as Analyzer class object
        #checks dataframe for public attribute self.jackpot_df is indexed by roll_number
        #if calling index.names works then public attribute .jackpot_df output is also valid data frame
        self.assertTrue(analyzer1.jackpot_df.index.name == 'roll_number')
        
    def test_12_combo(self):
        '''
        PURPOSE: Test 12 combo method, verifies combo method can be called and creates public attribute .combo_df.
                 .combo_df should have multi-columned index and  test verifies one column for count. 
        '''
        #calling analyzer method combo
        analyzer1.combo()
        #Test checks only if public attribute .combo_df is valid
        #and if number of columns is 1, for count
        #all other columns should be index columns, so are not counted in .columns
        self.assertTrue(len(list(analyzer1.combo_df.columns)) == 1 )
        
    def test_13_face_counts_per_roll(self):
        '''
        PURPOSE: Test 13 face_counts_per_roll method, verifies face_counts_per_roll can be called
                 and shape of resulting dataframe stored in public attribute .face_counts_df matches expected.
                 Specifically, shape should be N rolls by M faces.      
        '''
        #calls face_counts_per_roll method under Analyzer class
        analyzer1.face_counts_per_roll()
        #each die of same kind have 6 faces, so shape should be 20 rolls, by 6 faces
        expected_shape = (20, 6)
        #if test passes below, it is also valid that face_counts_df is a public attribute
        self.assertEqual(analyzer1.face_counts_df.shape, expected_shape)
        
        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MonteCarloTestSuite('test_1_change_wt'))
    suite.addTest(MonteCarloTestSuite('test_2_change_wt'))
    suite.addTest(MonteCarloTestSuite('test_3_change_wt'))
    suite.addTest(MonteCarloTestSuite('test_4_roll_die'))
    suite.addTest(MonteCarloTestSuite('test_5_current_die'))
    suite.addTest(MonteCarloTestSuite('test_6_play'))
    suite.addTest(MonteCarloTestSuite('test_7_show'))
    suite.addTest(MonteCarloTestSuite('test_8_show'))
    suite.addTest(MonteCarloTestSuite('test_9_show'))
    suite.addTest(MonteCarloTestSuite('test_10_jackpot'))
    suite.addTest(MonteCarloTestSuite('test_11_jackpot'))
    suite.addTest(MonteCarloTestSuite('test_12_combo'))
    suite.addTest(MonteCarloTestSuite('test_13_face_counts_per_roll'))
    unittest.TextTestRunner(verbosity=3).run(suite)