from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import os

app = Flask(__name__)

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route('/')
def home():
    return render_template('index.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/services')
def services():
    return render_template('Services.html')

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


@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    form = request.form

    data = {
        "name": form.get("name"),
        "email": form.get("email"),
        "message": form.get("message"),
        "wants_to_build": "idea_type" in form and form.get("idea_type") != "",
        "idea_type": form.get("idea_type"),

        # Game
        "game_platforms": request.form.getlist("game_platforms"),
        "game_timeframe": form.get("game_timeframe"),
        "game_budget": form.get("game_budget"),
        "game_idea": form.get("game_idea"),

        # App
        "app_platforms": request.form.getlist("app_platforms"),
        "app_problem": form.get("app_problem"),
        "app_budget": form.get("app_budget"),
        "app_details": form.get("app_details"),
    }

    # Clean out empty/null fields
    cleaned = {k: v for k, v in data.items() if v not in [None, "", [], "null"]}

    try:
        supabase.table("contact_submissions").insert(cleaned).execute()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/health')
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
