import dicom
from dicom.errors import InvalidDicomError
import numpy as np
from PIL import Image, ImageDraw

def parse_dicom_file(filename):
    """Parse the given DICOM filename

    :param filename: filepath to the DICOM file to parse
    :return: dictionary with DICOM image data
    """

    try:
        # extract pixel array
        dcm = dicom.read_file(filename)
        dcm_image = dcm.pixel_array

        # linear transformation from disk to memory representation
        # do only if rescale and slope is not 0 else leave disk
        try:
            intercept = dcm.RescaleIntercept
        except AttributeError:
            intercept = 0.0
        try:
            slope = dcm.RescaleSlope
        except AttributeError:
            slope = 0.0
        if intercept != 0.0 and slope != 0.0:
            dcm_image = dcm_image * slope + intercept

        # store in dict
        # dcm_dict = {'pixel_data' : dcm_image}
        # return dcm_dict

        # CHANGE IN CODE
        # we are returning only pixel array
        # we don't need to create a dict for that
        return dcm_image

    except InvalidDicomError:
        return None


def parse_contour_file(filename):
    """Parse the given contour filename

    :param filename: filepath to the contourfile to parse
    :return: list of tuples holding x, y coordinates of the contour
    """

    coords_lst = []
    with open(filename, 'r') as infile:
        for line in infile:
            coords = line.strip().split()

            x_coord = float(coords[0])
            y_coord = float(coords[1])
            coords_lst.append((x_coord, y_coord))
    return coords_lst


def poly_to_mask(polygon, width, height):
    """Convert polygon to mask

    :param polygon: list of pairs of x, y coords [(x1, y1), (x2, y2), ...]
     in units of pixels
    :param width: scalar image width
    :param height: scalar image height
    :return: Boolean mask of shape (height, width)
    """

    # https://stackoverflow.com/questions/3654289/scipy-create-2d-polygon-mask/3732128#3732128
    img = Image.new(mode='L', size=(width, height), color=0)
    ImageDraw.Draw(img).polygon(xy=polygon, outline=0, fill=1)
    mask = np.array(img).astype(bool)
    return mask


def get_patient_files(patient_dicom_id, patient_contour_id,
                      dicoms_path, contourfiles_path, verbose=True):
    """
    Get all dicom, i_contour and o_contour filenames of a given paient.

    Inputs:
        patient_dicom_id (pathlib.PosixPath): directory name for dicom files
        patient_contour_id (pathlib.PosixPath): directory name for contours
        dicoms_path (pathlib.PosixPath): main directory path for dicoms
        contours_path (pathlib.PosixPath): main directory path for contours
    Return:
        dicoms_valid (list): list of dicom image file paths
        i_contours_valid (list): list of i_contours file paths
        o_contours_valid (list): list of o_contours file paths
    """
    # extract all pathlib objects in directories
    dicoms = list((dicoms_path / patient_dicom_id).iterdir())
    i_contours = list((contourfiles_path / patient_contour_id / 'i-contours').iterdir())
    o_contours = list((contourfiles_path / patient_contour_id / 'o-contours').iterdir())

    # extract non-dot files as valid files
    dicoms_valid = [str(o) for o in dicoms if o.name[0] != '.']
    i_contours_valid = [str(o) for o in i_contours if o.name[0] != '.']
    o_contours_valid = [str(o) for o in o_contours if o.name[0] != '.']

    if verbose:
        print(f"# of dicoms : {len(dicoms)}, i_contours : {len(i_contours)}, o_contours : {len(o_contours)}")
        print(f"# of valid dicoms : {len(dicoms_valid)}, i_contours : {len(i_contours_valid)}, \
o_contours : {len(o_contours_valid)}")

    return (dicoms_valid, i_contours_valid, o_contours_valid)


def dicom_slice_dict(dicoms):
    """
    Creates ordered slice dict from a list of dicom filenames
    Input:
        dicoms (list): valid dicom files of a patient
    Return:
        dicoms_dict (dict): ordered dict by slice order
    """
    dicoms_dict = {}
    for dicom_fn in dicoms:
        slice_no = int(dicom_fn.split('/')[-1].split('.')[0])
        dicoms_dict[slice_no] = dicom_fn
    return dicoms_dict


def contour_slice_dict(contours):
    """
    Creates ordered slice dict from list of contour files
    Input:
        contours (list): valid contour files of a patient
    Return:
        contours_dict (dict): ordered dict by slice order
    """
    contours_dict = {}
    for contour_fn in contours:
        slice_no = int(contour_fn.split('/')[-1].split('-')[2])
        contours_dict[slice_no] = contour_fn
    return contours_dict


def patient_files_dict(dicoms_dict, i_contours_dict, o_contours_dict):
    """
    Create ordered slice dict from dicoms_dict, i_contours_dict, o_contours_dict
    Inputs:
        dicoms_dict (dict): ordered dict of dicom files
        i_contours_dict (dict): ordered dict of i_contour files
        o_contours_dict (dict): ordered dict of o_contour files
    Return:
        patient_files_dict (dict): ordered dict with same size as original dicom images containing
        list for [dicom file path, i_contour file path, o_contour file path]
    """
    patient_files_dict = {}
    for slice_no in dicoms_dict:
        dicom_fname = dicoms_dict.get(slice_no)
        i_contour_fname = i_contours_dict.get(slice_no)
        o_contour_fname = o_contours_dict.get(slice_no)
        patient_files_dict[slice_no] = {'dicom_fname': dicom_fname,
                                        'i_contour_fname': i_contour_fname,
                                        'o_contour_fname': o_contour_fname}
    return patient_files_dict


class Patient:
    def __init__(self, dicom_id, contour_id, dicoms_path, contourfiles_path):
        """
        Class object for patients

        dicom_id (str): patient directory name under a dir like "dicoms/"
        contour_id (str): patient directory name under dir like "contourfiles/"
        dicoms_path (pathlib.PosixPath): pathlib object for dicoms parent dir
        contourfiles_path (pathlib.PosixPath): pathlib object for contourfiles parent dir
        """

        self.dicom_id = dicom_id
        self.contour_id = contour_id
        self.dicoms_path = dicoms_path
        self.contourfiles_path = contourfiles_path

    def create_file_lists(self, verbose=True):
        """
        Creates lists for dicom, i_contour and o_contour files
        """
        self.dicoms, self.i_contours, self.o_contours = get_patient_files(self.dicom_id, self.contour_id,
                                                                          self.dicoms_path, self.contourfiles_path,
                                                                          verbose)

    def create_file_dicts(self, verbose=True):
        """
        Create ordered dicts for dicoms, i_contours, o_contours filenames and all files combined
        """
        if not hasattr(self, 'dicoms'):
            self.create_file_lists(verbose)

        # pdb.set_trace()

        self.dicoms_dict = dicom_slice_dict(self.dicoms)
        self.i_contours_dict = contour_slice_dict(self.i_contours)
        self.o_contours_dict = contour_slice_dict(self.o_contours)
        self.all_files_dict = patient_files_dict(self.dicoms_dict, self.i_contours_dict, self.o_contours_dict)

    def create_numpy_arrays(self, verbose=True):
        """
        Create ordered dict of dicts having np.array for dicom, i_contour and o_contour
        """
        if not hasattr(self, 'all_files_dict'):
            self.create_file_dicts(verbose)

        self.all_numpy_dict = {}
        for slice_no in self.all_files_dict:

            dicom_fn = self.all_files_dict[slice_no]['dicom_fname']
            i_contour_fn = self.all_files_dict[slice_no]['i_contour_fname']
            o_contour_fn = self.all_files_dict[slice_no]['o_contour_fname']

            # parse dicom
            if dicom_fn is not None:
                img_array = parse_dicom_file(dicom_fn)
            else:
                img_array = None

            if img_array is not None:
                # get image size
                H, W = img_array.shape

                # parse i_contour
                if i_contour_fn is not None:
                    i_contour_array = poly_to_mask(parse_contour_file(i_contour_fn)
                                                   , W, H).astype(np.uint8)
                else:
                    i_contour_array = None

                # parse o_contour
                if o_contour_fn is not None:
                    o_contour_array = poly_to_mask(parse_contour_file(o_contour_fn)
                                                   , W, H).astype(np.uint8)
                else:
                    o_contour_array = None
            else:
                img_array, i_contour_array, o_contour_array = None, None, None

            self.all_numpy_dict[slice_no] = {'dicom_array': img_array,
                                             'i_contour_array': i_contour_array,
                                             'o_contour_array': o_contour_array}
