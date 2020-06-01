import os
import requests
class noaa2harp():
    """
    A class used to represent an noaa2harp object

    ...

    Attributes
    ----------
    fsave : str
        Filename for base convertor txt

    Methods
    -------
    update_dataset()
        Fetch newest list from jsoc
        
    noaa2harp(NOAANUM)
        Returns HAPRNUM for given NOAA.
        Could be int or str
    """
    def __init__(self, fsave='./HARP_TO_NOAA.txt'):
        """
        Parameters
        ----------
        fsave : str
            Name of the file where dataset should be saved
        """
        self.fsave = fsave
        if not os.path.exists(self.fsave):
            print("Default HARP_TO_NOAA DOES NOT exists, fetching")
            self.update_dataset()
        else:
            print("Default HARP_TO_NOAA exists")
            print("Loading file")
            self._load_dataset()        
    
    def _load_dataset(self):
        """
        Load dataset into content variable
        """
        with open(self.fsave) as f:
            content = [line.rstrip() for line in f]
        self.content = content
    
    def update_dataset(self):
        """
        Wrapper method for download newest harpnum to noaa list
        """
        url = 'http://jsoc.stanford.edu/doc/data/hmi/harpnum_to_noaa/all_harps_with_noaa_ars.txt'
        r = requests.get(url)
        if r.ok:
            print("Content fetched, saving...")
            with open(self.fsave, 'wb') as f:
                f.write(r.content)
                print("File saved to {}".format(self.fsave))
            print("Loading new dataset")
            self._load_dataset()
            
    def noaa2harp(self, NOAANUM):
        '''
        This returns HARP number for provided NOAA region from content file
        
        Parameters
        ----------
        NOAANUM : int
            NOAANUM for which we need harp
        '''
        NOAANUM = str(NOAANUM)
        ins = [index for index, string in enumerate(self.content) if NOAANUM in string]
        harpnum = [ self.content[x].split(' ')[0] for x in ins ]
        if len(harpnum) != 1:
            raise Exception("Be careful! Your region is over multiple HARPs or it was not found! HARPS: {}".format(harpnum))
        return int(harpnum[0])
    
    def harp2noaa(self, HARPNUM):
        '''
        This returns NOAA number for provided HARP region from content file
        
        Parameters
        ----------
        HARPNUM : int
            HARPNUM for which we need NOAANUM
        '''
        HARPNUM = str(HARPNUM)
        ins = [index for index, string in enumerate(self.content) if HARPNUM in string]
        noaanum = [ self.content[x].split(' ')[1] for x in ins ]
        if len(noaanum) != 1:
            raise Exception("Be careful! Your HARP region is covered via multiple NOAA regions or it was not found! NOAA: {}".format(harpnum))
        return int(noaanum[0])