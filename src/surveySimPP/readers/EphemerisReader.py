import abc

class EphemerisReader(abc.ABC):
    """The base class for reading in the ephemerides from
    different simulators or in different storage formats.
    """

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def read_rows(self, begin_loc=0, chunk_size=None):
        """Reads in a set number of rows from the input file.

        Parameters:
        -----------
        begin_loc (int, optional): location in file where reading begins. This is the
           number of the line after the header, so 0 would be the first line of data
           [Default = 0].

        chunk_size (int, optional): length of chunk to be read in. Use None to read
            the entire file. [Default = None]

        Returns:
        -----------
        res_df (Pandas dataframe): dataframe of the auxilary data.

        """
        pass

    @abc.abstractmethod
    def read_objects(self, obj_ids=None):
        """Read in a chunk of data for given object IDs.

        Parameters:
        -----------
        obj_ids (list, optional): A list of object IDs to use. If set to None
            Then will load all objects in the file.

        Returns:
        -----------
        res_df (Pandas dataframe): The dataframe for the ephemerides.
        """
        pass
