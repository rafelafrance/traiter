from GoogleAPI import GoogleAPI
from apiclient import errors


class MapsEngine(GoogleAPI):
    """Wrapper class for the most common MapsEngine functions."""

    def __init__(self, config):
        """Initialize the service."""

        try:
            self._PROJECT_ID = config['project_id']
        except KeyError:
            raise ConfigError("Missing configuration element: project_id")

        # Initialize GoogleAPI instance and create storage service
        GoogleAPI.__init__(self, 'mapsengine')
        self.methods = self.get_methods()

        return


    def get_methods(self):
        """Print the currently available methods."""
        s = ''
        for i in dir(self):
            if not i[0].isupper() and i[0] != '_' and i != 'service':
                s += i
                s += '\t{0}'.format(getattr(self, i).__doc__)
                s += "\n"
        return s


    def upload_table(self, table_name, table_description, table_files, table_tags = []):
        """Create a table from a list of files."""

        response = self._create_placeholder(table_name, table_description, table_files, table_tags)

        try:
            table_id = response['id']
            print "New table ID: {0}".format(table_id)
            self._insert_files(table_id, table_files)

        except KeyError:
            print "Error uploading table files"
            print response

        return table_id


    def _create_placeholder(self, table_name, table_description, table_files, table_tags = []):
        """Create an empty placeholder. First step of uploading files to a table."""

        filenames = []

        for name in table_files:
            filenames.append({
                "filename": "%s" % name
            })

        fileupload = {
            "projectId": self._PROJECT_ID,
            "name": table_name,
            "description": table_description,
            "files": filenames,
            "draftAccessList": "Map Editors",
            "tags": table_tags,
            "schema": {
                "primaryKey": "occ_id"
            }
        }

        print "Creating empty table with structure:\n{0}".format(fileupload)

        # Create placeholder
        request = self.service.tables().upload(body=fileupload)
        response = request.execute()
        return response


    def _insert_files(table_id, table_files):
        """Insert content of files in table. Second step of uploading files to a table."""

        for name in table_files:
            print "Waiting 2 seconds"
            time.sleep(2)

            try:
                print "Setting up insert request"
                freq = self.service.tables().files().insert(id=table_id,
                                                          filename=name,
                                                          media_body=name)
                print "Calling insert request"
                freq.execute()
                print "Finished uploading %s" % name
            except Exception as e:
                print "Unable to insert '%s'" % name
                print e

        return


    def list_tables(self):
        """List the tables that are accessible for the current user."""

        request = self.service.tables().list(projectId = self._PROJECT_ID)
        response = request.execute()
        res = response['tables']

        return res


    def delete_table(self):
        return


    def check_table(self, tableId):
        request = self.service.tables().get(id=tableId)
        response = request.execute()
        print json.dumps(response, indent=2)
        return


    def read_table(self, table_id):
        request = self.service.tables().features().list(id=table_id)
        response = request.execute()
        print json.dumps(response, indent=2)
        return
