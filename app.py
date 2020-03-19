from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "Oh-itisa-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def starting_survey():
    "Allows user to begin survey"

    return render_template("start_survey.html", survey=satisfaction_survey)

@app.route("/start", methods=["POST"])
def start_survey():
    "Sets initial session values and redirects user to survey."
    session["answers"] = []
    session["question_num"] = 0
    
    return redirect("/questions/0") 


@app.route("/questions/<num>")
def show_questions(num):
    """Shows the next unanswered question in the survey,
    if user tries to enter different question, redirects them"""
    
    if not int(num) == int(session["question_num"]):
        if int(session["question_num"]) >= len(satisfaction_survey.questions):
            return redirect("/thankyou")
        else:
            rightnum = session["question_num"]
            flash("WRONG QUESTION")
            print("Flash message", "Rightnum", rightnum, "Num", num)
            return redirect(f"/questions/{rightnum}") 

    question = satisfaction_survey.questions[int(num)]
    
    session["question_num"] = num

    return render_template("questions.html", question=question)


@app.route("/answer", methods=["POST"])
def handle_answer():
    "append answer to responses list and redirect to the next question"

    session["answers"].append(request.form["choice"])
    
    session["question_num"] = int(session["question_num"]) + 1
    num = session["question_num"]
    
    print("Your answers so far", session["answers"])

    #May want to impliment an active survey variable?
    if int(num) >= len(satisfaction_survey.questions):
        return redirect("/thankyou")
    else:
        return redirect(f"/questions/{num}") 

@app.route("/thankyou")
def end_survey():
    return render_template("thankyou.html")