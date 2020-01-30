import pyodbc
import re
import json
from . import ResponseHandler
from . import Project

class ResponseHandler():

    # The map of table name substitutions
    table_dict = {
        "server": "Servers",
        "project": "Projects"
    }

    # The set of rules to
    rule_dict = ["t0.project_id = t1.project_id",
                 "t1.server_id = t2.server_id"]

    '''
    Handles every request that describes a query for data and returns the corresponding
    result set. Every result is converted to json before they are returned.
    '''
    def handle(request):
        # Retrieve the path from the request object
        request_url = request.path

        statement = ''

        # Check if the request was made for "all projects"
        if 'projects' in request_url:
            statement = 'Select * from Projects;'
        # Check if the request was made for "all servers"
        elif 'servers' in request_url:
            project_id = ResponseHandler.get_request_param_at(request, 2)
            statement = 'Select * from Projects t0, Servers t1 where t0.project_id = ' + project_id + ' AND t0.project_id = t1.project_id;'
        else:
            # Split up the url sections
            request_url_split = request_url.split('/')
            # Strip white spaces from the list
            request_url_split = ResponseHandler.strip_whitespaces(request_url_split)

            tabs = []
            cons = []

            # Loop over every section url section
            for i in range(0, len(request_url_split), 2):
                tabs.append(request_url_split[i])
                cons.append(request_url_split[i+1])

            statement = ResponseHandler.assemble_query(tabs, cons)

        cursor, result = ResponseHandler.execute_query(statement)
        json = ResponseHandler.to_json(cursor, result)
        return json

    def assemble_query(tabs, cons):
        query = 'SELECT * FROM '

        for i in range(len(tabs)):
            query += (ResponseHandler.get_table_name(tabs[i]) + ' t' + str(i))
            if i != len(tabs)-1: query += ', '

        query += ' WHERE '

        # Add the corresponding query rules depending on the "depth" of the query
        for i in range(len(tabs) - 1):
            if i < len(ResponseHandler.rule_dict):
                query += (ResponseHandler.rule_dict[i] + ' AND ')

        for i in range(len(cons)):
            query += ('t' + str(i) + "." + tabs[i] + '_id = ' + cons[i])
            if i != len(cons)-1: query += ' AND '

        query += ';'

        return query

    '''
    Executes a specific t-SQL query and returns the result set.
    '''
    def execute_query(sql):
        server = '127.0.0.1'
        database = 'Middleware'
        username = ''
        password = ''

        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
        cursor = connection.cursor()
        result = cursor.execute(sql)

        return cursor, result

    def strip_whitespaces(string):
        return list(filter(None, string))

    def get_table_name(identifier):
        return ResponseHandler.table_dict.get(identifier)

    '''
    Converts a specific result set to json.
    '''
    def to_json(cursor, result):
        # build list of column names tp use as dictionary keys from sql results
        columns = [column[0] for column in result.description]

        query_results = []
        for row in cursor.fetchall():
            query_results.append(dict(zip(columns, row)))

        output = {"MetaData": ResponseHandler.get_meta_data(), "Data":query_results}

        return json.dumps(output, sort_keys=True, indent=4)

    def get_meta_data():
        return '{}'

    def create_project(request):
        return 'project created'

    def get_request_param_at(request, index):
        return request.path.split('/')[index]
