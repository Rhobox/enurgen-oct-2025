import os
import peewee as pw
from flask import Flask, request, jsonify
from flask_cors import CORS
import click
import csv
import time

app = Flask(__name__, instance_relative_config=True)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

CORS(app)
app.config.from_mapping(
    SECRET_KEY='dev', # This is obviously not a good key
    DATABASE=os.path.join(app.instance_path, 'data.db'),
)

db = pw.SqliteDatabase(
    app.config['DATABASE'], 
    pragmas={'journal_mode': 'wal'} # Allows some concurrent read/writes
)

class Data(pw.Model):
    id = pw.AutoField() # Note that id fields are not a requirement for timeseries data.
    ts = pw.DateTimeField()
    source = pw.TextField()
    measure = pw.TextField()
    float_value = pw.FloatField()

    def __repr__(self):
        print(self.source, ' ', self.ts)

    class Meta:
        database = db

db.create_tables([Data])

@click.command('init-db')
def init_db_command():
    # Clears existing data and creates fresh tables.
    # Called via: `poetry run flask --app ./src/server.py init-db` from poetry root
    
    db.drop_tables([Data])
    db.create_tables([Data])
    click.echo('Initialized a fresh database.')

app.cli.add_command(init_db_command)

@app.route('/files', methods=['GET', 'POST'])
def files():
    """
    When called as a POST command parses and uploads the csv provided to the database.

    When called as a GET command returns the file names stored in the database.
    """
    if request.method == 'POST':
        if request.files:
            if not request.files:
                return jsonify(error="No files provided")
            
            new_rows = [] # For a very large number of rows this may cause memory problems
            for uploaded_file in request.files.getlist('data'):
                name = uploaded_file.filename
                print(name)
                decoded_uploaded_file = uploaded_file.read().decode()
                csv_readable_file = decoded_uploaded_file.split('\n')
                file = csv.reader(csv_readable_file, delimiter=',')
                header = next(file)
                for row in file:
                    for i, col in enumerate(row[1:]):
                        new_rows.append(Data(
                            ts=row[0],
                            source=name,
                            measure=header[i+1],
                            float_value=col
                            ))
                
            with db.atomic():
                Data.bulk_create(new_rows, batch_size=500)

    filenames = Data.select(Data.source).distinct()
    response = []
    for file in filenames:
        response.append(file.source)
    return jsonify(fileNames=response)