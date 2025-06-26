from flask import Flask, render_template, jsonify
from supabase import create_client, Client
import os

app = Flask(__name__)

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/projects')
def get_projects():
    response = supabase.table('projects').select("*").execute()
    projects = response.data

    # Group by category
    grouped = {
        "Professional": [],
        "Hobby": [],
        "School": []
    }

    for project in projects:
        cat = project['category']
        if cat in grouped:
            grouped[cat].append(project)

    return render_template("projects.html", grouped_projects=grouped)

if __name__ == '__main__':
    app.run(debug=True)