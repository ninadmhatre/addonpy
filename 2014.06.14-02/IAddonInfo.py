__author__ = 'Ninad'


class IAddonInfo(object):
    def __init__(self, *args):
        pass

    def print_addon_info(self):
        print(("""
        Name               : {0}
        Description        : {1}
        Version            : {2}
        Type               : {3}
        Type Description   : {4}
        Execution Sequence : {5}
        Stop Sequence      : {6}
        UUID               : {7}

        Author             : {8}
        Help Link          : {9}
        """).format(
            self.get_name(),
            self.get_desc(),
            self.get_version(),
            self.get_type(),
            self.get_type_desc(),
            self.get_start_seq(),
            self.get_stop_seq(),
            self.get_uuid(),
            self.get_author(),
            self.get_help_url()
        ))

    def get_uuid(self):
        return self.__get('uuid')

    def get_version(self):
        return self.__get('version')

    def get_name(self):
        return self.__addon__()

    def get_desc(self):
        return self.__get('description')

    def get_type(self):
        return self.__get('type')

    def get_type_desc(self):
        return AddonType.get_type_desc(self.get_type())

    def get_start_seq(self):
        return self.__get('execution_seq')

    def get_stop_seq(self):
        return self.__get('stop_seq')

    def get_author(self):
        return self.__get('author')

    def get_help_url(self):
        return self.__get('help_url')

    def __get(self, field):
        return self.__info__().get(field)


class AddonType(object):
    @staticmethod
    def get_type_desc(addon_type):
        try:
            type_int = int(addon_type)
        except ValueError as why:
            print("Error: Please provide type as int! More info: " + str(why.message))
            return "Invalid"

        type_desc = 'Unknown'
        if type_int == 1:
            type_desc = 'Addon'
        elif type_int == 2:
            type_desc = 'AddonOverload'
        elif type_int == 0:
            type_desc = 'CoreAddon'

        return type_desc
