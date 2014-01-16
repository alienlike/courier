import os
import string
from pkg_resources import resource_filename

datadir = resource_filename(__name__, '.data')

class FileSystemIO:

    # generate the absolute and relative paths for a message element
    def get_path(self, msg_elem_id):

        # convert id to a 20-character string padded with zeros
        msg_elem_id = '%020d' % msg_elem_id

        # split the string into 4-char chunks
        split_len = lambda str, length: [str[i:i+length] for i in range(0, len(str), length)]
        path_elems = split_len(msg_elem_id, 4)

        # convert the chunks into a relative path
        relpath = os.path.join(*path_elems)

        # convert the relative path to an absolute path
        abspath = os.path.join(datadir, relpath)

        # blaze a trail to the relative path
        reldir = relpath[:-1]
        self._blaze_trail(reldir)

        return abspath, relpath

    def get_abspath(self, relpath):
        abspath = os.path.join(datadir, relpath)
        return abspath

    def _blaze_trail(self, relpath):
        # make sure that the datadir exists
        if not os.path.exists(datadir):
            os.mkdir(datadir)
        # make sure that each subfolder exists within datadir
        currbase = datadir
        for dir in string.split(relpath, os.path.sep):
            currbase = os.path.join(currbase, dir)
            if not os.path.exists(currbase):
                os.mkdir(currbase)