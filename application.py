from flask import Flask, render_template,request,redirect,url_for,session
from flask_session import Session
app = Flask(__name__)
from omdb import OMDBClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from bloomfilter import bloomFilter
DATABASE_URL= "postgres+psycopg2://postgres:hello@localhost:5432/movies"
engine= create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)
app.config["SESSION_PERMENANT"]=False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
API_KEY= "cd690ad8"
client=OMDBClient(apikey=API_KEY)

def findsimilar(movieid):
    global session,db
    db.rollback()
    bloommovie=db.execute("SELECT movieID,movieBloomFilter from movies",{"movieid":movieid})
    bloomdictionary={movie_id:bloomFilter(bits1=bytes(bloom),total=7000,hashes=3) for movie_id,bloom in bloommovie}
    ourbloom=bloomdictionary[movieid]
    for movie_id,bloom in bloomdictionary.items():
        if movieid!=movie_id:
            if bloom.similarity_value(ourbloom)>0.33:
                a=db.execute("SELECT * from userLikes where UserID=:userid and (movieID in (select movieID from userhaswatched where userid=:userid) or movieID=:movieid)",{"userid":session["id"],"movieid":movieid}).fetchall()
                if len(a)==0:
                    db.execute("INSERT INTO userlikes(userid,movieid) VALUES(:user,:newmovie)",{"user":session["id"],"newmovie":movie_id})
                    db.commit()
    print("done <3")
def RecommendMainCode(id):
    movieinfo=client.imdbid(f"{id}")
    return movieinfo
    
    # link=f'<img src="{movieinfo["poster"]}" alt="{movieinfo["title"]}">'
    # title=f"<p1>{movieinfo["title"]}</p1>"

    return data

def parser(link):
    lst = link.split("/")
    for i in lst:
        if i[0:2] == "tt":
            return i


@app.route("/recommendations") #am hijacking for bit. easy stuff
def recommendations():
    id=session["id"]
    db.rollback()
    a=db.execute("SELECT distinct movies.movieid,movies.imdbid from userlikes inner join movies on userlikes.movieid = movies.movieid and posterlink is null;")
    for i in a:
    #     print(f'UPDATE movies SET movieplot= \'{movie["plot"]}\' WHERE movieid = {i[0]}')
        movieid=i[1]
        movie = RecommendMainCode(movieid)
        db.execute(f'UPDATE movies SET movieplot= :plot WHERE movieid = :id',{"plot":movie["plot"],"id":i[0]})
        db.execute(f'UPDATE movies SET posterlink = :poster WHERE movieid = :id',{"poster":movie["poster"],"id":i[0]})
    db.commit()
    a=db.execute("SELECT moviename, posterlink,movieplot from movies inner join userlikes on userlikes.movieid=movies.movieid where userlikes.userid=:id",
    {"id":id})
    movies=[]
    for i in a:
        movies.append({"title":i[0],"poster":i[1],"movieplot":i[2]})
    x=(len(movies)-3)//4 *4+3
    rows=[ movies[i:i+4]  for i in range(3,x,4)]
    return render_template("home.html",movies=enumerate(movies[:3]),rows=rows)
@app.route("/profile",methods=["GET","POST"])
def profile():
    if "id" not in session and request.method=="GET" :
        return render_template("InvalidSignin.html")
    else:
        if request.method=="POST":
            if "id" in session:
                print(session["id"])
                
                movieid=request.form.get("link")
                if movieid==None:
                    return render_template("Profile.html")
                movieid=parser(movieid)
                db.rollback()
                result=db.execute("SELECT movieID from movies where  imdbID = :movie",{"movie":movieid})
                for i in result:
                    ismoviein=db.execute("select movieID FROM userHasWatched where userid=:user and movieid = :movie",{"user":session["id"],"movie":i[0]})
                    ismoviein=len(list(ismoviein))>0
                    if not ismoviein:
                        db.execute("DELETE from userlikes where movieid=:movieid and userid=:user",{"user":session["id"],"movieid":i[0]})
                        db.execute("INSERT INTO userHasWatched(userid,movieid,rating) Values(:user,:movie,5)",{"user":session["id"],"movie":i[0]})
                        db.commit()
                        findsimilar(i[0])
                    # See if user,movie comb in 
                    # Else put in
                    # do recommendy stuff
                    # return str(i[0]) # id of movie
                return render_template("profile.html")
            try:
                email=request.form.get("email")
                password=request.form.get("password")
                x=db.execute("SELECT userid from users where useremail=:email and userpassword=:userpassword",{"email":email,"userpassword":password})
                flag=False
                for i in x:
                    flag=True
                    session["id"]=i[0]
                    print(session["id"])
            except:
                return "what the fudge"
            if flag==False:
                return "what the fudge"
    if request.method=="GET":
        return render_template("profile.html")

@app.route("/history",methods=["GET","POST"])
def history():
    # if "id" not in session and request.method=="GET" :
    #     return render_template("InvalidSignin.html")
    # else:
    #     if "id" in session:
    #         return "hello"
    #     if request.method=="POST":
    #         try:
    #             email=request.form.get("email")
    #             password=request.form.get("password")
    #             x=db.execute("SELECT userid from users where useremail=:email and userpassword=:userpassword",{"email":email,"userpassword":password})
    #             for i in x:
    #                 session["id"]=i[0]
    #                 print(session["id"])
    #         except:
    #             return "what the fudge"
    #         return render_template("thankyou.html")
    #     return "hello"
    # TODO: CHOOSE APPROPRIATE MOVIES
    db.rollback()
    id=session["id"]
    a=db.execute("SELECT distinct movies.movieid,movies.imdbid from userhaswatched inner join movies on userhaswatched.movieid = movies.movieid and posterlink is null;")
    for i in a:
    #     print(f'UPDATE movies SET movieplot= \'{movie["plot"]}\' WHERE movieid = {i[0]}')
        movieid=i[1]
        movie = RecommendMainCode(movieid)
        db.execute(f'UPDATE movies SET movieplot= :plot WHERE movieid = :id',{"plot":movie["plot"],"id":i[0]})
        db.execute(f'UPDATE movies SET posterlink = :poster WHERE movieid = :id',{"poster":movie["poster"],"id":i[0]})
    db.commit()

    a=db.execute("SELECT moviename, posterlink,movieplot from movies inner join userhaswatched on userhaswatched.movieid=movies.movieid where userhaswatched.userid=:id",
    {"id":id})
    movies=[]
    for i in a:
        movies.append({"title":i[0],"poster":i[1],"movieplot":i[2]})
    return render_template("history.html",movies=movies)

# @app.route("/<string:name>")
# def hello(name):
#     return f"Hello {name} idiot!"
# @app.route("")

@app.route("/signin")
def signin():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")
@app.route("/thanks",methods=["GET"])
def thanks():
    db.rollback()
    db.execute("INSERT INTO users(userName,userEmail,userPassword,userGender) VALUES (:userName , :userEmail,:userPassword,:userGender)",{"userName":request.args.get("username"),"userEmail":request.args.get("email"),"userPassword":request.args.get("password1"),"userGender":request.args.get("gender")})
    db.commit()    
    return render_template("thankyou.html")
