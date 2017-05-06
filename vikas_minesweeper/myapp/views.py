# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Crypto.Util.number import size
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from random import randint
import json
from django.http import JsonResponse


# List of variables, lists and dictonaries
answers_dict = {}
Total_Bombs = 10
LengthX = 9
LengthY = 9
Visited_Elements = [0]
Total_Elements = [0]
Length = [0,0,0]


class Tile:
    def __init__(self):
        self.bomb = False
        self.visited = False


# function to draw game for index page
def draw(request):
    del Length[:]
    Bomb_x = LengthX - 1
    Bomb_y = LengthY - 1
    Length.append(LengthX)
    Length.append(LengthY)
    Length.append(Total_Bombs)
    Total_Elements[0] = LengthX * LengthY
    grid = [[Tile() for n in range(LengthX)] for n in range(LengthY)]

    for n in range(Total_Bombs):
        x = randint(0, Bomb_x)
        y = randint(0, Bomb_y)

        while True:

            if grid[x][y].bomb == False:
                grid[x][y].bomb = True

            break

    preprocessedAnswers(grid,LengthX,LengthY,answers_dict)

    return render(request, "index.html", {"grid": grid})



# function to draw game on ajax call
def draw_ajax(request,LengthX,LengthY,Total_Bombs):
    Visited_Elements[0] = 0
    del Length[:]
    LengthX = int(LengthX)
    LengthY = int(LengthY)
    Length.append(LengthX)
    Length.append(LengthY)
    Total_Elements[0] = LengthX * LengthY
    Total_Bombs = int(Total_Bombs)
    Bomb_x = LengthX - 1
    Bomb_y = LengthY - 1
    grid = []

    grid = [[Tile() for n in range(LengthX)] for n in range(LengthY)]
    count = 0
    for n in range(Total_Bombs):

        while True:
            x = randint(0, Bomb_x)
            y = randint(0, Bomb_y)
            if grid[x][y].bomb == False:
                grid[x][y].bomb = True
                count +=1
                break

    preprocessedAnswers(grid,LengthX,LengthY,answers_dict)

    return HttpResponse(json.dumps({"length_x":LengthX,"length_y":LengthY}), content_type="application/json")




# function to preprocess data and create preprocessed
# answers, need to lookup only most of the time
def preprocessedAnswers(grid,LengthX,LengthY,answers_dict):
    answers_dict.clear()

    for rows in range(LengthX):

        for columns in range(LengthY):
            box_value = 0

            if grid[rows][columns].bomb == False:
                for (dx, dy) in [(0, 0),(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    if (0 <= (rows + dx) < LengthX) and (0 <= (columns + dy) < LengthY):
                        if grid[rows + dx][columns + dy].bomb == True:
                            box_value += 1

            if grid[rows][columns].bomb == True:
                box_value = -1

            answers_dict[rows+1,columns+1] = box_value

    return answers_dict



#  lookup for each ajax request from our preprocessed
#  answers and send response accordingly.
# Trying to reduce complexity of algorithm
def checkStatus(request,index_id_x,index_id_y):
    Success = False

    if request.method == 'GET' and request.is_ajax():
        x = int(index_id_x)
        y = int(index_id_y)
        answer = answers_dict[x,y]

        if answer == -1:
            answer_list = []

            for key in answers_dict:
                if answers_dict[key] == -1:
                    answer_list.append(key)

            return HttpResponse(json.dumps({"result": answer,"result_list":answer_list}), content_type="application/json")


        if answer == 0:
            emptyBoxes_dict = {}
            emptyBoxes_dict[str((x,y))]=0
            emptyBoxes_dict = emptyBoxes(x, y,emptyBoxes_dict)
            Visited_Elements[0] = Visited_Elements[0] + len(emptyBoxes_dict)

            if Visited_Elements[0] == (Total_Elements[0] - Total_Bombs):
                Success = True

            return HttpResponse(json.dumps({"result": answer, "result_list": emptyBoxes_dict,"Success":Success}), content_type="application/json")

        Visited_Elements[0] += 1
        if Visited_Elements[0] == (Total_Elements[0] - Total_Bombs):
            Success = True

        return HttpResponse(json.dumps({"result": answer,"Success":Success}), content_type="application/json")




# function to create empty fields when we
# clicked on any single emply field in game
def emptyBoxes(x,y,emptyBoxes_dict):
    LengthX = Length[0]
    LengthY = Length[1]
    print LengthX,LengthY

    for (dx, dy) in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        if (0 < (x + dx) <= LengthX) and (0 < (y + dy) <= LengthY):
            index_x_y = (x + dx,y + dy)

            if str(index_x_y) not in emptyBoxes_dict:
                if answers_dict[index_x_y] == 0:
                    emptyBoxes_dict[str(index_x_y)] = 0
                    emptyBoxes(x +dx,y+dy,emptyBoxes_dict)
                if answers_dict[index_x_y] != -1:
                    emptyBoxes_dict[str(index_x_y)] = answers_dict[index_x_y]


    return emptyBoxes_dict

