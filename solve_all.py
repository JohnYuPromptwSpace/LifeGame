import sys

def load_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    result = []
    for line in lines:
        row = [int(char) for char in line.strip()]
        result.append(row)

    return result

if input("Solve All? Y to continue, else to discard\n") != "Y":
    sys.exit()

try:
    # reset lab
    LAB_NAME = ["Toad", "Beacon", "Glider", "Pulsar", "48P22.1", "Achim's p11", "Flicker", "Gosper Glider Gun"]

    for MAP in LAB_NAME:
        curr = load_data(f"data/default_data/{MAP}.txt")
        
        with open(f"data/player_data/{MAP}.txt", 'w') as file:
            for data in curr:
                file.write("".join(map(str,data)) + "\n")

except:
    print("Faild to reset Lab data.\nCheck gamePath/data/player_data for player current puzzle data\nCheck gamePath/data/default_data for player puzzle default data\nCheck gamePath/data/puzzles for player puzzle answer data")
    sys.exit()

try:
        # reset player state
    curr = [
        [1,1,1,1,1,1,1,1,],
        [1,1,1,1,1,1,1,1,]
    ]
    with open("data/player_data/player_state.txt", 'w') as file:
        for data in curr:
            file.write("".join(map(str,data)) + "\n")

except:
    print("Faild to reset Player state data.\nCheck gamePath/data/player_data for player current state data\nCheck gamePath/data/default_data for player state default data")
    sys.exit()

print("--------------------------------------------------")
print("Player data has been set to All Solved successfuly")
print("--------------------------------------------------")