from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from model import db, app, socketio, timedelta, emit, datetime, Record, Individuals, Schools, Parents
from random import randint
import json
import os
from os import listdir
import random
from os.path import isfile, join
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(ROOT_DIR + '/ML-Models/Similarity')
import SimilarityModel
sys.path.append(ROOT_DIR + '/ML-Models/Career')
import weight_loader

model, index2word_set = SimilarityModel.loadModel()

clf,encoder = weight_loader.load_career()

qna = {}
with open('qna.json') as f:
    qna = json.load(f)

nature = {}
with open('nature.json') as f:
    nature = json.load(f)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/individual', methods=['POST', 'GET'])
def individual():
    if request.method == 'POST':

        email = str(request.form['email'])
        school_email = str(request.form['school_email'])

        user = Individuals.query.filter_by(email=email).first()

        scores = {
            "visual": 0,
            "verbal": 0,
            "math": 0,
            "intrapersonal": 0,
            "logical": 0,
            "body": 0,
            "musical": 0,
            "nature": 0
        }

        metadata = {
            "email": email,
            "uuid": ""
        }

        uuid = randint(1000, 9999)

        if user is not None:
            records = Record.query.filter_by(email=email).order_by(Record.record_date.desc()).all()

            if records is not None:
                for record in records:
                    scores[str(record.score_type)] = max(scores[str(record.score_type)], int(record.score))

            metadata["uuid"] = user.uuid
        else:
            db.session.add(Individuals(email=email, uuid=uuid))
            db.session.commit()
            metadata["uuid"] = uuid

        if school_email != "":
            school_entry = Schools.query.filter_by(individual_email=email, school_email=school_email).first()
            if school_entry is None:
                db.session.add(Schools(individual_email=email, school_email=school_email))
                db.session.commit()

        session['ind_email'] = str(email)
        session['ind_uuid'] = str(metadata['uuid'])

        return render_template('individual.html', result=scores, metadata=metadata)

@app.route('/school', methods=['POST', 'GET'])
def school():
    #global ind_uuid, ind_email
    if request.method == 'POST':
        school_email = str(request.form['school_email'])

        studentScores = {}

        listOfStudents = []

        users = Schools.query.filter_by(school_email=school_email).all()
        for user in users:
            records = Record.query.filter_by(email=user.individual_email).order_by(Record.record_date.desc()).all()
            if user.individual_email not in studentScores:
                studentScores[user.individual_email] = {
                    "visual": 0,
                    "verbal": 0,
                    "math": 0,
                    "intrapersonal": 0,
                    "logical": 0,
                    "body": 0,
                    "musical": 0,
                    "nature": 0
                }
            for record in records:
                studentScores[user.individual_email][str(record.score_type)] = max(studentScores[user.individual_email][str(record.score_type)], int(record.score))

            listOfStudents.append(user.individual_email)

        sorted_by_visual = sorted(studentScores.items(), key=lambda x: (x[1]['visual']))
        sorted_by_verbal = sorted(studentScores.items(), key=lambda x: (x[1]['verbal']))
        sorted_by_math = sorted(studentScores.items(), key=lambda x: (x[1]['math']))
        sorted_by_intrapersonal = sorted(studentScores.items(), key=lambda x: (x[1]['intrapersonal']))
        sorted_by_logical = sorted(studentScores.items(), key=lambda x: (x[1]['logical']))
        sorted_by_body = sorted(studentScores.items(), key=lambda x: (x[1]['body']))
        sorted_by_musical = sorted(studentScores.items(), key=lambda x: (x[1]['musical']))
        sorted_by_nature = sorted(studentScores.items(), key=lambda x: (x[1]['nature']))

        return render_template('school.html', list_of_students=listOfStudents, school_email=school_email)

    else:
        return render_template('school.html')

@app.route('/parent', methods=['POST', 'GET'])
def parent():
    global clf,encoder
    if request.method == 'POST':

        email = str(request.form['email'])

        children = Parents.query.filter_by(parent_email=email).all()

        graph_scores = {
            "visual": [],
            "verbal": [],
            "math": [],
            "intrapersonal": [],
            "logical": [],
            "body": [],
            "musical": [],
            "nature": []
        }

        graph_dates = []

        child_email = ""

        if children is not None:

            for child in children:

                child_email = child.child_email

                N = 30
                while(N >= 0):
                    start_date = datetime.now() - timedelta(N)
                    graph_dates.append(start_date.strftime('%d/%m'))
                    N -= 1
                    for key, value in graph_scores.items():
                        record = Record.query.filter_by(email=child.child_email, score_type=key, record_date=start_date.date()).first()
                        value.append(record.score) if record is not None else value.append(0)

        # maze , math, music, video , natural , body

        input = []
        features = ["visual","verbal","math","body","musical","logical","intrapersonal","nature"]

        for feature in features:
            record = Record.query.filter_by(email=child_email,record_date=datetime.now().date(),score_type=feature).first()
            if record is not None:
                input.append(record.score)
            else:
                input.append(0)

        predicted = clf.predict([input])
        career_name = list(encoder.inverse_transform(predicted))

        return render_template('parent.html', graph_dates=graph_dates, graph_scores=graph_scores, child_email=child_email, career_name=career_name[0])


@app.route('/game/maze')
def game_maze():
    return render_template('maze-index.html')


@app.route('/game/maths')
def game_maths():
    return render_template('maths-index.html')

@app.route('/game/body')
def game_body():
    return redirect("https://storage.googleapis.com/tfjs-models/demos/posenet/camera.html")

@app.route('/game/video', methods=['POST', 'GET'])
def game_video():
    global qna, model, index2word_set
    if request.method == 'GET':

        video_name = 'v1'
        video_path = 'videos/'+video_name+'.mp4'
        listOfQuestions = []

        questions = qna[video_name]

        for key, value in questions.items():
            listOfQuestions.append(value["question"])

        return render_template('video-index.html', listOfQuestions=listOfQuestions, video_name=video_name, video_path=video_path)

    if request.method == 'POST':

        score = 0
        n_score = 0

        for key, value in request.form.to_dict().items():
            a,b = key.split("-")
            exp_answers = qna[a][b]["answers"]
            maxScore = 0.0
            value = value.lower()
            for ea in exp_answers:
                ea = ea.lower()
                maxScore = max(maxScore,SimilarityModel.predict(model, index2word_set, ea, value))
            print(maxScore)

            if maxScore > 50.0:
                score += 1
            else:
                n_score += 1

        finalScore = (score / (score + n_score))*100

        pre_record = Record.query.filter_by(score_type="visual",record_date=datetime.now().date()).first()

        if pre_record is None:
            db.session.add(Record(email=session['ind_email'], score_type="visual", score=finalScore))
            db.session.commit()
        else:
            pre_record.score = max(pre_record.score, finalScore)
            db.session.commit()

        emit('video', {'final_score' : finalScore, "status" : "finish"}, broadcast=True, namespace='/individual/'+session['ind_uuid'])

        return "Your Feedback is submitted! This Window will automatically close shortly!!"

@app.route('/game/music', methods=['POST', 'GET'])
def game_music():
    global qna, model, index2word_set
    if request.method == 'GET':

        musicFilesPath = ROOT_DIR + '/static/music/'
        musicfiles = [f for f in listdir(musicFilesPath) if isfile(join(musicFilesPath, f))]
        musicfiles = [x for x in musicfiles if x != ".DS_Store"]

        random.shuffle(musicfiles)

        finalMusicFilesNames = musicfiles[0:5]

        finalMusicFilesPath = [('music/'+x) for x in finalMusicFilesNames]

        onlyNames = []

        for musicName in finalMusicFilesNames:
            a,b = musicName.split("-")
            onlyNames.append(a)

        return render_template('music-index.html', finalMusicFilesPath=finalMusicFilesPath, onlyNames=onlyNames)

    if request.method == 'POST':

        score = 0
        n_score = 0

        for key, value in request.form.to_dict().items():
            a,b,c = key.split("-")
            if c == value:
                score += 1
            else:
                n_score += 1

        finalScore = (score / (score + n_score)) * 100

        pre_record = Record.query.filter_by(score_type="musical", record_date=datetime.now().date()).first()

        if pre_record is None:
            db.session.add(Record(email=session['ind_email'], score_type="musical", score=finalScore))
            db.session.commit()
        else:
            pre_record.score = max(pre_record.score, finalScore)
            db.session.commit()

        emit('music', {'final_score' : finalScore, "status" : "finish"}, broadcast=True, namespace='/individual/'+session['ind_uuid'])

        return "Your Feedback is submitted! This Window will automatically close shortly!!"

@app.route('/game/nature', methods=['POST', 'GET'])
def game_nature():
    global qna, model, index2word_set, nature
    if request.method == 'GET':

        natureFilesPath = ROOT_DIR + '/static/nature/'
        naturefiles = [f for f in listdir(natureFilesPath) if isfile(join(natureFilesPath, f))]
        naturefiles = [x for x in naturefiles if x != ".DS_Store"]

        random.shuffle(naturefiles)

        finalNatureFilesNames = naturefiles[0:5]

        finalNatureFilesPath = [('nature/'+x) for x in finalNatureFilesNames]

        onlyNames = []

        for musicName in finalNatureFilesNames:
            a,b = musicName.split(".")
            onlyNames.append(a)

        return render_template('nature-index.html', finalNatureFilesPath=finalNatureFilesPath, onlyNames=onlyNames)

    if request.method == 'POST':

        score = 0
        n_score = 0

        for key, value in request.form.to_dict().items():
            a,b = key.split("~")
            maxScore = 0
            value = value.lower()
            for ea in nature[a]['answers']:
                ea = ea.lower()
                maxScore = max(maxScore,SimilarityModel.predict(model, index2word_set, ea, value))
            if maxScore > 50.0:
                score += 1
            else:
                n_score += 1

        finalScore = (score / (score + n_score)) * 100

        pre_record = Record.query.filter_by(score_type="nature", record_date=datetime.now().date()).first()

        if pre_record is None:
            db.session.add(Record(email=session['ind_email'], score_type="nature", score=finalScore))
            db.session.commit()
        else:
            pre_record.score = max(pre_record.score, finalScore)
            db.session.commit()

        emit('nature', {'final_score' : finalScore, "status" : "finish"}, broadcast=True, namespace='/individual/'+session['ind_uuid'])

        return "Your Feedback is submitted! This Window will automatically close shortly!!"

@socketio.on('maze')
def handle_maze_game(json):

    if json['status'] == 'finish':
        finalScore = json['final_score']
        pre_record = Record.query.filter_by(score_type="logical", record_date=datetime.now().date()).first()

        if pre_record is None:
            db.session.add(Record(email=session['ind_email'], score_type="logical", score=finalScore))
            db.session.commit()
        else:
            pre_record.score = max(pre_record.score, finalScore)
            db.session.commit()

    emit('maze', json, broadcast=True, namespace='/individual/'+session['ind_uuid'])
    print('Maze received json: ' + str(json))

@socketio.on('maths')
def handle_maths_game(json):

    if json['status'] == 'finish':
        finalScore = json['final_score']
        pre_record = Record.query.filter_by(score_type="math", record_date=datetime.now().date()).first()

        if pre_record is None:
            db.session.add(Record(email=session['ind_email'], score_type="math", score=finalScore))
            db.session.commit()
        else:
            pre_record.score = max(pre_record.score, finalScore)
            db.session.commit()

    emit('maths', json, broadcast=True, namespace='/individual/'+session['ind_uuid'])
    print('Maths received json: ' + str(json))

@socketio.on('video')
def handle_video_game(json):
    emit('video', json, broadcast=True, namespace='/individual/'+session['ind_uuid'])
    print('Video received json: ' + str(json))

@socketio.on('music')
def handle_video_game(json):
    emit('music', json, broadcast=True, namespace='/individual/'+session['ind_uuid'])
    print('Music received json: ' + str(json))

@socketio.on('nature')
def handle_nature_game(json):
    emit('nature', json, broadcast=True, namespace='/individual/'+session['ind_uuid'])
    print('Nature received json: ' + str(json))

@socketio.on('body')
def handle_body_game(json):
    emit('body', json, broadcast=True, namespace='/individual/'+session['ind_uuid'])
    print('Body received json: ' + str(json))

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)
