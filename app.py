from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "Oh-itisa-secret"

debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def starting_survey():
  "showing the survey"

  return render_template("start_survey.html", survey = satisfaction_survey)

@app.route("/questions/<num>")
def show_questions(num):
  "showing the question"
  test = satisfaction_survey.questions[int(num)]

  return render_template("questions.html", question = test, num = num)

@app.route("/answer")
def handle_answer():
  "append answer to responses list and redirect to the next q"

  responses.append(request.form["choice"])
  next_question = int(request.form["num"]) + 1

  return redirect("/questions/<next_question>")


