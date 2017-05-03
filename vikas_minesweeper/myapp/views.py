# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Crypto.Util.number import size
from django.shortcuts import render
from django.http import HttpResponse
from random import randint
import json
from django.http import JsonResponse


# List of global variables, lists and dictonaries
Total_Bombs = 10
LengthX = 9
LengthY = 9
answers_dict = {}
emptyBoxes_dict = {}
empty_boxes = []
class Tile:
    def __init__(self):
        self.bomb = False
        self.visited = False




# function to draw game
def draw(request):
    grid = [[Tile() for n in range(LengthX)] for n in range(LengthY)]
    for n in range(Total_Bombs):
        x = randint(0, 8)
        y = randint(0, 8)
        while True:
            if grid[x][y].bomb == False:
                grid[x][y].bomb = True
            break
    dict = preprocessedAnswers(grid)
    return render(request, "index.html", {"grid": grid})


#function to preprocess data and create preprocessed answers, need to lookup only most of the time
def preprocessedAnswers(grid):
    for rows in range(LengthX):
        for columns in range(LengthY):
            box_value = 0
            if grid[rows][columns].bomb == False:
                for (dx, dy) in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    if (0 <= (rows + dx) < LengthX) and (0 <= (columns + dy) < LengthY):
                        if grid[rows + dx][columns + dy].bomb == True:
                            box_value += 1

            if grid[rows][columns].bomb == True:
                box_value = -1

            answers_dict[str(rows+1)+str(columns+1)] = box_value
            if box_value == 0:
                emptyBoxes_dict[str(rows+1)+str(columns+1)] = 0
    return answers_dict



#lookup for each ajax request from our preprocessed answers and send response accordingly
def checkStatus(request,index_id):
    if request.method == 'GET' and request.is_ajax():
        xy = str(index_id)
        x_y = map(int, str(xy))
        x = x_y[0]
        y = x_y[1]
        answer = answers_dict[xy]
        if answer == -1:
            answer_list = []
            for key in answers_dict:
                if answers_dict[key] == -1:
                    answer_list.append(key)
            return HttpResponse(json.dumps({"result": answer,"result_list":answer_list}), content_type="application/json")

        if answer == 0:
            emptyBoxes_dict = {}
            emptyBoxes_dict[xy]=0
            emptyBoxes_dict = emptyBoxes(x, y,emptyBoxes_dict)
            return HttpResponse(json.dumps({"result": answer, "result_list": emptyBoxes_dict}), content_type="application/json")

        return HttpResponse(json.dumps({"result": answer}), content_type="application/json")

    else:
        return render("index.html", locals())



# function to create empty fields when we clicked on any single emply field in game
def emptyBoxes(x,y,emptyBoxes_dict):
    for (dx, dy) in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        if (0 < (x + dx) <= LengthX) and (0 < (y + dy) <= LengthY):
            index_x_y = str(x + dx)+str(y + dy)

            if index_x_y not in emptyBoxes_dict:
                if answers_dict[index_x_y] == 0:
                    emptyBoxes_dict[index_x_y] = answers_dict[index_x_y]
                    emptyBoxes(x +dx,y+dy,emptyBoxes_dict)
                if answers_dict[index_x_y] != -1:
                    emptyBoxes_dict[index_x_y] = answers_dict[index_x_y]

    return emptyBoxes_dict













