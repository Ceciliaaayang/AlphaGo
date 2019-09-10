import numpy as np
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, \
                       PASS, is_black_white, coord_to_point, where1d, \
                       MAXSIZE, NULLPOINT

# different types of patterns below
C2 = 1		# chong'er	2 stones in a row, 1 move to make a chongsan
C3 = 2		# chongsan	3 stones in a row, 1 move to make a chongsi
C4 = 3		# chongsi	4 stones in a row, 1 move(1 possible position) to make a 5
H2 = 4		# huo'er	2 stones in a row, 1 move to make a huosan
H3 = 5		# huosan	3 stones in a row, 1 move to make a huosi
H4 = 6		# huosi		4 stones in a row, 1 move(2 possible positions) to make a 5
H5 = 7		# huowu		5 stones in a row
ANALYZED = 8		# has benn analyzed
UNANALYZED = 0			# has not been analyzed

'''
	Define an BoardEvaluator class.
	Note: I wrote more than 100 lines if-elif-else statements to discuss every single
		possible scenarios that could occur. This portion of code looks ugly but it is
		quite necessary for the BoardEvaluator process.
'''
class BoardEvaluator (object):

	def __init__ (self, boardsize=15):
		# TODO self.POS is for adding weight to each intersetion
		# add weight of 7 to the center, 6 to the outer square, then
		# 5, 4, 3, 2, 1, at last 0 to the outermost square.
		# self.POS = []
		# for i in range(self.boardsize):
		# 	row = []
		# 	for j in range(self.boardsize):
		# 		row.append( 7 - max(abs(i - 7), abs(j - 7)) )
		# 	# row = [ (7 - max(abs(i - 7), abs(j - 7))) for j in range(self.boardsize) ]
		# 	self.POS.append(tuple(row))
		
		self.boardsize = boardsize
		self.result = [ 0 for _ in range(self.boardsize * 2) ]		# save current reslut of analyzation in a line
		self.line = [ 0 for _ in range(self.boardsize * 2) ]		# current data in a line
		# result of analysis of whole board 
		# format of each item in list is record[row][col][dir]
		self.record = [[[0 for _ in range(4)] for _ in range(self.boardsize)] for _ in range(self.boardsize)]
		# count of each pattern: count[BLACK/WHITE][pattern]
		self.count = [[0 for _ in range(10)] for _ in range(3)]
		self.reset()

	
	# reset data
	def reset (self):
		self.record = [[[UNANALYZED for _ in range(4)] for _ in range(self.boardsize)] for _ in range(self.boardsize)]
		self.count = [[0 for _ in range(10)] for _ in range(3)]

	
	# analyze & evaluate board 
	# return score based on analysis result
	def evaluate (self, board, turn):
		score = self.__evaluate(board, turn)
		stone = GoBoardUtil.opponent(turn)
		if score < -9000:
			# print 'evaluate: stone = ', stone
			for i in range(10):
				if self.count[stone][i] > 0:
					score -= i
		elif score > 9000:
			# print 'evaluate: stone = ', stone
			for i in range(10):
				if self.count[turn][i] > 0:
					score += i
		return score
	
	
	# analyze & evaluate board 
	# in 4 directinos: horizontal, vertical, diagonal(left-hand or right-hand)
	# return score difference between players based on analysis result
	def __evaluate (self, board, toPlay):
		opponent = GoBoardUtil.opponent(toPlay)
		self.reset()
		# analysis in 4 directions
		for i in range(self.boardsize):
			for j in range(self.boardsize):
				if board[i][j] != 0:
					# has not analyzed horizontally
					if self.record[i][j][0] == UNANALYZED:
						self.__analysis_horizon(board, i, j)
					# has not analyzed vertically
					if self.record[i][j][1] == UNANALYZED:
						self.__analysis_vertical(board, i, j)
					# has not analyzed left-hand diagonally 
					if self.record[i][j][2] == UNANALYZED:
						self.__analysis_left(board, i, j)
					# has not analyzed right-hand diagonally
					if self.record[i][j][3] == UNANALYZED:
						self.__analysis_right(board, i, j)

		check = {}

		# for either WHITE or BLACK, calculated the number of occurences of different
		# patterns (i.e., five, four, cFour, three, cThree, two, cTwo)
		for c in (H5, H4, C4, H3, C3, H2, C2):
			check[c] = 1
		# for each stone on the board
		for i in range(self.boardsize):
			for j in range(self.boardsize):
				stone = board[i][j]
				if stone != 0:
					# for 4 directions
					for k in range(4):
						ch = self.record[i][j][k]
						if ch in check:
							self.count[stone][ch] += 1
		
		# return score if there is a five
		if self.count[opponent][H5]:
			return -9999
		elif self.count[toPlay][H5]:
			return 9999

		# if there exist 2 huosi, it's equivalent to 1 huowu
		if self.count[opponent][H4] >= 2:
			return -9999
		if self.count[toPlay][H4] >= 2:
			return 9999
		
		# if there exist 2 chongsi, it's equivalent to 1 huosi
		if self.count[WHITE][C4] >= 2:
			self.count[WHITE][H4] += 1
		if self.count[BLACK][C4] >= 2:
			self.count[BLACK][H4] += 1

		# return score for specific patterns
		toPlay_score = 0
		opponent_score = 0
		# current toPlay is WHITE
		if self.count[toPlay][H4] > 0:			# toPlay huosi
			return 9990
		if self.count[opponent][H4] > 0:			# opponent huosi
			return -9990
		if self.count[toPlay][C4] and self.count[toPlay][H3]:			# toPlay chongsi & huosan
			return 9985
		if self.count[opponent][C4] and self.count[opponent][H3]:			# opponent chongsi & huosan
			return -9985
		if self.count[toPlay][C4] > 0:			# toPlay chongsi
			return 9980
		if self.count[opponent][C4] > 0:			# opponent chongsi
			return -9980
		if	(self.count[toPlay][H3] > 1 and	# toPlay >1 huosan &
			self.count[opponent][C4] == 0 and	# no opponent chongsi &
			self.count[opponent][H3] == 0 and	# no opponent huosan &
			self.count[opponent][C3] == 0):		# no opponent chongsan
				return 9970
		if	(self.count[opponent][H3] > 1 and	# opponent >1 huosan &
			self.count[toPlay][C4] == 0 and	# no toPlay chongsi &
			self.count[toPlay][H3] == 0 and	# no toPlay huosan &
			self.count[toPlay][C3] == 0):		# no toPlay chongsan
				return -9970
		if self.count[toPlay][H3] and self.count[opponent][C4] == 0:	# toPlay huosan & no opponent chongsi
			return 9960
		if self.count[opponent][H3] and self.count[toPlay][C4] == 0:	# opponent huosan & no toplay chongsi
			return -9960
		
		if self.count[toPlay][H3] > 1:			# toPlay >1 huosan
			toPlay_score += 2000
		elif self.count[toPlay][H3]:			# toPlay 1 huosan
			toPlay_score += 200
		if self.count[opponent][H3] > 1:			# opponent >1 huosan
			opponent_score += 500
		elif self.count[opponent][H3]:			# opponent 1 huosan
			opponent_score += 100
		
		if self.count[toPlay][C3]:					# toPlay chongsan
			toPlay_score += self.count[toPlay][C3] * 10
		if self.count[opponent][C3]:					# opponent chongsan
			opponent_score += self.count[opponent][C3] * 10
		if self.count[toPlay][H2]:						# toPlay huo'er
			toPlay_score += self.count[toPlay][H2] * 4
		if self.count[opponent][H2]:						# opponent huo'er
			opponent_score += self.count[opponent][H2] * 4
		if self.count[toPlay][C2]:						# toPlay chong'er
			toPlay_score += self.count[toPlay][C2]
		if self.count[opponent][C2]:						# opponent chong'er
			opponent_score += self.count[opponent][C2]
		
		
		# TODO include weight for each intersection
		# add weight of 7 to the center, 6 to the outer square, then
		# 5, 4, 3, 2, 1, at last 0 to the outermost square.
		# wc = 0
		# bc = 0
		# # for each intersection with a stone, add weight
		# for i in range(self.boardsize):
		# 	for j in range(self.boardsize):
		# 		stone = board[i][j]
		# 		if stone != 0:
		# 			if stone == WHITE:
		# 				wc += self.POS[i][j]
		# 			else:
		# 				bc += self.POS[i][j]
		# # add total weight to total score
		# turn_score += wc
		# opponent_score += bc
		
		# return score differnece between players
		return toPlay_score - opponent_score
	
	
	# anaylze horizontally
	def __analysis_horizon (self, board, i, j):
		# add each intersection in a row to line
		for x in range(self.boardsize):
			self.line[x] = board[i][x]
		self.analysis_line(self.line, self.result, self.boardsize, j)
		for x in range(self.boardsize):
			if self.result[x] != UNANALYZED:
				self.record[i][x][0] = self.result[x]
		return self.record[i][j][0]
	
	
	# analyze vertically
	def __analysis_vertical (self, board, i, j):
		for x in range(self.boardsize):
			self.line[x] = board[x][j]
		self.analysis_line(self.line, self.result, self.boardsize, i)
		for x in range(self.boardsize):
			if self.result[x] != UNANALYZED:
				self.record[x][j][1] = self.result[x]
		return self.record[i][j][1]
	
	
	# analyze left-hand diagonally
	def __analysis_left (self, board, i, j):
		if i < j:
			x, y = j - i, 0
		else:
			x, y = 0, i - j
		k = 0
		while k < self.boardsize:
			if x + k > (self.boardsize - 1) or y + k > (self.boardsize - 1):
				break
			self.line[k] = board[y + k][x + k]
			k += 1
		self.analysis_line(self.line, self.result, k, j - x)
		for s in range(k):
			if self.result[s] != UNANALYZED:
				self.record[y + s][x + s][2] = self.result[s]
		return self.record[i][j][2]

	
	# analyzed right-hand diagonally
	def __analysis_right (self, board, i, j):
		if (self.boardsize - 1) - i < j:
			x, y, realnum = j - (self.boardsize - 1) + i, (self.boardsize - 1), (self.boardsize - 1) - i
		else:
			x, y, realnum = 0, i + j, j
		k = 0
		while k < self.boardsize:
			if x + k > (self.boardsize - 1) or y - k < 0:
				break
			self.line[k] = board[y - k][x + k]
			k += 1
		# print("i = {}, j = {}, x = {}, k = {}".format(i, j, x, k))
		self.analysis_line(self.line, self.result, k, j - x)
		for s in range(k):
			if self.result[s] != UNANALYZED:
				self.record[y - s][x + s][3] = self.result[s]
		return self.record[i][j][3]
	
	
	# analyze a line, find out different patterns (i.e., five, four, three, etc)
	def analysis_line(self, line, record, num, pos):		
		while len(line) < self.boardsize * 2:
			line.append(self.boardsize)
		while len(record) < self.boardsize * 2:
			record.append(UNANALYZED)
		
		for i in range(num, self.boardsize * 2):
			line[i] = self.boardsize
		for i in range(num):
			record[i] = UNANALYZED
		
		if num < 5:
			for i in range(num): 
				record[i] = ANALYZED
			return 0
		stone = line[pos]
		# print("pos = {}\n line = {}\n stone = {}\n".format(pos, line, stone))
		inverse = (0, 2, 1)[stone]
		num -= 1
		xl = pos
		xr = pos
		# left border
		while xl > 0:
			if line[xl - 1] != stone:
				break
			xl -= 1
		# right border
		while xr < num:
			if line[xr + 1] != stone:
				break
			xr += 1
		left_range = xl
		right_range = xr
		# left border (not opponent's stone intersection)
		while left_range > 0:
			if line[left_range - 1] == inverse:
				break
			left_range -= 1
		# right border (not opponent's stone intersection)
		while right_range < num:
			if line[right_range + 1] == inverse:
				break
			right_range += 1
		
		# if the linear range is less than 5, return directly
		if right_range - left_range < 4:
			for k in range(left_range, right_range + 1):
				record[k] = ANALYZED
			return 0
		
		# set ANALYZED
		for k in range(xl, xr + 1):
			record[k] = ANALYZED
		
		srange = xr - xl

		# if 5 in a row
		if srange >= 4:	
			record[pos] = H5
			return H5
		
		# if 4 in a row
		if srange == 3:	
			leftfour = False
			# if space on the left
			if xl > 0:
				if line[xl - 1] == 0:
					# huo'si
					leftfour = True
			if xr < num:
				if line[xr + 1] == 0:
					if leftfour:
						# huo'si
						record[pos] = H4
					else:
						# chognsi
						record[pos] = C4
				else:
					if leftfour:
						# chongsi
						record[pos] = C4
			else:
				if leftfour:
					# chongsi
					record[pos] = C4
			return record[pos]
		
		# if 3 in a row
		if srange == 2:
			left3 = False
			# if space on the left
			if xl > 0:
				# if space on the left
				if line[xl - 1] == 0:
					if xl > 1 and line[xl - 2] == stone:
						record[xl] = C4
						record[xl - 2] = ANALYZED
					else:
						left3 = True
				elif xr == num or line[xr + 1] != 0:
					return 0
			if xr < num:
				# if space on the right
				if line[xr + 1] == 0:
					if xr < num - 1 and line[xr + 2] == stone:
						# 11101 or 22202 is equivalent to chongsi
						record[xr] = C4
						record[xr + 2] = ANALYZED
					elif left3:
						record[xr] = H3
					else:
						record[xr] = C3
				elif record[xl] == C4:
					return record[xl]
				elif left3:
					record[pos] = C3
			else:
				if record[xl] == C4:
					return record[xl]
				if left3:
					record[pos] = C3
			return record[pos]
		
		# if 2 in a row
		if srange == 1:
			left2 = False
			if xl > 2:
				# if space on the left
				if line[xl - 1] == 0:
					if line[xl - 2] == stone:
						if line[xl - 3] == stone:
							record[xl - 3] = ANALYZED
							record[xl - 2] = ANALYZED
							record[xl] = C4
						elif line[xl - 3] == 0:
							record[xl - 2] = ANALYZED
							record[xl] = C3
					else:
						left2 = True
			if xr < num:
				# if space on the right
				if line[xr + 1] == 0:
					if xr < num - 2 and line[xr + 2] == stone:
						if line[xr + 3] == stone:
							record[xr + 3] = ANALYZED
							record[xr + 2] = ANALYZED
							record[xr] = C4
						elif line[xr + 3] == 0:
							record[xr + 2] = ANALYZED
							record[xr] = left2 and H3 or C3
					else:
						if record[xl] == C4:
							return record[xl]
						if record[xl] == C3:
							record[xl] = H3
							return record[xl]
						if left2:
							record[pos] = H2
						else:
							record[pos] = C2
				else:
					if record[xl] == C4:
						return record[xl]
					if left2:
						record[pos] = C2
			return record[pos]
		return 0

