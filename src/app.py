# app.py

import requests
from flask import Flask, render_template, abort, request, session, redirect, url_for
from plexapi.server import PlexServer
from plexapi.exceptions import NotFound
import config

app = Flask(__name__)
# Load the secret key from our config file to enable sessions
app.secret_key = config.SECRET_KEY

# --- Helper Functions (no changes here) ---
def check_internet_connection():
    try:
        requests.get("http://detectportal.firefox.com/success.txt", timeout=3)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

def add_auth_to_url(url):
    if not url: return None
    return f"{config.PLEX_URL}{url}?X-Plex-Token={config.PLEX_TOKEN}"

# --- Plex Connection (no changes here) ---
try:
    print("Connecting to Plex server as admin...")
    plex = PlexServer(config.PLEX_URL, config.PLEX_TOKEN, timeout=10)
    server_title = plex.friendlyName
    print(f"✅ Connection to '{server_title}' successful!")
except Exception as e:
    plex = None
    server_title = "Plex Server (Connection Failed)"
    print(f"❌ Could not connect to Plex. Error: {e}")

# --- App Routes ---

@app.route('/')
def user_select():
    """Shows the user selection screen."""
    if not plex: abort(500, "Plex server not connected.")
    
    # Get all account users (admin + managed users)
    users = [plex.myPlexAccount()] + plex.myPlexAccount().users()
    for user in users:
        # We need the full URL for the user's avatar
        user.thumbUrl = user.thumb
    
    is_online = check_internet_connection()
    return render_template('user_select.html',
                           users=users,
                           server_title=server_title,
                           is_online=is_online)

@app.route('/login/<username>')
def login(username):
    """Switches to a user and saves them in the session."""
    session['username'] = username
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    """Clears the session to log the user out."""
    session.clear()
    return redirect(url_for('user_select'))

def get_plex_instance():
    """Helper to get the Plex instance for the currently logged-in user."""
    if not plex: abort(500, "Plex server not connected.")
    
    username = session.get('username')
    if not username:
        return None # No user is logged in
    
    # Switch the plex object to the context of the logged-in user
    return plex.switchUser(username)

@app.route('/home')
def home():
    """The main dashboard for the logged-in user."""
    user_plex = get_plex_instance()
    if not user_plex: return redirect(url_for('user_select'))

    is_online = check_internet_connection()
    on_deck = user_plex.library.onDeck()
    recently_added = user_plex.library.recentlyAdded()

    for item in on_deck: item.thumbUrl = add_auth_to_url(item.thumb)
    for item in recently_added: item.thumbUrl = add_auth_to_url(item.thumb)

    return render_template('home_dashboard.html',
                           server_title=server_title,
                           is_online=is_online,
                           on_deck=on_deck,
                           recently_added=recently_added)

@app.route('/item/<int:rating_key>')
def item_details(rating_key):
    user_plex = get_plex_instance()
    if not user_plex: return redirect(url_for('user_select'))
    
    is_online = check_internet_connection()
    try:
        item = user_plex.fetchItem(rating_key)
        item.thumbUrl = add_auth_to_url(item.thumb)
        item.artUrl = add_auth_to_url(item.art)
        
        if item.type == 'show':
            for season in item.seasons():
                season.thumbUrl = add_auth_to_url(season.thumb)
                for episode in season.episodes():
                    episode.thumbUrl = add_auth_to_url(episode.thumb)

        return render_template('item_details.html', item=item, server_title=server_title, is_online=is_online)
    except NotFound:
        abort(404, "Media not found.")

# --- NEW: Routes for marking media as watched/unwatched ---
@app.route('/item/<int:rating_key>/mark_watched')
def mark_watched(rating_key):
    user_plex = get_plex_instance()
    if not user_plex: return redirect(url_for('user_select'))
    
    item = user_plex.fetchItem(rating_key)
    item.markWatched()
    return redirect(url_for('item_details', rating_key=rating_key))

@app.route('/item/<int:rating_key>/mark_unwatched')
def mark_unwatched(rating_key):
    user_plex = get_plex_instance()
    if not user_plex: return redirect(url_for('user_select'))
    
    item = user_plex.fetchItem(rating_key)
    item.markUnwatched()
    return redirect(url_for('item_details', rating_key=rating_key))


# --- Player and Search routes remain the same, but need the user context ---
@app.route('/player/<int:rating_key>')
def player(rating_key):
    user_plex = get_plex_instance()
    if not user_plex: return redirect(url_for('user_select'))
    
    try:
        item = user_plex.fetchItem(rating_key)
        stream_url = item.getStreamURL()
        return render_template('player.html', item=item, stream_url=stream_url)
    except NotFound:
        abort(404, "Media not found.")

@app.route('/search')
def search():
    user_plex = get_plex_instance()
    if not user_plex: return redirect(url_for('user_select'))
    
    query = request.args.get('query', '')
    is_online = check_internet_connection()
    results = []
    if query:
        results = user_plex.search(query)
        for item in results:
            item.thumbUrl = add_auth_to_url(item.thumb)

    return render_template('search_results.html', query=query, results=results, server_title=server_title, is_online=is_online)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)