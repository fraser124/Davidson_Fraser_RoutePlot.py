import numpy as np
import click

'''This function creates a matrix of size*size. It then formats the elements of the matrix into different values depending on position, leaving the area in the middle to be populated later by our drone. '''
def area_create(): 
    size = 14
    area = np.zeros((size+1,size))
    for i in range(size):
        if i != 0 or i == size:
            area[i][0] = str(size - i-1)
    for j in range(size):
        if j != 0 and j != 1:
            area[size][j] = str(j-1)
        elif j == 1:
            area[size][j] = 98
    for k in range(size):
        area[0][k] = 99
        area[size-1][k] = 99
        area[k][1] = 98
    return area

'''Input: A matrix of int. Function: converts to str and converts into printable format, then prints '''        
def print_area(area): 
    
    str_area = str(area).replace(' [', '').replace('[', '').replace(']', '').replace('.','  :').replace(' 0',"  ").replace('97', ' X')
    str_area = str_area.replace('99  : ','______').replace('99  :','_').replace(': 98  :','|').replace('__98  : ','|_______')
    print(str_area)

''' Input: A list of str with each coord. Function: prints str in suitable format'''
def print_coords(coords): 
    print("Co-ordinates: ")
    print(str(coords).replace('[','').replace(']','').replace("',","").replace("'",''))
    

''' Input: An empty matrix created by area_create(). Output: Either populated matrix and coordinates, stops the program or drone crash and coordinatres '''
def main(area_in):  
    
    area = area_in
    route_list = []
    route_coords = []
    start_pos_x = None
    start_pos_y =None
    size = 14
    route_name = input('Insert route file name or STOP to exit. i.e. route_1.txt : ')
    
    
    while True: #Prevents FileNotFoundError when unknown input from user and kicks if STOP entered
            
        try:
            with open(route_name) as rn:
                for line in rn:
                    line = line.split('\n')[0]
                    route_list.append(line)
            break
                   
        except FileNotFoundError:
            if route_name.upper() == "STOP":
                stop = 1
                return stop , 1
                break
            else:
                route_name = input("Invalid file name, retype file name i.e. route_1.txt : ")
            
    start_pos_x = int(route_list[0])
    start_pos_y= int(route_list[1])
    fin_route = route_list[2:]
    start_pos_x += 1
    start_pos_y = size - start_pos_y -1
    pos_x = start_pos_x -1
    pos_y = size-start_pos_y-1
    coord = "(" + str(pos_x) + "," + str(pos_y) + ")"
    route_coords.append(coord)
    
    if 1 < start_pos_x < size and 0 < start_pos_y < size -1: #ensures start position in bounds
        area[start_pos_y][start_pos_x] = 97 # 97 = X using print_area()
    else:
        print('Invalid start position, insert new route!')
    
    next_x = start_pos_x
    next_y = start_pos_y
    i = 0
        
    for next_dir in fin_route:#applies cardinal to our current position 
        if next_dir == "N":
            next_y -= 1
            pos_y += 1
        elif next_dir == "S":
            next_y += 1
            pos_y -= 1
        elif next_dir == "E":
            next_x += 1
            pos_x += 1
        elif next_dir == "W":
            next_x -= 1
            pos_x -= 1
        
        if 1 < next_x < size and 0 < next_y < size -1: #checks if still in bounds
            area[next_y][next_x] = 97
            coord = "(" + str(pos_x) + "," + str(pos_y) + ")"
            route_coords.append(coord)
        else:
            print_area(area)
            print('\nYour drone crashed into the boundary!')
            stop = 2
            return stop, route_coords
            break
        from time import sleep #allows drone to be followed 
        print_area(area)
        sleep(0.2)
        i += 1
        #if i <= len(fin_route):
        click.clear()
    
    return area, route_coords


'''Executable code using above functions'''    
area = area_create()
stop = 0

while stop == 0:
    
    area, coordinates = main(area)
    
    if isinstance(area,int) == True and area == 1:
        stop = 1
        print("Stopping program")
    
    elif isinstance(area,int) == True and area == 2:
        print("\n ")
        print_coords(coordinates)
        print("\n ")
        area = area_create()
    
    else:
        click.clear()
        print("\n")
        print_area(area)
        print("\n ")
        print_coords(coordinates)
        print("\n ")
        area = area_create()
        

    