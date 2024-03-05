from app.models.models import User, db

class UserRepository:
    @staticmethod
    def create_user(email, password, api_token):
        new_user = User(email=email, password=password, api_token=api_token)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()
