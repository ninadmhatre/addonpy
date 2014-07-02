__author__ = 'Ninad'

from collections import namedtuple


class IAddonInfo(object):
    """
    Base class for all addons, this provides basic meta information retrieval and may be extended to provide some
    common functionality for all addons
    """
    __t = namedtuple('AddonInfo', 'name, version, type, uuid, type_desc')

    def __init__(self):
        """
        Not used!
        :return: void
        """
        pass

    def get_addon_info(self):
        """
        get addon information in form of dict, for searching purpose
        :return: addon information as dict()
        :rtype: dict
        """
        return self.__t(
            name=self.get_name(),
            type=self.get_type(),
            type_desc=self.get_type_desc(),
            uuid=self.get_uuid(),
            version=self.get_version()
        )._asdict()

    def print_addon_info(self):
        """
        Used to print all the meta information about addon loaded (just for dumping all the info)
        :return: prints information about addon
        """
        print("""
        Name               : {0}
        Description        : {1}
        Version            : {2}
        Type               : {3}
        Execution Sequence : {4}
        Stop Sequence      : {5}
        UUID               : {6}
        Author             : {7}
        Help Link          : {8}
        """.format(
            self.get_name(),
            self.get_desc(),
            self.get_version(),
            self.get_type(),
            self.get_start_seq(),
            self.get_stop_seq(),
            self.get_uuid(),
            self.get_author(),
            self.get_help_url()
        ))

    def get_uuid(self):
        """
        UUID of addon from __info__()
        :return: UUID
        :rtype: str
        """
        return self._get('uuid')

    def get_version(self):
        """
        version of addon from __info__()
        :return: version
        :rtype: str
        """
        return self._get('version')

    def get_name(self):
        """
        name of addon from __info__()
        :return: addon name
        :rtype: str
        """
        return self.__addon__()

    def get_desc(self):
        """
        description of addon from __info__()
        :return: description
        :rtype: str
        """
        return self._get('description')

    def get_type(self):
        """
        type of addon from __info__()
        :return: addon type
        :rtype: str
        """
        return self._get('type')

    def get_start_seq(self):
        """
        Execution sequence of addon from __info__()
        :return: execution sequence
        :rtype: list
        """
        return self._get('execution_seq')

    def get_stop_seq(self):
        """
        Stop sequence of addon from __info__()
        :return: Stop sequence
        :rtype: list
        """
        return self._get('stop_seq')

    def get_author(self):
        """
        author of addon from __info__()
        :return: Author
        :rtype: str
        """
        return self._get('author')

    def get_help_url(self):
        """
        help link or addon home page of addon from __info__()
        :return: help link for addon
        :rtype: str
        """
        return self._get('help_url')

    def _get(self, field):
        """
        get value of field from addon from __info__()
        :return: value for field passed
        :rtype: str
        """
        return self.__info__.get(field)


# class AddonType(object):
#     """
#     Enum like functionality, which may be extended to add comparison
#     """
#
#     @staticmethod
#     def get_type_desc(addon_type):
#         """
#         type enum in class returns description of numeric type passed
#         :param addon_type: numeric type
#         :return: description of numeric type
#         :rtype: str
#         """
#         try:
#             type_int = int(addon_type)
#         except ValueError as why:
#             print("Error: Please provide type as int! More info: " + str(why.message))
#             return "Invalid"
#
#         type_desc = 'Unknown'
#         if type_int == 1:
#             type_desc = 'Addon'
#         elif type_int == 2:
#             type_desc = 'AddonOverload'
#         elif type_int == 0:
#             type_desc = 'CoreAddon'
#
#         return type_desc
