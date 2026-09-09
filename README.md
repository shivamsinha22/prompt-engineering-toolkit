In the terminal, type:

bash
ls

to confirm the zip is there, then run:

bash
unzip prompt-engineering-toolkit-no-flask.zip -d .

Then:

bash
ls

again — you should now see app.py, toolkit/, templates/ etc. Then run:

bash
python app.py
If unzip command doesn't exist, run this instead:

bash
python3 -c "import zipfile; zipfile.ZipFile('prompt-engineering-toolkit-no-flask.zip').extractall('.')"
