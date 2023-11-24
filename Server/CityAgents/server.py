from flask import Flask, request, jsonify
from model import CityModel as RandomModel
from agent import Car as RandomAgent

# Size of the board:
number_agents = 1
width = 24
height = 25
randomModel = None
currentStep = 0

app = Flask("Traffic example")

@app.route('/init', methods=['GET', 'POST'])
def initModel():
    global currentStep, randomModel

    if request.method == 'POST':
        randomModel = RandomModel(number_agents)

        return jsonify({"message":"Parameters recieved, model initiated."})
    elif request.method == 'GET':
        randomModel = RandomModel(number_agents)

        return jsonify({"message":"Default parameters recieved, model initiated."})


@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
        agentPositions = [{"id": str(a.unique_id), "x": x, "y":1, "z":z}
                          for a_list, (x, z) in randomModel.grid.coord_iter()
                          for a in a_list if isinstance(a, RandomAgent)]
        print(agentPositions)

        return jsonify({'positions':agentPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})


if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)