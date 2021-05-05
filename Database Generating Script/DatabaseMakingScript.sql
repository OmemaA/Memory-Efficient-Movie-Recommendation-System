
CREATE TABLE users(
    userID SERIAL NOT NULL PRIMARY KEY,
    userName varchar(255) NOT NULL,
    userEmail varchar(255) NOT NULL,
    userPassword VARCHAR(255) NOT NULL,
    userGender VARCHAR(255) NOT NULL
);


CREATE TABLE movies(
    movieID INT NOT NULL PRIMARY KEY,
    movieName varchar(255) NOT NULL,
    moviePlot varchar(1000),
    imdbID VARCHAR(20) NOT NULL,
    posterLink VARCHAR(500),
    movieBloomFilter bytea,
    movieSimilarTo bytea
);

CREATE TABLE userHasWatched (
    UserID INTEGER REFERENCES users(userID),
    MovieID INTEGER REFERENCES movies(movieID),
    Rating INTEGER NOT NULL,
    PRIMARY KEY(UserID,movieID)
);

CREATE TABLE UserLikes (
    UserID INTEGER REFERENCES users(userID),
    MovieID INTEGER REFERENCES movies(movieID),
    PRIMARY KEY(UserID,MovieID)
);
