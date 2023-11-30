from flask import Flask, request, jsonify
from model import CityModel
from agent import *

# Size of the board:
number_agents = 20
width = 24
height = 25
cityModel = None
currentStep = 0

app = Flask("Traffic example")

@app.route('/init', methods=['GET', 'POST'])
def initModel():
    global currentStep, cityModel

    if request.method == 'POST':
        cityModel = CityModel(number_agents)

        return jsonify({"message":"Parameters recieved, model initiated."})
    elif request.method == 'GET':
        cityModel = CityModel(number_agents)

        return jsonify({"message":"Default parameters recieved, model initiated."})


@app.route('/getAgents', methods=['GET'])
def getAgents():
    global cityModel

    if request.method == 'GET':
        agentPositions = [{"id": str(a.unique_id), "x": x, "y":0, "z":z, "destination": {"x": a.destination[0], "y": 0, "z": a.destination[1]}}
                          for a_list, (x, z) in cityModel.grid.coord_iter()
                          for a in a_list if isinstance(a, Car)]

        return jsonify({'positions':agentPositions})

@app.route('/getTrafficLight', methods=['GET'])
def getTrafficLight():
    global cityModel

    if request.method == 'GET':
        trafficLightPositions = [{"id": str(a.unique_id), "x": x, "y":0, "z":z, "state":a.state, "direction":a.direction}
                          for a_list, (x, z) in cityModel.grid.coord_iter()
                          for a in a_list if isinstance(a, Traffic_Light)]
        return jsonify({'positions':trafficLightPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, cityModel
    if request.method == 'GET':
        cityModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})


if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)