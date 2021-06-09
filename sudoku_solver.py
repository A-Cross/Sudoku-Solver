import numpy as np
import copy
import random

class sudoku_state:
    def __init__(self, board):
        self.board = board
    
    def is_goal(self):
        """Checks if the state produced is the goal state."""
        if 0 in self.board:
            is_goal = False
        else:
            is_goal = True
        
        return is_goal
    
    def is_invalid(self, dictionary):
        """Checks if the board is invalid e.g. numbers appearing twice in a row or column or square."""
        flag = False
        rows = range(0,9)
        board = self.board
        dic = dictionary
        
        if dic == False:
            flag = True
        
        if not bool(dic) and np.isin(0, board):
            flag = True
        
        if self == None:
            flag = True
        
        for row in rows:
            row_test = board[row]
            index = np.array([0])
            row_test_no_zeros = np.setdiff1d(row_test,index,True)
            if len(np.unique(row_test_no_zeros)) != len(row_test_no_zeros):
                flag = True
            else:
                continue
        
        for key in dic:
            check = dic.get(key)
            if len(check) == 0:
                flag = True
                
        return flag
    
    def row_finder(self, state):
        """Checks each row for 0 and adds each row containing a 0 to a list."""
        rows = range(0,9)
        rows_with_zero = []
        for row in rows:
            row_check = state[row]
            if np.isin(0, row_check):
                rows_with_zero.append(row)
            else:
                continue
              
        return rows_with_zero
    
    
    
    def valid_value(self, state, row, column, value, dictionary):
        """Checks if the value is valid. If setting a value means that an empty cell will not 
           have any possible values left, then that value is invalid."""
        is_valid = True

        rows, columns = square_finder(row, column)
        for key in dictionary:
            if key[0] == row and key[1] == column:
                continue

            if key[0] == row:
                value_list = dictionary.get(key)
                if len(value_list) == 1 and value in value_list:
                    is_valid = False

            if key[1] == column:
                value_list = dictionary.get(key)
                if len(value_list) == 1 and value in value_list:
                    is_valid = False

            if key[0] in rows and key[1] in columns:
                value_list = dictionary.get(key)
                if len(value_list) == 1 and value in value_list:
                    is_valid = False
        
        return is_valid
    
def square_slice(state, row, column):
    """Obtains the 3x3 square the cell is in and returns it."""
    array = state
    if row < 3:
        if column < 3:
            square_slice = array[0:3, 0:3]
        if 2 < column <6:
            square_slice = array[0:3, 3:6]
        if column > 5:
            square_slice = array[0:3, 6:9]
    elif 2 < row < 6:
        if column < 3:
            square_slice = array[3:6, 0:3]
        if 2 < column <6:
            square_slice = array[3:6, 3:6]
        if column > 5:
            square_slice = array[3:6, 6:9]
    elif 5 < row:
        if column <3:
            square_slice = array[6:9, 0:3]
        if 2 < column <6:
            square_slice = array[6:9, 3:6]
        if column > 5:
            square_slice = array[6:9, 6:9]

    return square_slice

def row_missing_values(state, row):
    """Finds the missing values in the row"""
    row_missing_values = []
    for i in range(1,10):
        if np.isin(i, state[row]):
            continue
        else:
            row_missing_values.append(i)

    return row_missing_values

def column_missing_values(state, column):
    """Finds missing values in the column."""
    columns_missing = []
    col = state[:, column]
    for i in range(1,10):
        if np.isin(i, col):
            continue
        else:
            columns_missing.append(i)

    return columns_missing

def square_missing_values(state, row, column):
    """Finds the missing values in each sub-square."""
    square = square_slice(state, row, column)
    square_missing = []
    for i in range(1,10):
        if np.isin(i, square):
            continue
        else:
            square_missing.append(i)

    return square_missing
    

def cells_dictionary(board):
    """Produces a dictionary of cell coordinates paired to potential cell values."""
    cell_list = []
    cell_missing_list = []
    rows = range(0,9)
    columns = range(0,9)

    for row in rows:
        for column in columns:
            if board[row][column] == 0:
                cell = (row, column)
                cell_list.append(cell)

                row_missing = set(row_missing_values(board, row))
                col_missing = set(column_missing_values(board, column))
                square_missing = set(square_missing_values(board, row, column))
                sets_intersection = row_missing.intersection(col_missing)
                second_sets_intersection = square_missing.intersection(sets_intersection)
                cell_missing = sorted(list(second_sets_intersection))
                cell_missing_list.append(cell_missing)

    cell_dictionary = dict(zip(cell_list, cell_missing_list))
    return cell_dictionary

def cell_dictionary_shortest(dictionary):
    """Returns a list of keys with shortest length values."""
    min_val = min([len(dictionary[key]) for key in dictionary])
        
    min_value_list = [] 
    for key in dictionary: 
        if len(dictionary[key]) == min_val: 
            min_value_list.append(key)
    
    return min_value_list

def square_finder(row, column):
    """Returns lists of the row and column values for the square a cell is located in."""
    if row < 3:
        if column < 3:
            rows = [0,1,2]
            columns = [0,1,2]
        if 2 < column < 6:
            rows = [0,1,2]
            columns = [3,4,5]
        if 5 < column < 9:
            rows = [0,1,2]
            columns = [6,7,8]
    elif 2 < row < 6:
        if column < 3:
            rows = [3,4,5]
            columns = [0,1,2]
        if 2 < column < 6:
            rows = [3,4,5]
            columns = [3,4,5]
        if 5 < column < 9:
            rows = [3,4,5]
            columns = [6,7,8]
    elif 5 < row < 9:
        if column < 3:
            rows = [6,7,8]
            columns = [0,1,2]
        if 2 < column < 6:
            rows = [6,7,8]
            columns = [3,4,5]
        if 5 < column < 9:
            rows = [6,7,8]
            columns = [6,7,8]
    
    return rows, columns

def cell_dictionary_updater(dictionary, row, column, value):
    """After a value has been found to be valid, this method updates the dictionary.
       Possible values for cells in the same row, column and square as the cell being 
       changed are updated to remove the value being assigned."""
    rows, columns = square_finder(row, column)
    dictionary_copy = copy.deepcopy(dictionary)
    for key in dictionary:
        if key[0] == row and key[1] == column:
            del dictionary_copy[key]
        
        if key[0] == row:
            value_list = dictionary.get(key)
            if value in value_list:
                x = dictionary_copy.get(key)
                if x == None:
                    continue
                if len(x) == 0:
                    continue
                elif value in x:
                    x.remove(value)
                    if len(x) == 0:
                        del dictionary_copy[key]
                
        if key[1] == column:
            value_list = dictionary.get(key)
            if value in value_list:
                value_list.remove(value)
                x = dictionary_copy.get(key)
                if x == None:
                    continue
                if len(x) == 0:
                    continue
                elif value in x:
                    x.remove(value)
                    if len(x) == 0:
                        del dictionary_copy[key]

        if key[0] in rows and key[1] in columns:
            value_list = dictionary.get(key)
            if value in value_list:
                value_list.remove(value)
                x = dictionary_copy.get(key)
                if x == None:
                    continue
                if len(x) == 0:
                    continue
                elif value in x:
                    x.remove(value)
                    if len(x) == 0:
                        del dictionary_copy[key]

    return dictionary_copy
    
def zeros_counter(board, row, column):
    """Finds and returns the number of zeroes in the same row, column and square as the cell being evaluated."""
    square = square_slice(board, row, column)
    row_array = board[row]
    column_array = board[:,column]
    row_zeros = np.count_nonzero(row_array == 0) - 1
    column_zeros = np.count_nonzero(column_array == 0) - 1
    square_zeros = np.count_nonzero(square == 0) - 1
    no_of_zeros = row_zeros + column_zeros + square_zeros
    
    return no_of_zeros
    
def degree_heuristic(state, min_values, dictionary):
    """Finds and returns the cell with the most possible constraints."""
    board = state.board
    zeros = []

    for key in min_values:
        row = key[0]
        column = key[1]
        key_zeros = zeros_counter(board, row, column)
        zeros.append(key_zeros)
    
    test = dict(zip(min_values, zeros))
    ordered_variable = max(test, key=test.get)
    
    return ordered_variable

def least_constraining_value(dictionary, key):
    """From the possible values of the most constrained cell, this method returns a list of the
       possible values ordered from least constraining to most constraining."""
    values = dictionary.get(key)
    row = key[0]
    column = key[1]
    value_index = []
    constrain_keys = []
    ordered_values = []
    rows, columns = square_finder(row, column)
    
    if len(values) == 1:
        return values
    else:
        for value in values:
            value_index.append(value)
            constrain = []
            for k in dictionary:
                if k[0] == row and k[1] == column:
                    continue
                elif k[0] == row:
                    k_values_check = dictionary.get(k)
                    if value in k_values_check:
                        constrain.append(value)
                elif k[1] == column:
                    k_values_check = dictionary.get(k)
                    if value in k_values_check:
                        constrain.append(value)
                elif k[0] in rows or k[1] in columns:
                    k_values_check = dictionary.get(k)
                    if value in k_values_check:
                        constrain.append(value)
            z = len(constrain)
            constrain_keys.append(z)
    
    while len(constrain_keys) > 0:
        least_get = min(constrain_keys)
        least_get_index = constrain_keys.index(least_get)
        order = value_index[least_get_index]
        ordered_values.append(order)
        constrain_keys.remove(least_get)
        value_index.remove(order)

    return ordered_values

def solution_finder(state, dictionary):
    """This method contains the backtracking algorithm used to solve the sudoku."""
    start_state = state
    board = start_state.board
    
    if sudoku_state.is_invalid(start_state, dictionary):
        board[board > -1] = -1
        start_state.board = board
        return start_state
    
    new_state = copy.deepcopy(state)
    test_board = copy.deepcopy(board)
    min_values = cell_dictionary_shortest(dictionary)
    ordered_variable = degree_heuristic(state, min_values, dictionary)
    
    row = ordered_variable[0]
    column = ordered_variable[1]
    least_values = least_constraining_value(dictionary, ordered_variable)

    for value in least_values:  
        dictionary_test = copy.deepcopy(dictionary)
        test_board[row][column] = value
        if new_state.valid_value(new_state, row, column, value, dictionary_test):
            new_state.board = test_board
            update_dictionary = cell_dictionary_updater(dictionary_test, row, column, value)
            
            if new_state.is_goal():
                return new_state

            if not sudoku_state.is_invalid(new_state, update_dictionary):
                test_new_state = solution_finder(new_state, update_dictionary)

                if test_new_state is not None and test_new_state.is_goal():
                    return test_new_state

        test_board[row][column] = 0
    return None
    
def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    
    test = cells_dictionary(sudoku)
    state = sudoku_state(sudoku)
    solved_sudoku_state = solution_finder(state, test)
    
    if solved_sudoku_state == None:
        sudoku[sudoku > -1] = -1
        solved_sudoku = sudoku
    else:
        solved_sudoku = solved_sudoku_state.board
            
    return solved_sudoku