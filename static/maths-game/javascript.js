var playing = false;
var final_score={'score':0,'n_score':0,'final_score':0,'status':'-1'};
var timeremaining;
var static_time;
var action;
var final_score;
var correctAnswer;
var socket = io.connect('http://' + document.domain + ':' + location.port);
// Check game is start or reset
document.getElementById("startreset").onclick = function(){
    //var socket = io.connect('http://' + document.domain + ':' + location.port);
    final_score.status = 'start';
    socket.emit("maths" , final_score);
// if playing
    if(playing == true){
        //location.reload();
    }else{
        playing = true;
        document.getElementById("scorevalue").innerHTML = final_score.score;
        // Time counter
        show("timeremaining");
        timeremaining = 20;
        document.getElementById("timeremainingvalue").innerHTML = timeremaining;
        hide("gameover");
        document.getElementById("startreset").innerHTML = "Reset Game";
        // start countdown
        startCountdown();
        // generate a Q&A
        //generateQA();
        var i = random();
        eval('generateQA'+i+'()');
        static_time=timeremaining;
    }
}
for(i=1 ; i< 5; i++){
    document.getElementById("box"+i).onclick = function(){
    if(playing == true){
        if(this.innerHTML == correctAnswer){
            // for correct answer increase score by 1
            final_score.score ++;
            document.getElementById("scorevalue").innerHTML = final_score.score;
            hide("wrong");
            show("correct");
            setTimeout(function(){
                hide("correct");
            }, 1000);
            //generateQA();
            var k = random();
            eval('generateQA'+k+'()');
            static_time=timeremaining;
        }
        else{
            final_score.n_score ++;
            hide("correct");
            show("wrong");
            setTimeout(function(){
                hide("wrong");
                }, 1000);
            //generateQA();
            var k = random();
            eval('generateQA'+k+'()');
            static_time=timeremaining;
            }
        }
    }
}
function startCountdown(){
    action = setInterval(function(){
        timeremaining -=1;
        document.getElementById("timeremainingvalue").innerHTML = timeremaining;
        if(timeremaining == 0){
            stopCountdown();
            show("gameover");
            document.getElementById("gameover").innerHTML = "<p>Game Over!</p> <p>Your Score is " + final_score.score +  ".</p>"+"You gave "+final_score.n_score+" incorrect answers.";
            final_score['final_score'] = (final_score.score/(final_score.score+final_score.n_score))*100;
            console.log(final_score);
            //var socket = io.connect('http://' + document.domain + ':' + location.port);
            final_score.status = 'finish';
            socket.emit("maths" , final_score);
            hide("timeremaining");
            hide("correct");
            hide("wrong");
            playing = false;
            document.getElementById("startreset").innerHTML = "Start Game";
        }
        else if(static_time-timeremaining>=5)
        {   final_score.n_score ++;
            var k = random();
            eval('generateQA'+k+'()');
            static_time=timeremaining;
        }
    }, 1000);
}
function stopCountdown(){
    clearInterval(action);
}
//show an element
function show(Id){
    document.getElementById(Id).style.display = "block";
}
//hide an element
function hide(Id){
    document.getElementById(Id).style.display = "none";
}
// Questions and Answers Generation LOGIC
function generateQA1(){
    var x = 1 + Math.round(9*Math.random());
    var y = 1 + Math.round(9*Math.random());
    //var z = 1 + Math.round(9*Math.random());
    correctAnswer = x*y;
    document.getElementById("Qshow").innerHTML = x + "x" + y;
    var correctPostion = 1 + Math.round(3*Math.random());
    document.getElementById("box"+correctPostion).innerHTML = correctAnswer; // Correct Answer
    var anwsers = [correctAnswer];
        for(i=1 ; i<5 ; i++){
            if(i != correctPostion){
                var wrongAnswer;
                do{
                    wrongAnwser = (1 + Math.round(9 * Math.random())) *
                                  (1 + Math.round(9 * Math.random()));
                } while(anwsers.indexOf(wrongAnswer)>-1)
                document.getElementById("box"+i).innerHTML = wrongAnwser;
                anwsers.push(wrongAnwser);
            }
        }
}
function generateQA3(){
    var x = 1 + Math.round(9*Math.random());
    var y = 1 + Math.round(9*Math.random());
    correctAnswer = x+y;
    document.getElementById("Qshow").innerHTML = x + "+" + y;
    var correctPostion = 1 + Math.round(3*Math.random());
    document.getElementById("box"+correctPostion).innerHTML = correctAnswer; // Correct Answer
    var anwsers = [correctAnswer];
        for(i=1 ; i<5 ; i++){
            if(i != correctPostion){
                var wrongAnswer;
                do{
                    wrongAnwser = (1 + Math.round(9 * Math.random())) *
                                  (1 + Math.round(9 * Math.random()));
                } while(anwsers.indexOf(wrongAnswer)>-1)
                document.getElementById("box"+i).innerHTML = wrongAnwser;
                anwsers.push(wrongAnwser);
            }
        }
}
function generateQA2(){
    var x = 1 + Math.round(9*Math.random());
    var y = 1 + Math.round(9*Math.random());
    //var z = 1 + Math.round(9*Math.random());
    correctAnswer = x-y;

    document.getElementById("Qshow").innerHTML = x + "-" + y;
    var correctPostion = 1 + Math.round(3*Math.random());
    document.getElementById("box"+correctPostion).innerHTML = correctAnswer; // Correct Answer
    var anwsers = [correctAnswer];
        for(i=1 ; i<5 ; i++){
            if(i != correctPostion){
                var wrongAnswer;
                do{
                    wrongAnwser = (1 + Math.round(9 * Math.random())) *
                                  (1 + Math.round(9 * Math.random()));
                } while(anwsers.indexOf(wrongAnswer)>-1)
                document.getElementById("box"+i).innerHTML = wrongAnwser;
                anwsers.push(wrongAnwser);
            }
        }
}
function random(){
    var i  = Math.floor(Math.random()*20)%4;
    if(i<=0) return random();
    return i;
  }