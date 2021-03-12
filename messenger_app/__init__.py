# Python Imports
import os
import json

# Flask Imports
from flask import Flask, render_template, request, session, url_for, redirect

# Database Imports
from .database import utils


def create_messenger_app():
    """
    Messenger App
    """
    # Set Flask Name
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'alskdjfalj#123'

    # Set Database File Path
    app.config.from_mapping(DATABASE="messenger_app\database\db.sqlite")

    # Initialize App -- Allows 'init-db' to be called
    utils.initialize_app(app)

    #############################################################
    # Routes
    #############################################################
    @app.route('/', methods=['GET', 'POST'])
    def landing():
        """
        Landing Page - Create Chat Room || Enter Chat Room || View Chat Rooms
        """
        # Get Threads
        threads = utils.get_db().execute(
            "SELECT * FROM thread;"
        ).fetchall()

        return render_template('landing.html', threads=threads)


    @app.route('/thread', methods=["GET", "POST"])
    def thread():
        """
        Thread Route - Create Thread
        """
        if request.method == "POST":
            # Get Input
            username = request.form["username"]
            
            # Convert User Into List for First User
            username = [username]

            # Dump User To Store as String (SQLite doesnt allow arrays)
            users = json.dumps(username)

            # Create Thread
            conn = utils.get_db()
            db_cursor = conn.cursor()
            db_cursor.execute(
                'INSERT INTO thread (users)'
                ' VALUES (?)',
                (users,)
            )
            conn.commit()

            # Store Session Variables
            session['username'] = username
            session['thread_id'] = db_cursor.lastrowid

            # Return Thread ID (For Testing Purposes)
            if "RETURN" in request.headers and request.headers["RETURN"] == "1":
                return {"thread_id": db_cursor.lastrowid}

            return redirect(url_for(f"get_thread", thread_id=session['thread_id'], username=session['username']))

        elif request.method == "GET":
            # Get Thread
            thread = utils.get_db().execute(
                'SELECT * FROM thread WHERE id = ?;', (request.args.get("thread_id"),)
            ).fetchone()

            # Check If Thread Exists
            if thread:
                # Store Session Variables
                session['username'] = request.args.get("username")
                session['thread_id'] = request.args.get("thread_id")

                return redirect(url_for(f"get_thread", thread_id=session['thread_id'], username=session['username']))
            
            return redirect(url_for('landing'))


    @app.route("/thread/<int:thread_id>/", methods=["GET"])
    def get_thread(thread_id):
        """
        Get Thread
        """
        # Get Thread
        thread = utils.get_db().execute(
            'SELECT * FROM thread WHERE id = ?;', (str(thread_id),)
        ).fetchone()

        # Check If Thread Exists
        if thread is None:
            return render_template("landing/view.html")

        # Convert Thread To Dict
        dict_thread = dict(thread)

        # Check Messages
        if dict_thread["messages"] is None:
            dict_thread["messages"] = []
        
        # Store Session Variables
        session['username'] = request.args.get("username")
        session['thread_id'] = thread_id

        # Confirm Messages Is Object (Key: Value)
        try:
            messages = json.loads(dict_thread["messages"])
        except TypeError:
            messages = dict_thread["messages"]
        
        # Return Thread Messages (For Testing Purposes)
        if "RETURN" in request.headers and request.headers["RETURN"] == "1":
            return {"messages": messages}

        return render_template("view.html", thread_id=thread_id, username=session['username'], messages=messages)
    

    @app.route("/thread/<int:thread_id>/<username>", methods=["POST"])
    def message(thread_id, username):
        """
        Message Route - Send Message In Thread
        """
        # Get Input
        message = request.form["message"]

        # Get Thread
        thread = utils.get_db().execute(
            "SELECT * FROM thread WHERE id = ?;", (str(thread_id),)
        ).fetchone()

        # Setup Messages/Message
        messages = []
        message = {'username': f'{username}', 'message': f'{message}'}

        # Form Message
        if thread["messages"] is None:
            messages.append(message)
        else:
            messages.extend(eval(thread["messages"]))
            messages.append(message)

        messages = json.dumps(messages)
        
        # Update Thread Messages
        db = utils.get_db().cursor()
        db.execute(
            'UPDATE thread SET messages = ?'
            'WHERE id = ?',
            (messages, thread_id)
        )
        utils.get_db().commit()

        # Store Session Variables
        session['username'] = username
        session['thread_id'] = thread_id

        return "204"


    @app.route("/thread/<int:thread_id>/history", methods=["GET"])
    def history(thread_id):
        """
        History Route - Chat History
        """
        # Get Thread
        thread = utils.get_db().execute(
            "SELECT * FROM thread WHERE id = ?;", (str(thread_id),)
        ).fetchone()

        # Convert Thread To Dict
        dict_thread = dict(thread)

        # Check Messages
        if dict_thread["messages"] is None:
            dict_thread["messages"] = []

        # Confirm Messages Is Object (Key: Value)
        try:
            messages = json.loads(dict_thread["messages"])
        except TypeError:
            messages = dict_thread["messages"]

        return render_template("chat_history.html", thread=dict_thread, username=request.args.get("username"), messages=messages)

    return app
