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

    grouped = {
        "Professional Work": [],
        "Hobby Projects": [],
        "School Projects": []
    }

    for project in projects:
        cat = project.get("category", "").lower()
        if "professional" in cat:
            grouped["Professional Work"].append(project)
        elif "hobby" in cat:
            grouped["Hobby Projects"].append(project)
        elif "school" in cat:
            grouped["School Projects"].append(project)

    return render_template("projects.html", grouped_projects=grouped)
    
if __name__ == '__main__':
    app.run(debug=True)
