import sys
import random


'''
 how to do enums in python
 no return types

'''

moving_taxonomy = {"kn":[[2,1],[1,2],[-2,-1],[-2,1],[-1,-2],[-1,2],[2,-1]],
                   "bs":[[1,1],[1,-1],[-1,-1],[-1,1],[2,2],[-2,-2],[2,-2],[-2,2],[3,3],[-3,-3],[-3,3],[3,-3],[4,4],[4,-4],[-4,4],[-4,-4],[5,5],[5,-5],[-5,5],[-5,-5],[6,6],[6,-6],[-6,6],[-6,-6],[7,7],[7,-7],[-7,7],[-7,-7]],
                   "rk":[[0,1],[1,0],[-1,0],[0,-1],[0,2],[2,0],[-2,0],[0,-2],[0,3],[3,0],[-3,0],[0,-3],[0,4],[4,0],[-4,0],[0,-4],[0,5],[5,0],[-5,0],[0,-5],[0,6],[6,0],[-6,0],[0,-6],[0,7],[7,0],[-7,0],[0,-7]],
                   "pw":[[1,0],[-1,0]],
                   "qn":[[1,1],[1,-1],[-1,-1],[-1,1],[2,2],[-2,-2],[2,-2],[-2,2],[3,3],[-3,-3],[-3,3],[3,-3],[4,4],[4,-4],[-4,4],[-4,-4],[5,5],[5,-5],[-5,5],[-5,-5],[6,6],[6,-6],[-6,6],[-6,-6],[7,7],[7,-7],[-7,7],[-7,-7],
                        [0,1],[1,0],[-1,0],[0,-1],[0,2],[2,0],[-2,0],[0,-2],[0,3],[3,0],[-3,0],[0,-3],[0,4],[4,0],[-4,0],[0,-4],[0,5],[5,0],[-5,0],[0,-5],[0,6],[6,0],[-6,0],[0,-6],[0,7],[7,0],[-7,0],[0,-7]],
                   "kk":[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
                   }

eating_taxonomy = {"kn":[[2,1],[1,2],[-2,-1],[-2,1],[-1,-2],[-1,2],[2,-1]],
                   "bs":[[1,1],[1,-1],[-1,-1],[-1,1],[2,2],[-2,-2],[2,-2],[-2,2],[3,3],[-3,-3],[-3,3],[3,-3],[4,4],[4,-4],[-4,4],[-4,-4],[5,5],[5,-5],[-5,5],[-5,-5],[6,6],[6,-6],[-6,6],[-6,-6],[7,7],[7,-7],[-7,7],[-7,-7]],
                   "rk":[[0,1],[1,0],[-1,0],[0,-1],[0,2],[2,0],[-2,0],[0,-2],[0,3],[3,0],[-3,0],[0,-3],[0,4],[4,0],[-4,0],[0,-4],[0,5],[5,0],[-5,0],[0,-5],[0,6],[6,0],[-6,0],[0,-6],[0,7],[7,0],[-7,0],[0,-7]],
                   "pw":[[1,1],[1,-1],[-1,1],[-1,-1]],
                   "qn":[[1,1],[1,-1],[-1,-1],[-1,1],[2,2],[-2,-2],[2,-2],[-2,2],[3,3],[-3,-3],[-3,3],[3,-3],[4,4],[4,-4],[-4,4],[-4,-4],[5,5],[5,-5],[-5,5],[-5,-5],[6,6],[6,-6],[-6,6],[-6,-6],[7,7],[7,-7],[-7,7],[-7,-7],
                        [0,1],[1,0],[-1,0],[0,-1],[0,2],[2,0],[-2,0],[0,-2],[0,3],[3,0],[-3,0],[0,-3],[0,4],[4,0],[-4,0],[0,-4],[0,5],[5,0],[-5,0],[0,-5],[0,6],[6,0],[-6,0],[0,-6],[0,7],[7,0],[-7,0],[0,-7]],
                   "kk":[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
                   }


can_jump=set(["kn"])
polarity={"pw":{"b":1, "w":-1}}

debug=False

class piece:

    def __init__(self,id,loc):
        self.id=id
        self.position=loc
        self.type=id[1:3]
        self.color=id[0]
        self.active=True

class cell:
    def __init__(self):
        self.piece=None

    def to_text(self):
        if self.piece==None:
            return "      ."
        else:
            return self.piece.id+"  ."

class game:
    def __init__(self):
        self.board=[[cell() for i in range(8)] for j in range(8)]

    def printBoard(self):
        for row in self.board:
            for this_cell in row:
                print this_cell.to_text(),
            print
        print

    def add_piece(self,apiece,coords):
        coords
        if self.board[coords[0]][coords[1]].piece!=None:
            return
        self.board[coords[0]][coords[1]].piece=apiece
        apiece.position=coords

    def generate_path(self,x,y):
        #print "BEGIN", x, y
        i=0
        j=0
        result=[]
        if x[0]==y[0]:
            i=0
        if x[0]>y[0]:
            i=-1
        if x[0]<y[0]:
            i=1
        if x[1]==y[1]:
            j=0
        if x[1]>y[1]:
            j=-1
        if x[1]<y[1]:
            j=1
        steps=0
        temp=x
        #print i, j
        while True:
            temp=[temp[0]+i,temp[1]+j]
            result.append(temp)
            steps+=1
            if temp==y or steps>=10:
                return result
            #print result
        return result

    def is_in_board(self,i):
        if i[0]>=0 and i[0]<=7 and i[1]>=0 and i[1]<=7:
            return True
        return False
        
    def move_at_random_to_empty(self,color_set):
        possible_moves=[]
        for apiece in color_set:
            original_position=apiece.position
            for offset in moving_taxonomy[apiece.type]:
                is_blocked=False
                if apiece.type in can_jump:
                    new_coordinates=[apiece.position[0]+offset[0],apiece.position[1]+offset[1]]
                else:
                    if debug==True:
                        print apiece.id

                    if apiece.type in polarity and offset[0]*polarity[apiece.type][apiece.color] < 0:
                        continue

                    new_coordinates=[apiece.position[0]+offset[0],apiece.position[1]+offset[1]]
                    for i in self.generate_path(original_position,new_coordinates):
                        if self.is_in_board(i)==False:
                            is_blocked=True
                            break
                        elif  i!= new_coordinates and  self.board[i[0]][i[1]].piece!=None:
                            is_blocked = True
                            break
                if is_blocked==False and self.is_in_board(new_coordinates)==True and self.board[new_coordinates[0]][new_coordinates[1]].piece == None:
                    #print apiece.id, new_coordinates, original_position
                    possible_moves.append((apiece,new_coordinates,original_position))
        if len(possible_moves)>0:
            chosen_move=possible_moves[random.randint(0,len(possible_moves)-1)]
            new_coordinates=chosen_move[1]
            apiece=chosen_move[0]
            original_position=chosen_move[2]
            apiece.position=new_coordinates
            self.board[new_coordinates[0]][new_coordinates[1]].piece=apiece
            print self.board[new_coordinates[0]][new_coordinates[1]].piece.id, original_position, "->", new_coordinates
            self.board[original_position[0]][original_position[1]].piece=None


        


    def move_to_capture(self,color_set,opponent_set):
        possible_moves=[]
        for apiece in color_set:
            my_color=apiece.color
            original_position=apiece.position
            for offset in eating_taxonomy[apiece.type]:
                is_blocked=False
                if apiece.type in can_jump:
                    ## We are assuming that can_jump and polarity do not overlap
                    new_coordinates=[apiece.position[0]+offset[0],apiece.position[1]+offset[1]]
                else:
                    if apiece.type in polarity and offset[0]*polarity[apiece.type][apiece.color] < 0:
                        continue
                    new_coordinates=[apiece.position[0]+offset[0],apiece.position[1]+offset[1]]
                    for i in self.generate_path(original_position,new_coordinates):
                        if self.is_in_board(i)==False:
                            is_blocked=True
                            break
                        elif i!= new_coordinates and self.board[i[0]][i[1]].piece!=None:
                            is_blocked=True
                            break
                if is_blocked == False and  self.is_in_board(new_coordinates)==True and self.board[new_coordinates[0]][new_coordinates[1]].piece != None  and self.board[new_coordinates[0]][new_coordinates[1]].piece.color != my_color:
                    #print apiece.id, new_coordinates, original_position
                    possible_moves.append((apiece,new_coordinates,original_position))
        if len(possible_moves)>0:
            chosen_move=possible_moves[random.randint(0,len(possible_moves)-1)]
            new_coordinates=chosen_move[1]
            apiece=chosen_move[0]
            original_position=chosen_move[2]
            apiece.position=new_coordinates
            opponent_set.remove(self.board[new_coordinates[0]][new_coordinates[1]].piece)
            self.board[new_coordinates[0]][new_coordinates[1]].piece=apiece
            self.board[original_position[0]][original_position[1]].piece=None
            print self.board[new_coordinates[0]][new_coordinates[1]].piece.id, original_position, "->", new_coordinates
        else:
            if debug == True:
                print "Move To empty"
            self.move_at_random_to_empty(color_set)

random.seed()
this_game = game()
whites=set()
blacks=set()
playing_order=["w","b"]
playing_set={"w":whites, "b":blacks}

original_layout=(("bkn1",[0,1]),("bkn2",[0,6]),("bbs1",[0,2]),("bbs2",[0,5]),("brk1",[0,0]),("brk2",[0,7]),("bpw1",[1,0]),("bpw2",[1,7]),("bpw3",[1,1]),("bpw4",[1,6]),("bpw5",[1,2]),("bpw6",[1,5]),("bpw7",[1,3]),("bpw8",[1,4]),
                 ("bkk1",[0,3]),("bqn1",[0,4]),
                 ("wkn1",[7,1]),("wkn2",[7,6]),("wbs1",[7,2]),("wbs2",[7,5]),("wrk1",[7,0]),("wrk2",[7,7]),("wpw1",[6,0]),("wpw2",[6,7]),("wpw3",[6,1]),("wpw4",[6,6]),("wpw5",[6,2]),("wpw6",[6,5]),("wpw7",[6,3]),("wpw8",[6,4]),
                 ("wkk1",[7,3]),("wqn1",[7,4])
                 )
##  Set up the game  ###
for xpiece in original_layout:
    team=playing_set[xpiece[0][0]]
    apiece=piece(xpiece[0],None)
    team.add(apiece)
    this_game.add_piece(apiece,xpiece[1])

### Start the game  ####
movement_number=0
this_game.printBoard()
while len(whites)>0 and len(blacks)>0:
    print "Turn of", playing_order[movement_number%len(playing_order)],  movement_number, len(whites), len(blacks)
    this_game.move_to_capture(playing_set[playing_order[movement_number%len(playing_order)]],playing_set[playing_order[(movement_number+1)%len(playing_order)]])
    this_game.printBoard()
    king_captured=True
    for piece in playing_set[playing_order[(movement_number+1)%len(playing_order)]]:
        if piece.type == "kk":
            king_captured=False
            break
    if king_captured==True:
        print playing_order[(movement_number+1)%len(playing_order)], "King captured... Game over!!!"
        break
    movement_number+=1

