data = ['.........O',
'.......O.O',
'......O.O',
'OO...O..O',
'OO....O.O',
'.......O.O.........OO',
'.........O.........O.O',
'.....................O',
'.....................OO']

for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j] == "O":
            print([j,i], end = ",")