import sys

# Node class is declared
class Node():
    # init function is declared with the variables: self, state, parent and action, each of these variables is then initialized.
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

# StackFrontier class is declared        
class StackFrontier():
    # init function is declared and self.frontier is set to a empty list.
    def __init__(self):
        self.frontier = []
    
    # add function is declared and the node is added to self.frontier list    
    def add(self, node):
        self.frontier.append(node)
    
    # contains_state function is declared, the node is checked to see if it is the solution, if not, node is expanded and next node is added   
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    # empty function is declared, if frontier is empty, the length of frontier is equal to 0
    def empty(self):
        return len(self.frontier) == 0
    
    # remove function is declared, if frontier has a node, after checking it, the node will be removed
    # if frontier is already empty, empty frontier exception will occur
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

# QueueFrontier class is declared importing all the code from the StackFrontier class
class QueueFrontier(StackFrontier):
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

# Maze class is declared and initialized
class Maze():
    def __init__(self, filename):
        
        # Reads file and sets the height and width of the maze
        with open(filename) as f:
            contents = f.read()
            
        # Validates start zone and end goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")
        
        # Determine the height and width of the maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        
        # Keeps track of any walls in the path
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
            
        self.solution = None
        
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()
        
    def neighbours(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
    
    def solve(self):
        """Finds a solution to maze, if one exists."""
        
        # Keeps track of the number of states that have been explored
        self.num_explored = 0
        
        # initialize the frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)
        
        # initializes an empty explored set
        self.explored = set()
        
        # keeps looping until the solution is found
        while True:
            
            # if there is nothing left in frontier, then there is no path
            if frontier.empty():
                raise Exception("no solution")
            
            
            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1
            
            # If the node is the goal, then we have a solution to the maze
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                    
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            # Marks the node as explored
            self.explored.add(node.state)
            
            # Adds the neighbours to the frontier
            for action, state in self.neighbours(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
                    
    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size =  50
        cell_border = 2
        
        
        # Create a blank canvas to work with
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)
        
        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                
                # The Walls
                if col:
                    fill = (40, 40, 40)
                    
                # Start zone
                elif (i, j) == self.start:
                    fill = (255, 0, 0)
                    
                # End Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)
                    
                # Solution to the maze
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)
                    
                # States Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)
                    
                    
                # Empty cells
                else:
                    fill = (237, 240, 252)
                    
                # Draw cells
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border), 
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill = fill
                )
            img.save(filename)
            
if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt, use https://www.dcode.fr/maze-generator to generate the maze to solve and paste it in your maze.txt file")

# Maze is printed and is then solved and printed once more    
m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)