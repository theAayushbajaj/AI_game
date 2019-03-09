from model import db, Record
import random
from datetime import datetime, timedelta

N = 30
features = ["visual","verbal","math","intrapersonal","logical","body","musical","nature"]
while (N >= 0):
    start_date = datetime.now() - timedelta(N)
    email = "vasu@gmail.com"
    for i in range(4):
        finalScore = random.randint(10,70)
        choice = random.choice(features)
        print(choice)
        pre_record = Record.query.filter_by(score_type=choice, record_date=start_date.date()).first()

        if pre_record is None:
            db.session.add(Record(email=email, score_type=choice, score=finalScore, record_date=start_date.date()))
            db.session.commit()
        else:
            pre_record.score = max(pre_record.score, finalScore)
            db.session.commit()
    N -= 1
