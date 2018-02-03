from __future__ import print_function
import copy, random
MOVES = {0:'up', 1:'left', 2:'down', 3:'right'}
PLAYERS = {'max': 0, 'computer': 1}

class State:
        """game state information"""
        #Hint: probably need the tile matrix, which player's turn, score, previous move
        def __init__(self, matrix, player, score, pre_move):
                self.matrix = matrix     # list of list
                self.player = player     # int
                self.score = score
                self.pre_move = pre_move    # previous State
                self.successors = []  #list of State objects
                self.isTerminal = False
                self.movement = -1  #upState= 0 ,  leftState= 1, downState = 2, rightState = 3
        def highest_tile(self): 
	#"""Return the highest tile in the matrix here (just a suggestion, you don't have to)"""
                self.highestTile = 0
                for i in range(0, len(self.matrix)):
                        for j in range(0, len(self.matrix)):
                                self.highestTile = max(self.highestTile, self.matrix[i][j])
                return self.highestTile
        def getScore(self):
                return self.score
        def getPlayerType(self):
                return self.player
        def getMatrix(self):
                return self.matrix
        def getIsTerminal(self):
                return self.isTerminal
        def setIsTerminal(self, isItTerminal):
                self.isTerminal = isItTerminal
        def getMovement(self):
                return self.movement            
        def setMovement(self, direction):
                self.movement = direction
class Gametree:
	"""main class for the AI"""
	#Hint: Two operations are important. Grow a game tree, and then compute minimax score. 
	#Hint: To grow a tree, you need to simulate the game one step. 
	#Hint: Think about the difference between your move and the computer's move.
	def __init__(self, root, totalPoints, depth):
                self.stateRoot = State(root, PLAYERS['max'],totalPoints, None)
                self.height = depth

                self.stateAndChildren = {} #State and its children
                self.stateAndItsParent = {} #State and it parent
                self.stateAndItsParent[self.stateRoot]= None #layer 0
                
                
	def grow_once(self, state, isTerminal):  # state is State object
		"""generate the state's children and save it in the listOfChildrenStates"""
		listOfChildrenStates= []
		if state.getPlayerType() == PLAYERS['max']: #simuator is used for imitating the movement of the up, left, down, right

                        for i in range(0, 4):
                                simulator = Simulator( copy.deepcopy(state.getMatrix()), state.getScore() )

                                stateInitial = copy.deepcopy(state.getMatrix())
                                simulator.move(i)
                                if( simulator.getMatrixBefore() == stateInitial ): #if the simulator return the same matrix as before, then don't create the State object

                                        continue
                                stateChild = State(simulator.getMatrixBefore(), PLAYERS['computer'], simulator.getMatrixBeforeScore(), state)
                                stateChild.setMovement(i)
                                if isTerminal: #if this method is called to generate the terminal children, then set all the States to be terminal
                                        stateChild.setIsTerminal(True)
                                self.stateAndItsParent[stateChild] = state #set each children to its parent
                                listOfChildrenStates.append(stateChild) 

		elif state.getPlayerType() == PLAYERS['computer']:
                    
                        currMatrix = copy.deepcopy(state.getMatrix())
                        dimension = len(currMatrix)
                        for i in range(0, dimension):
                                for j in range(0, dimension):
                                        if currMatrix[i][j] == 0: # only create a State object for the chance player if there is an empty space to place a 2-tile
                                                modifiedMatrix = copy.deepcopy(state.getMatrix())
                                                modifiedMatrix[i][j] = 2
                                                plusA2TileState = State(modifiedMatrix, PLAYERS['max'], state.getScore(), state)

                                                self.stateAndItsParent[plusA2TileState] = state #set each children to each parent
                                                listOfChildrenStates.append(plusA2TileState)
		self.stateAndChildren[state] = listOfChildrenStates #parent and its children are connected
                
                
                    
	def grow(self, state, height):
		"""Grow the full tree from root"""
		if( height == 3):
                        self.grow_once(self.stateRoot, False) #layer 1

                        for i in range(0, len(self.stateAndChildren[self.stateRoot])): #layer 2
                                self.grow_once(self.stateAndChildren[self.stateRoot][i], False)

                        for i in range(0, len(self.stateAndChildren[self.stateRoot])):  #layer 3
                                for j in range(0, len(self.stateAndChildren[ self.stateAndChildren[self.stateRoot][i] ]) ):
                                        self.grow_once( self.stateAndChildren[ self.stateAndChildren[self.stateRoot][i] ][j], True )
		elif( height == 1):
                        self.grow_once(self.stateRoot, True) #layer 1
		
	def minimax(self, state):
		"""Compute minimax values on the three"""
		if state.getIsTerminal():
                    return self.evaluationFunction(state)
		elif state.getPlayerType() == PLAYERS['max']:
                    value = float('-inf')
                    for i in range(0, len( self.stateAndChildren[state])):
                                   value = max( value, self.minimax( self.stateAndChildren[state][i] ) )
                    return value
		elif state.getPlayerType() == PLAYERS['computer']:
                    value = 0
                    for i in range(0, len(self.stateAndChildren[state])):
                                   value = value + self.minimax(self.stateAndChildren[state][i]) * (1.0)/len(self.stateAndChildren[state])
                    return value                    
	def evaluationFunction(self, state): # evaluation function for the non-terminal node
		return state.getScore() + state.highest_tile()
		
		
	def compute_decision(self):
		"""Derive a decision"""
		self.grow(self.stateRoot,3) #1)grow the tree first
		listOfMinimax = []
		for i in range(0, len(self.stateAndChildren[self.stateRoot]) ): #2)calculate the minimax for each children of the root
                           listOfMinimax.append( self.minimax( self.stateAndChildren[self.stateRoot][i] ) )		
		highestMinimax= max(listOfMinimax)
		highestMinimaxIndexInListOfMinimax = listOfMinimax.index(highestMinimax)
		stateWithHighestMinimax = self.stateAndChildren[self.stateRoot][highestMinimaxIndexInListOfMinimax] # make the movement based on that State's self.movement                                                                       
		#Replace the following decision with what you compute
		decision = stateWithHighestMinimax.getMovement()  #3)make the movement based on that State's self.movement 
		#Should also print the minimax value at the root
		#decision = random.randint(0,2)
		print("move: ", MOVES[decision])
		print("expectimax at the root: ", self.minimax(self.stateRoot))
		return decision

class Simulator:
	"""Simulation of the game"""
	#Hint: You basically need to copy all the code from the game engine itself.
	#Hint: The GUI code from the game engine should be removed. 
	#Hint: Be very careful not to mess with the real game states. 
	def __init__(self, matrix, score):
            self.matrixBefore = matrix
            self.matrixBeforeScore = score
	def getMatrixBefore(self):
            return self.matrixBefore
	def getMatrixBeforeScore(self):
            return self.matrixBeforeScore
	def move(self, direction):
		for i in range(0, direction):
			self.rotateMatrixClockwise()
		if self.canMove():
			self.moveTiles()
			self.mergeTiles()
		for j in range(0, (4 - direction) % 4):
			self.rotateMatrixClockwise()
	def moveTiles(self):
		tm = self.matrixBefore
		size_board = len(self.matrixBefore)
		for i in range(0, size_board):      
			for j in range(0, size_board - 1): 
				while tm[i][j] == 0 and sum(tm[i][j:]) > 0:
					for k in range(j, size_board - 1): 
						tm[i][k] = tm[i][k + 1]
					tm[i][size_board - 1] = 0  
	def mergeTiles(self): 
		tm = self.matrixBefore
		size_board = len(self.matrixBefore)
		for i in range(0, size_board):
			for k in range(0, size_board - 1):
				if tm[i][k] == tm[i][k + 1] and tm[i][k] != 0:
					tm[i][k] = tm[i][k] * 2
					tm[i][k + 1] = 0
					self.matrixBeforeScore += tm[i][k]
					self.moveTiles()
            
		
	def checkIfCanGo(self):
		tm = self.matrixBefore
		size_board = len(self.matrixBefore)
		for i in range(0, size_board ** 2): 
			if tm[int(i / size_board)][i % size_board] == 0: 
				return True		
		for i in range(0, size_board):      
			for j in range(0, size_board - 1):  
				if tm[i][j] == tm[i][j + 1]:
					return True
				elif tm[j][i] == tm[j + 1][i]:
					return True
		return False
	def canMove(self): 
		tm = self.matrixBefore
		size_board = len(self.matrixBefore)
		for i in range(0, size_board):
			for j in range(1, size_board):
				if tm[i][j-1] == 0 and tm[i][j] > 0:
					return True
				elif (tm[i][j-1] == tm[i][j]) and tm[i][j-1] != 0:
					return True
		return False
	def rotateMatrixClockwise(self):	
		tm = self.matrixBefore
		size_board = len(self.matrixBefore)
		for i in range(0, int(size_board/2)): 
			for k in range(i, size_board- i - 1): 
				temp1 = tm[i][k]
				temp2 = tm[size_board - 1 - k][i] 
				temp3 = tm[size_board - 1 - i][size_board - 1 - k] 
				temp4 = tm[k][size_board - 1 - i] 
				tm[size_board - 1 - k][i] = temp1 
				tm[size_board - 1 - i][size_board - 1 - k] = temp2 
				tm[k][size_board - 1 - i] = temp3  
				tm[i][k] = temp4		
	def convertToLinearMatrix(self):  
		m = []
		size_board = len(self.matrixBefore)
		for i in range(0, size_board ** 2):
			m.append(self.matrixBefore[int(i / size_board)][i % size_board]) ##
		m.append(self.matrixBeforeScore)
		return m
