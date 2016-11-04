# start mongo
sudo mongod --fork --logpath data/log/mongod.log --dbpath data/db
# start apache

# TODO

# start server
uwsgi --ini courserecs.ini --plugin python3 --chmod-socket=666
