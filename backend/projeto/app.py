from flask import Flask, request
from config.config import Config
from extension.extensao import db
from flask_cors import CORS

def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    CORS(app, 
         supports_credentials=True, 
         resources={r"/*": {
            "origins": ["http://localhost:8080", "http://localhost:8081"]
    }})

    from blueprints.cadastro_bp import cadastro_bp
    from blueprints.login_bp import login_bp
    from blueprints.perfil_bp import perfil_bp
    from blueprints.mensageria_bp import mensageria_bp
    
    app.register_blueprint(cadastro_bp, url_prefix='/cadastrar')
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(perfil_bp, url_prefix='/perfil')
    app.register_blueprint(mensageria_bp)

    return app

app = init_app()

