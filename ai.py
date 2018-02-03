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
                self.pre_move = pre_move    # State sebelumnya <<--- ini buat pa ya?
                self.successors = []  #list of State objects
	def highest_tile(self):
		"""Return the highest tile here (just a suggestion, you don't have to)"""
		self.highestTile = 0
		for i in range(0, len(self.matrix)):
                        for j in range(0, len(self.matrix)):
                                self.highestTile = max(self.highestTile, self.matrix[i][j])
                if True:
                        return self.highestTile

        def getScore(self):
                return self.score
        def getPlayerType(self):
                return self.player
        def getMatrix(self):
                return self.matrix
                
		

class Gametree:
	"""main class for the AI"""
	#Hint: Two operations are important. Grow a game tree, and then compute minimax score. 
	#Hint: To grow a tree, you need to simulate the game one step. 
	#Hint: Think about the difference between your move and the computer's move.
	def __init__(self, root, totalPoints, depth):
                self.stateRoot = State(root, PLAYERS['max'],totalPoints, None)
		self.height = depth
		self.totalPoints = totalPoints

		self.layer0 = [self.stateRoot]  # Layer 0 is done  (list biasa)
		self.layer1 = []                # (list biasa)
		self.layer2 = []                # (list of list)
		self.layer3 = []                # (list of list)
                
	def grow_once(self, state):  # state itu State object
		"""Grow the tree one level deeper"""  ## only from the max state right?
		listOfChildrenStates= []

                if state.getPlayerType == PLAYERS['max']:
                        simulatorUp = Simulator( state.getMatrix(), state.getScore())
                        simulatorLeft = Simulator( state.getMatrix(), state.getScore())
                        simulatorDown = Simulator( state.getMatrix(), state.getScore())
                        simulatorRight = Simulator( state.getMatrix(), state.getScore())

                        simulatorUp.move(0);
                        simulatorLeft.move(1);
                        simulatorDown.move(2);
                        simulatorRight.move(3);

                        stateChildUp = State(simulatorUp.getMatrixBefore(), PLAYERS['computer'], simulatorUp.getMatrixBeforeScore(), state)
                        stateChildLeft = State(simulatorLeft.getMatrixBefore(), PLAYERS['computer'], simulatorLeft.getMatrixBeforeScore(), state)
                        stateChildDown = State(simulatorDown.getMatrixBefore(), PLAYERS['computer'], simulatorDown.getMatrixBeforeScore(), state)
                        stateChildRight = State(simulatorDown.getMatrixBefore(), PLAYERS['computer'], simulatorDown.getMatrixBeforeScore(), state)

                        listOfChildrenStates.append(stateChildUp)
                        listOfChildrenStates.append(stateChilLeft)
                        listOfChildrenStates.append(stateChildDown)
                        listOfChildrenStates.append(stateChildRight)
                elif state.getPlayerType == PLAYERS['computer']:
                        #countEmptyField = 0;

                        currMatrix = state.getMatrix()
                        dimension = len(currMatrix)
                        for i in range(0, dimension):
                                for j in range(0, dimension):
                                        if currMatrix[i][j] == 0:
                                                modifedMatrix = currMatrix
                                                modifiedMatrix[i][j] = 2
                                                plusA2Tile = State(modifiedMatrix, PLAYERS['max'], state.getScore(), state)
                                                
                                                listOfChildrenStates.append(plusA2Tile)

        
		return listOfChildrenStates
	def grow(self, state, height):
		"""Grow the full tree from root"""
		self.layer1 = grow_once(self.stateRoot)   #Layer 1 is done

		for i in range(0, len(self.layer1)):      #Layer 2 is done
                        self.layer2.append( grow_once(self.layer1[i]) )

                for i in range(0, len(self.layer2)):      #Layer 3 is done
                        for j in range(0, len(self.layer2[i]):
                                self.layer3.append( grow_once(self.layer2[i][j]) )
                                       
		
	def minimax(self, state):
		"""Compute minimax values on the three"""
		#grow(state)
		pass
	def compute_decision(self):
		"""Derive a decision"""
                #minimax(self.stateRoot)
                          
		#Replace the following decision with what you compute
		decision = random.randint(0,3)
		#Should also print the minimax value at the root
		print(MOVES[decision])
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
			#self.placeRandomTile()
		for j in range(0, (4 - direction) % 4):
			self.rotateMatrixClockwise()
	def moveTiles(self):
		tm = self.matrixBefore
		for i in range(0, len(self.matrixBefore)):      ##ini gw ganti self.board_size jadi len(self.matrixBefore)
			for j in range(0, len(self.matrixBefore) - 1): ##
				while tm[i][j] == 0 and sum(tm[i][j:]) > 0:
					for k in range(j, len(self.matrixBefore) - 1): ##
						tm[i][k] = tm[i][k + 1]
					tm[i][len(self.matrixBefore) - 1] = 0  ##
	def mergeTiles(self):
                tm = self.matrixBefore
		for i in range(0, len(self.matrixBefore)):      ##
			for k in range(0, len(self.matrixBefore) - 1):  ##
				if tm[i][k] == tm[i][k + 1] and tm[i][k] != 0:
					tm[i][k] = tm[i][k] * 2
					tm[i][k + 1] = 0
					self.matrixBeforeScore += tm[i][k]
					self.moveTiles()
		
	def checkIfCanGo(self):
		tm = self.matrixBefore
		for i in range(0, len(self.matrixBefore) ** 2): ##
			if tm[int(i / len(self.matrixBefore))][i % len(self.matrixBefore)] == 0: ##
				return True		
		for i in range(0, len(self.matrixBefore)):      ##
			for j in range(0, len(self.matrixBefore) - 1):  ##
				if tm[i][j] == tm[i][j + 1]:
					return True
				elif tm[j][i] == tm[j + 1][i]:
					return True
		return False
	def canMove(self):
                tm = self.matrixBefore
		for i in range(0, len(self.matrixBefore)):      ##
			for j in range(1, len(self.matrixBefore)):  ##
				if tm[i][j-1] == 0 and tm[i][j] > 0:
					return True
				elif (tm[i][j-1] == tm[i][j]) and tm[i][j-1] != 0:
					return True
		return False
	def rotateMatrixClockwise(self):	
		tm = self.matrixBefore
		for i in range(0, int(len(self.matrixBefore)/2)): ##
			for k in range(i, len(self.matrixBefore)- i - 1): ##
				temp1 = tm[i][k]
				temp2 = tm[len(self.matrixBefore) - 1 - k][i] ##
				temp3 = tm[len(self.matrixBefore) - 1 - i][len(self.matrixBefore) - 1 - k] ##
				temp4 = tm[k][len(self.matrixBefore) - 1 - i] ##
				tm[len(self.matrixBefore) - 1 - k][i] = temp1 ##
				tm[len(self.matrixBefore) - 1 - i][len(self.matrixBefore) - 1 - k] = temp2 ##
				tm[k][len(self.matrixBefore) - 1 - i] = temp3  ##
				tm[i][k] = temp4		
	def convertToLinearMatrix(self):  ##katany boleh d delete
		m = []
		for i in range(0, len(self.matrixBefore) ** 2):
			m.append(self.matrixBefore[int(i / len(self.matrixBefore))][i % len(self.matrixBefore)]) ##
		m.append(self.matrixBeforeScore)
		return m
