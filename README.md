# enurgen-oct-2025

### Assumptions
* Valid CSV file is provided
* CSV files are provided with `ts` as the first header/column
    * Could trivially be changed to the row that has `ts`, but for ease of use right now it's the first header


### Shortcuts
* Uses the flask development server, hosts to localhost (Docker binds to `0.0.0.0`)

Run the image with:
`docker compose up --build`

Requires docker.

## Notes:

Due the nature of timeseries data, and for speed (of insert and development) it doesn't check if a record exists.

Not sure if the navbar on the left was for multiple pages later or a quick list of filenames. Given there's one page it populates an alternative file name list.

There is no method of viewing CSV data that has been processed in-app. I used a sqlite extension on VSCode to manually verify uploads.

It doesn't filter out duplicates, as there are no constraints given on name. This leaves an unwise amount of responsibility on the user to be aware of what they're uploading as unconstrained data.

To avoid setting up any filtering CORS is unrestricted.