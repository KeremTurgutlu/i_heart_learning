import numpy as np
from torch.utils.data import *
from torch import FloatTensor as FT
from .dicom_utils import parse_dicom_file, poly_to_mask, parse_contour_file

class HeartDataset2D(Dataset):
    """
    Create 2D dataset from given list of Patients

    Inputs:
        all_patients (list): list containing Patient objects
        contour_type (str): either 'i_contour' or 'o_contour'
    """
    def __init__(self, all_patients, contour_type):

        self.all_patients = all_patients
        self.contour_type = contour_type
        # self.model_type = model_type

        # get filenames
        self.dicom_contour_fnames = []
        for patient in self.all_patients:
            # create all files dict
            patient.create_file_dicts(False)
            # loop over slices
            for slice_no in patient.all_files_dict:
                slice_dict = patient.all_files_dict[slice_no]
                dicom_fname = slice_dict['dicom_fname']
                contour_fname = slice_dict[f'{self.contour_type}_fname']
                if contour_fname is not None:
                    self.dicom_contour_fnames.append((dicom_fname, contour_fname))

    def __getitem__(self, idx):
        # get filename pair by idx
        dicom_contour_fname = self.dicom_contour_fnames[idx]
        dicom_fname, contour_fname = dicom_contour_fname[0], dicom_contour_fname[1]

        #
        img = parse_dicom_file(dicom_fname)
        H, W = img.shape
        msk = poly_to_mask(parse_contour_file(contour_fname), W, H).astype(np.uint8)

        return FT(img)[None, :], FT(msk)[None, :] # convert to FloatTensor and add channel (1)

    def __len__(self):
        return len(self.dicom_contour_fnames)