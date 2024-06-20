from flask import Flask, request, jsonify 
from flask_cors import CORS
from simplex_2_phases import Simplex2Phases
from plne import PLNE
from tableau_builder import TableauBuilder

app = Flask(__name__)
CORS(app)

@app.route('/simplex-solver/api/solve', methods=['POST'])
def solve():
    parameter = request.get_json()
    print(parameter)
    str_problem = f"{parameter['objective']}\n{parameter['constraints']}"
    tableau_builder = TableauBuilder(str_problem=str_problem)
    result = None
    if parameter['naturalSolution']:
        result = PLNE(tableau_builder.build(), tableau_builder.problem_type).solve()
    else:
        result = Simplex2Phases(tableau_builder.build(), tableau_builder.problem_type).solve()
    return jsonify(result), 201

if __name__ == '__main__':
    app.run(debug=True)