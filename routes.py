from flask import Blueprint, render_template, request
from flask import Blueprint, render_template
from app.models import Character, Norsemen_Characters, Viking_Players
from app import db
# Create a blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/characters')
def view_characters():
    search_query = request.args.get('search', '')  # Get the search query from the URL
    filters = request.args.get('filters', None)  # Add filters if needed later

    if search_query:
        # Perform a full-text search
        characters = Character.query.filter(
            db.or_(
                Character.character.ilike(f'%{search_query}%'),
                Character.name.ilike(f'%{search_query}%'),
                Character.img.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        characters = Character.query.all()
    return render_template('characters.html', characters=characters, search_query=search_query)

@main.route('/norsemen_characters')
def view_table_two():
    search_query = request.args.get('search', '')  # Get the search query from the URL

    if search_query:
        # Perform a search across relevant columns
        norsemen = Norsemen_Characters.query.filter(
            db.or_(
                Norsemen_Characters.character_name.ilike(f'%{search_query}%'),
                Norsemen_Characters.description.ilike(f'%{search_query}%'),
                Norsemen_Characters.image_url.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        norsemen = Norsemen_Characters.query.all()

    return render_template('norsemen_characters.html', norsemen=norsemen, search_query=search_query)

@main.route('/viking_players')
def view_table_three():
    search_query = request.args.get('search', '')  # Get the search query from the URL

    if search_query:
        # Perform a search across relevant columns
        viking_players = Viking_Players.query.filter(
            db.or_(
                Viking_Players.name.ilike(f'%{search_query}%'),
                Viking_Players.stats.ilike(f'%{search_query}%'),
                Viking_Players.photo.ilike(f'%{search_query}%'),
                Viking_Players.biography.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        viking_players = Viking_Players.query.all()

    return render_template('viking_players.html', viking_players=viking_players, search_query=search_query)