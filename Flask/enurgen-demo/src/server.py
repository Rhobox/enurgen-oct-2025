import os
import peewee as pw
from flask import Flask, Response, request, jsonify
from peewee import SqliteDatabase, Model
from datetime import datetime
import click, csv

app = Flask(__name__, instance_relative_config=True)
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

    class Meta:
        database = db

db.create_tables([Data])

@click.command('init-db')
def init_db_command():
    # Clears existing data and creates fresh tables.
    
    db.drop_tables([Data])
    db.create_tables([Data])
    click.echo('Initialized a fresh database.')

app.cli.add_command(init_db_command)

@app.route('/')
def index():
    new_test_data = Data.create(
        ts=datetime.now(),
        source='file_a.csv',
        measure='measure_a',
        float_value=17.223
    )
    new_test_data.save()
    count = Data.select().count()
    return '{0}'.format(count)

@app.route('/files', methods=['GET', 'POST'])
def files():
    if request.method == 'POST':
        if request.files:
            name = request.files['data'].filename
            uploaded_file = request.files['data'].read().decode()
            csv_readable_file = uploaded_file.split('\n')
            file = csv.reader(csv_readable_file, delimiter=',')
            header = next(file)
            count = 0
            with db.atomic():
                for row in file:
                    count += 1
                    for i, col in enumerate(row[1:]):
                        new_row = Data.create(
                            ts=row[0],
                            source=name,
                            measure=header[i+1],
                            float_value=col
                        )
                        new_row.save()
        
            return 'Added {0} rows.\n'.format(count)
        
        return 'No file provided.\n'

    filenames = Data.select(Data.source).distinct()
    response = []
    for file in filenames:
        response.append(file.source)
    return jsonify(fileNames=response)