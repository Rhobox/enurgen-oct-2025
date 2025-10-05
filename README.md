# enurgen-oct-2025

### Assumptions
* Valid CSV file is provided
* CSV files are provided with `ts` as the first header/column
    * Could trivially be changed to the row that has `ts`, but for ease of use right now it's the first header


### Shortcuts
* Uses the flask development server, hosts to localhost


Database can be cleared by deleting the instance folder and restarting the server or by running:
`poetry run flask --app ./src/server.py init-db` 
from poetry root (`Flask/enurgen-demo`).

Flask server can be run via:
`poetry run flask --app ./src/server.py run -p 5001`
Note that Flask has a default of 5000 which can cause issues on mac.

React frontend can be run with `npm run dev` from `React/enurgen-demo/`


## Notes:

Due the nature of timeseries data, and for speed (of insert and development) it doesn't check if a record exists.

Not sure if the navbar on the left was for multiple pages later or a quick list of filenames. Given there's one page it populates an alternative file name list.

There is no method of viewing CSV data that has been processed in-app. I used a sqlite extension on VSCode.

It doesn't filter out duplicates, as there are no constraints given on name. This leaves an unwise amount of responsibility on the user to be aware of what they're uploading as unconstrained data.

To avoid setting up any filtering CORS is unrestricted.

There's cleanup to be done on the frontend, but it functions as expected.