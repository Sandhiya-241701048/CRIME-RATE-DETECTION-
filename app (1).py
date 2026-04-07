from flask import Flask
from flask_cors import CORS
from routes.auth     import auth_bp
from routes.dataset  import dataset_bp
from routes.analysis import analysis_bp
from routes.alerts   import alerts_bp
from routes.reports  import reports_bp

app = Flask(__name__)
app.secret_key = "crime-rate-detection-secret-2024"
CORS(app, supports_credentials=True)

app.register_blueprint(auth_bp,     url_prefix="/api/auth")
app.register_blueprint(dataset_bp,  url_prefix="/api/dataset")
app.register_blueprint(analysis_bp, url_prefix="/api/analysis")
app.register_blueprint(alerts_bp,   url_prefix="/api/alerts")
app.register_blueprint(reports_bp,  url_prefix="/api/reports")

@app.route("/")
def home():
    return {"message": "Crime Rate Detection API is running!", "status": "ok"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
