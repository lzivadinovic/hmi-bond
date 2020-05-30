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
        name : str
            The name of the animal
        num_legs : int, optional
            The number of legs the animal (default is 4)
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
        '''
        NOAANUM = str(NOAANUM)
        ins = [index for index, string in enumerate(self.content) if NOAANUM in string]
        harpnum = [ self.content[x].split(' ')[0] for x in ins ]
        if len(harpnum) != 1:
            raise Exception("Be careful! Your region is over multiple HARPs or it was not found! HARPS: {}".format(harpnum))
        return int(harpnum[0])