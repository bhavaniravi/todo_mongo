
from datetime import datetime

from pymongo import MongoClient
import pymongo


class ToDoApplication:

    def __init__ ( self, argv ):
        self.argv = argv
        try:
            self.client = MongoClient()
            self.db = self.client.todo_db
            self.collection = self.db.todos
            self.collection.create_index([('title', pymongo.ASCENDING)], unique=True)
        except Exception as e:
            print ( "Oops! Error connecting to MongoDB: %s" % e )

    def help (self):
        print ("usage: %s <method>" % self.argv[0])
        print ("== Methods ==")
        print ("list   <done>                 list all incomplete tasks sorted by priority then chronologically")
        print ("help                          show this help")
        print ("add    <title,description>    add new task")
        print ("done   <title>                list all complete tasks chronologically")
        print ("delete <title>                deletes item with title")

    def run(self):
        """
        Runs function of respective command in help
        """
        if self.argv[1].lower() == "help":
            self.help()
        if self.argv[1].lower() == "list":
            try:
                self.list(self.argv[2]=="done")
            except IndexError:
                self.list()
        if self.argv[1].lower() == "add":
            self.add(title=self.argv[2],description=self.argv[3])
        if self.argv[1].lower() == "done":
            self.done(title=self.argv[2])
        if self.argv[1].lower() == "delete":
            self.delete(title=self.argv[2])

    def add(self, **kwargs):
        kwargs.update({"done":False,"created_at":datetime.now()})
        todo_id = self.collection.insert_one(kwargs).inserted_id
        print ("New todo added with id "+str(todo_id))

    def list(self,done=False):
        """
        lists all todo
        """
        if done:
            collection = self.collection.find({"done":True})
        else:
            collection = self.collection.find()

        for todo in collection:
            print (todo.values())

    def done(self, title):
        """
        marks node with title done
        """
        self.collection.update_one(
                        {"title": title},
                        {"$set": { "done": True }}
                    )
        print ("Todo marked done")

    def delete(self, title):
        """
        deletes a document based on title
        """
        self.collection.remove({"title":title})

if __name__ == "__main__":
    import sys

    try:
        app = ToDoApplication( sys.argv )
        app.run()
    except Exception as e:
        print (e)
