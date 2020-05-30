#Ok, i dont know how to work with class factories so i cant extend this
class process_continuum():
    """
    A class used to represent an process_continuum object.
    We use this object to automate continuum images processing
    
    #### WE ARE NOT LOADING ALL FILES INTO THIS OBJECT, WE ARE GOING ONE BY ONE!!!! ####

    ...

    Attributes
    ----------
    inpath : str
        Path to fits file that we need to process
    
    opath : str
        Path where corrected fits should be saved

    Methods
    -------
    __limb_dark()
        limbdarkening coeeficients
    
    _correct_for_limb()
        Function used to correct for limb darkening
        
    _normalize():
        Function used to normalize data
        
        
        
    master_wrap
    """
    
    def __init__(self, inpath, overwrite=False):
        self.inpath = inpath
        self.overwrite = overwrite
        # check if input is list
        if isinstance(self.inpath, list):
            print("Dataset detected!")
            #self.outpath = os.path.dirname(self.inpath.replace('raw','processed'))
            #print("Files will be saved to: {}".format(self.outpath_dir)) 
            #Path(os.path.dirname(self.inpath.replace('raw','processed'))).mkdir(parents=True, exist_ok=True)
            print("Processing ...")
            for in_img in self.inpath:
                Path(os.path.dirname(in_img.replace('raw','processed'))).mkdir(parents=True, exist_ok=True)
                out = self._master_wrap(in_img)
                out.save(in_img.replace('raw','processed'))
            print("Processing done.")
        elif isinstance(self.inpath, str):
            print("Single file detected!")
            print("Processing ...")
            out = self._master_wrap(self.inpath)
            print("Processing done.")
            self.outpath = self.inpath.replace('raw','processed')
            print("File will be saved to: {}".format(self.outpath)) 
            Path(os.path.dirname(self.outpath)).mkdir(parents=True, exist_ok=True)
            out.save(self.outpath)
            print("File saved!")
        else:
            raise ValueError("I cant understand input, should be string or list of strings")
            
        
    
    def __limb_dark(self, r, koef=np.array([0.32519, 1.26432, -1.44591, 1.55723, -0.87415, 0.173333])):
        """
        This function takes r as distance from sun center in units of sun radii and return division factor for correction.
        We are making it internal function, because we only need to call it from correct_for_limb function.
        """
        # r is normalized distance from center [0,1]
        if len(koef) != 6:
            raise ValueErrror("koef len should be exactly 6")
        if np.max(r) > 1 or np.min(r) < 0:
            raise ValueError("r should be in [0,1] range")
        mu = np.sqrt(1-r**2)  # mu = cos(theta)
        return koef[0]+koef[1]*mu+koef[2]*mu**2+koef[3]*mu**3+koef[4]*mu**4+koef[5]*mu**5

    def _correct_for_limb(self, sunpy_map):
        """
        This function takes sunpy map and removes limb darkening from it
        It transfer coordinate mesh to helioprojective coordinate (using data from header)
        Calucalates distance from sun center in units of sun radii at the time of observation
        Uses limb_dark function with given coeffitiens and divides by that value

        Input: sunpy_map (sunpy.map) - input data
        Returns: sunpy.map - output data object
        """
        helioproj_limb = sunpy.map.all_coordinates_from_map(sunpy_map).transform_to(
            frames.Helioprojective(observer=sunpy_map.observer_coordinate))
        rsun_hp_limb = sunpy_map.rsun_obs.value
        distance_from_limb = np.sqrt(
            helioproj_limb.Tx.value**2+helioproj_limb.Ty.value**2)/rsun_hp_limb
        limb_cor_data = sunpy_map.data / self.__limb_dark(distance_from_limb)
        return sunpy.map.Map(limb_cor_data, sunpy_map.meta)

    # AVERAGE
    def _normalize(self, sunpy_map, header_keyword='AVG_F_NO', NBINS=100):
        '''
        This function normalizes sunpy map
        It first creates histogram of data
        Finds maximum of histogram and divide whole dataset with that number
        This is efectevly normalization to quiet sun

        input:  sunpy_map (sunpy.map) - input data
                header_keyword (string) - name of header keyword in which maximum of histogram will be written to 
                                          This allows users to later on, revert to unnormalized image, default is AVG_F_NO
                NBINS (int) - How many bins you want for your histogram, default is 100
        output: sunpy.map - output data object
        '''
        weights, bin_edges = np.histogram(
            sunpy_map.data.flatten(), bins=NBINS, density=True)
        # MAGIC I SAY!
        # find maximum of histogram
        k = (weights == np.max(weights)).nonzero()[0][0]
        # find flux value for maximum of histogram
        I_avg = (bin_edges[k+1]+bin_edges[k])/2
        # update data
        I_new = sunpy_map.data/I_avg
        # create new keyword in header
        # AVG_F_ON
        # AVG_F_EN
        sunpy_map.meta[header_keyword] = I_avg
        # create new map
        return sunpy.map.Map(I_new, sunpy_map.meta)

    def _master_wrap(self,fname):
        '''
        This function is just simple wrapper for all provided functions

        input: filename (string) -  fits file path that correction shoud be performed on
        output: ofile (string) - string with path to new file
        '''
        # load data
        sunpy_data = sunpy.map.Map(fname)
        # correct map for limb
        mid_data = self._correct_for_limb(sunpy_data)
        # Normalize
        mid_data = self._normalize(mid_data, header_keyword='AVG_F_ON')
        return mid_data
        #mid_data.peek()
        # enhance
        #mid_data = enhance_wrapper(mid_data)
        # normalize again, enhance can make mess with flux
        #mid_data = normalize(mid_data, header_keyword='AVG_F_EN')
        # Create new filename
        
        #Create new logic for saving files
#         outfile = os.path.basename(filename).replace(
#             search_criterium, search_criterium+sufix)
#         ofile = os.path.join(output_dir, outfile)
        # save map
        #mid_data.save(ofile)
        #return ofile





#     def enhance_wrapper(sunpy_map, depth=5, model="keepsize", activation="relu", ntype="intensity"):
#         '''
#         This procedures run enhance https://github.com/cdiazbas/enhance (it works only from my fork https://github.com/lzivadinovic/enhance)
#         on input sunpy map
#         Check source code for explanation of code and input parameters

#         input: sunpy_map (sunpy.map) - input data set
#         output: sunpy.map - output data object (enhanced)
#         '''
#         # if rtype is spmap, there is no need for output, it will return sunpy.map object (lzivadinovic/enhance fork - master branch)
#         out = enhance(inputFile=sunpy_map, depth=depth, model=model,
#                       activation=activation, ntype=ntype, output='1.fits', rtype='spmap')
#         out.define_network()
#         return out.predict()