Installation:
-------------

    - Pre-requisites:
      ---------------

        - Python 2.6+
        - virtualenv
        - pip

    This is a command line tool to generate bigquery data types from existing mysql table. Follow instructions below to run it.

        - Create a virtualenv for this tool `virtualenv /some/directory/for/virtual/env`.
        - Switch to it by running `source /some/directory/for/virtual/env/bin/activate`.
        - Install dependencies by running `pip install -r requirements.txt`.


    To run this tool use the following arguments for example,

        `python bq-generate.py --host='127.0.0.1' --database='somedb' --table='sometable' --user='root' --password-from-file=/location/of/.passwordfile`

    If in doubt run `python bq-generate.py --help` to see usage of arguments


To-Do:
------

    - Currently only prints bigquery types as comma separated values to STDOUT. It would be good to get this to print a JSON data structure. 
    - Unit tests coverage.
    - Only works for mysql basic types. No blobs allowed.

