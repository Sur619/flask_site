CREATE TABLE IF NOT EXISTS mainmenu(
    id integer primary key autoincrement,
    title text not null,
    url text not null
);


CREATE TABLE IF NOT EXISTS posts(
    id integer PRIMARY KEY AUTOINCREMENT,
    title text not null,
    text text not null,
    url text not null,
    time integer not null
);