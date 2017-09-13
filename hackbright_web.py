"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def homepage():
    students, projects = hackbright.get_students_and_projects()

    return render_template("homepage.html", students=students, projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    if github:

        first, last, github = hackbright.get_student_by_github(github)

        rows = hackbright.get_grades_by_github(github)

        return render_template("student_info.html", first=first, last=last,
                               github=github, rows=rows)
    else:
        return render_template("student_info.html")


@app.route("/add-confirmation", methods=["POST"])
def add_confirmation():
    """ ADD a student """
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    github = request.form.get('github')

    hackbright.make_new_student(fname, lname, github)

    first, last, github = hackbright.get_student_by_github(github)

    return render_template("student_added_confirmation.html", github=github)


@app.route("/add-project-confirmation", methods=["POST"])
def add_project_confirmation():
    """ ADD a project """
    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.make_new_project(title, description, max_grade)

    title, description, max_grade = hackbright.get_project_by_title(title)

    return render_template("project_added_confirmation.html", title=title)


@app.route("/project")
def show_project():
    title = request.args.get('title')
    if title:
        project = hackbright.get_project_by_title(title)

        students = hackbright.get_grades_by_title(title)

        return render_template("show_project.html", project=project, students=students)
    else:
        return render_template("show_project.html")

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
