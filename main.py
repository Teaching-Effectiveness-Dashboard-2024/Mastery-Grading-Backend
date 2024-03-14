from flask import Flask
from models import db
from login.routes import login_bp
from dashboard.routes import dashboard_bp
from grading.routes import grading_bp

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:rootgrading@database-mastery-grading.cx0k4s4omp9i.us-east-1.rds.amazonaws.com:5432/mastery_database"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(grading_bp)

if __name__ == '__main__':
    app.run(debug=True)
