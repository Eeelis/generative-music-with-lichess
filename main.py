import berserk, requests, json, webbrowser, socket

token = YOUR-TOKEN-GOES-HERE
number_of_games = 0

# Each square is assigned a value between 2 (a8, top left) and 65 (h1, bottom right), 1 and 0 are reserved for initializing
board = {
    "a8": "2;",  "b8": "3;",  "c8": "4;",  "d8": "5;",  "e8": "6;",  "f8": "7;",  "g8": "8;",  "h8": "9;",
    "a7": "10;",  "b7": "11;", "c7": "12;", "d7": "13;", "e7": "14;", "f7": "15;", "g7": "16;", "h7": "17;",
    "a6": "18;", "b6": "19;", "c6": "20;", "d6": "21;", "e6": "22;", "f6": "23;", "g6": "24;", "h6": "25;",
    "a5": "26;", "b5": "27;", "c5": "28;", "d5": "29;", "e5": "30;", "f5": "31;", "g5": "32;", "h5": "33;",
    "a4": "34;", "b4": "35;", "c4": "36;", "d4": "37;", "e4": "38;", "f4": "39;", "g4": "40;", "h4": "41;",
    "a3": "42;", "b3": "43;", "c3": "44;", "d3": "45;", "e3": "46;", "f3": "47;", "g3": "48;", "h3": "49;",
    "a2": "50;", "b2": "51;", "c2": "52;", "d2": "53;", "e2": "54;", "f2": "55;", "g2": "56;", "h2": "57;",
    "a1": "58;", "b1": "59;", "c1": "60;", "d1": "61;", "e1": "62;", "f1": "63;", "g1": "64;", "h1": "65;",
    }

# Send PD a 1 for each occupied square and a 0 for each unoccupied square
def Initialize():
    arr = data["d"]["fen"].split('/')
    positions = ''
    for e in arr:
        for c in e:
            if (c.isalpha() or c == '-'):
                positions += '1'
            else:
                positions += int(c.strip() or 0) * '0' 
    print(positions + "\n")
    for char in positions:
        s.sendall((char + ";").encode(encoding="utf-8"))
    
# Setup server for sending data to PD
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9001
s.connect(host, port)

headers={
    'Authorization': f'Bearer ' + token,
    "Accept": "application/x-ndjson"
}

# Create session as described at https://berserk.readthedocs.io/en/master/readme.html
session = berserk.TokenSession(token)
client = berserk.Client(session=session)

# Open game in web browser and start receiving game info
webbrowser.open("https://lichess.org/tv")
lines = requests.get('https://lichess.org/api/tv/feed', stream = True, headers=headers).iter_lines()

# Parse, print and send to PD
for line in lines:
    data = json.loads(line)
    if (data["t"] == "featured"):
        number_of_games += 1
        print("\nReceiving moves from game " + str(number_of_games) + "\nInitial State:")
        Initialize()
    elif (data["t"] == "fen"):
        move = (data["d"]["lm"])
        initial_position = (move[:len(move)//2])
        target_position = (move[len(move)//2:])
        print("Piece moved from " + str(initial_position) + " to " + str(target_position))
        s.sendall(board[initial_position].encode(encoding="utf-8")) 
        s.sendall(board[target_position].encode(encoding="utf-8"))

