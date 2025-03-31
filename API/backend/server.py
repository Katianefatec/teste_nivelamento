from flask import Flask
from routes.operadoras import bp_operadoras
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Registrar as rotas
app.register_blueprint(bp_operadoras)

if __name__ == '__main__':
    app.run(debug=True, port=3000)