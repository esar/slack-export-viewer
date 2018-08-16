import json
import os
import glob
import io

from slackviewer.message import Message

class Reader(object):
    """
    Reader object will read all of the archives' data from the json files
    """

    def __init__(self, PATH):
        self._PATH = PATH
        # TODO: Make sure this works
        self.__USER_DATA = {}
        with io.open(os.path.join(self._PATH, "metadata.json")) as f:
            metadata = json.load(f)
            for id,name in metadata['users'].items():
              self.__USER_DATA[id] = {'name': name}

        #with io.open(os.path.join(self._PATH, "users.json"), encoding="utf8") as f:
        #    self.__USER_DATA = {u["id"]: u for u in json.load(f)}


    ##################
    # Public Methods #
    ##################

    def compile_channels(self):
        channel_names = os.listdir(os.path.join(self._PATH, 'channels'))
        channel_names = [os.path.splitext(x)[0] for x in channel_names]
        
        #channel_data = self._read_from_json("channels.json")
        #channel_names = [c["name"] for c in channel_data.values()]

        return self._create_messages('channels', channel_names, None) #channel_data)

    def compile_groups(self):
        group_names = os.listdir(os.path.join(self._PATH, 'private_channels'))
        group_names = [x for x in group_names if not x.startswith('mpdm-')]
        group_names = [os.path.splitext(x)[0] for x in group_names]

        #group_data = self._read_from_json("groups.json")
        #group_names = [c["name"] for c in group_data.values()]

        return self._create_messages('private_channels', group_names, None) #group_data)

    def compile_dm_messages(self):
        dm_names = os.listdir(os.path.join(self._PATH, 'direct_messages'))
        dm_names = [os.path.splitext(x)[0] for x in dm_names]
        return self._create_messages('direct_messages', dm_names, None, True)

        ## Gets list of dm objects with dm ID and array of members ids
        #dm_data = self._read_from_json("dms.json")
        #dm_ids = [c["id"] for c in dm_data.values()]

        ## True is passed here to let the create messages function know that
        ## it is dm data being passed to it
        #return self._create_messages(dm_ids, dm_data, True)

    def compile_dm_users(self):
        """
        Gets the info for the members within the dm

        Returns a list of all dms with the members that have ever existed

        :rtype: [object]
        {
            id: <id>
            users: [<user_id>]
        }

        """
        dm_names = os.listdir(os.path.join(self._PATH, 'direct_messages'))
        dm_names = [os.path.splitext(x)[0] for x in dm_names]
        all_dm_users = []
        for name in dm_names:
          with open(os.path.join(self._PATH, 'direct_messages', name + '.json')) as f:
            channel_info = json.load(f)['channel_info']
            members = [self.__USER_DATA[m] for m in channel_info["members"]]
            all_dm_users.append({'id': name, 'users': members})
        return all_dm_users

        #dm_data = self._read_from_json("dms.json")
        #dms = dm_data.values()
        #all_dms_users = []

        #for dm in dms:
        #    # checks if messages actually exsist
        #    if dm["id"] not in self._EMPTY_DMS:
        #        dm_members = {"id": dm["id"], "users": [self.__USER_DATA[m] for m in dm["members"]]}
        #        all_dms_users.append(dm_members)

        #return all_dms_users


    def compile_mpim_messages(self):
        mpim_names = os.listdir(os.path.join(self._PATH, 'private_channels'))
        mpim_names = [x for x in mpim_names if x.startswith('mpdm-')]
        mpim_names = [os.path.splitext(x)[0] for x in mpim_names]

        #mpim_data = self._read_from_json("mpims.json")
        #mpim_names = [c["name"] for c in mpim_data.values()]

        return self._create_messages('private_channels', mpim_names, None) #mpim_data)

    def compile_mpim_users(self):
        """
        Gets the info for the members within the multiple person instant message

        Returns a list of all dms with the members that have ever existed

        :rtype: [object]
        {
            name: <name>
            users: [<user_id>]
        }

        """
        mpim_names = os.listdir(os.path.join(self._PATH, 'private_channels'))
        mpim_names = [x for x in mpim_names if x.startswith('mpdm-')]
        mpim_names = [os.path.splitext(x)[0] for x in mpim_names]
        all_mpim_users = []
        for name in mpim_names:
          with open(os.path.join(self._PATH, 'private_channels', name + '.json')) as f:
            channel_info = json.load(f)['channel_info']
            all_mpim_users.append({'name': channel_info['name'], 'users': [self.__USER_DATA[m] for m in channel_info["members"]]})

        #mpim_data = self._read_from_json("mpims.json")
        #mpims = [c for c in mpim_data.values()]
        #all_mpim_users = []

        #for mpim in mpims:
        #    mpim_members = {"name": mpim["name"], "users": [self.__USER_DATA[m] for m in mpim["members"]]}
        #    all_mpim_users.append(mpim_members)

        return all_mpim_users


    ###################
    # Private Methods #
    ###################

    def _create_messages(self, dir, names, data, isDms=False):
        """
        Creates object of arrays of messages from each json file specified by the names or ids

        :param [str] names: names of each group of messages

        :param [object] data: array of objects detailing where to get the messages from in
        the directory structure

        :param bool isDms: boolean value used to tell if the data is dm data so the function can
        collect the empty dm directories and store them in memory only

        :return: object of arrays of messages

        :rtype: object
        """

        chats = {}
        empty_dms = []

        for name in names:

            # gets path to dm directory that holds the json archive
            #dir_path = os.path.join(self._PATH, name)
            messages = []
            # array of all days archived
            day_files = [name] #glob.glob(os.path.join(dir_path, "*.json"))

            # this is where it's skipping the empty directories
            if not day_files:
                if isDms:
                    empty_dms.append(name)
                continue

            for day in sorted(day_files):
                with io.open(os.path.join(self._PATH, dir, day + '.json')) as f: #, encoding="utf8") as f:
                    # loads all messages
                    day_messages = json.load(f)
                    messages.extend([Message(self.__USER_DATA, data, d) for d in day_messages['messages']])

            chats[name] = messages

        if isDms:
            self._EMPTY_DMS = empty_dms

        return chats

    def _read_from_json(self, file):
        """
        Reads the file specified from json and creates an object based on the id of each element

        :param str file: Path to file of json to read

        :return: object of data read from json file

        :rtype: object
        """

        try:
            with io.open(os.path.join(self._PATH, file), encoding="utf8") as f:
                return {u["id"]: u for u in json.load(f)}
        except IOError:
            return {}
