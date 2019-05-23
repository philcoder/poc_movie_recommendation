from app import app, db

from app.models import User, Movie, SuggestMovies, UserRating

##NOTE: every model create need to be put in dictionary and imported like this code!
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Movie': Movie, 'UserRating' : UserRating, 'SuggestMovies' : SuggestMovies}