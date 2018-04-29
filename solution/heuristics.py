import cv2
import numpy as np
from skimage import filters

# define kernel types
KERNEL_TYPE = [
    cv2.MORPH_RECT,
    cv2.MORPH_ELLIPSE,
    cv2.MORPH_CROSS,
]


def i_contour_from_o_contour(dicom_array, o_contour_array, threshold="auto",
                             kernel_type=0, kernel_sz=3):
    """
    Generate i-contour given a o-contour array
    by employing thresholding and morphological
    operations. Applies closing -> opening -> final proposal

    Inputs:
        dicom_array (np.array): Raw DICOM image

        o_contour_array (np.array): Boolean mask array
            for o-contour

        threshold (int, ): threshold for i-contour
            extraction.
            if "auto", threshold will be estimated by OTSU
            https://en.wikipedia.org/wiki/Otsu%27s_method

        kernel_type (int, list): 0: cv2.MORPH_RECT
                                 1: cv2.MORPH_ELLIPSE
                                 2: cv2.MORPH_CROSS
            If list, it must have 2 elements:
            one for opening, one for closing.

        kernel_size (int, list): kernel size for operations
            If list, it must have 2 elements:
            one for opening, one for closing
    Return:
        i_contour_proposal (np.array): Proposed boolean
        mask array for i-contour
    """
    # pdb.set_trace()

    if isinstance(kernel_type, list) & isinstance(kernel_sz, list):
        kernel_type1, kernel_type2 = kernel_type
        kernel_sz1, kernel_sz2 = kernel_sz

    elif isinstance(kernel_type, int) & isinstance(kernel_sz, int):
        kernel_type1, kernel_type2 = kernel_type, kernel_type
        kernel_sz1, kernel_sz2 = kernel_sz, kernel_sz
    else:
        raise Exception('kernel_type and kernel_sz must be both int or list')

    # generate proposal
    roi_array = dicom_array * o_contour_array
    if threshold == "auto":
        threshold = filters.threshold_otsu(roi_array[roi_array != 0])
    roi_i_contour_proposal = (roi_array > threshold).astype(np.uint8)

    # apply closing
    kernel = cv2.getStructuringElement(KERNEL_TYPE[kernel_type1],
                                       (kernel_sz1, kernel_sz1))
    roi_i_contour_proposal = cv2.morphologyEx(roi_i_contour_proposal,
                                              cv2.MORPH_CLOSE, kernel)
    # apply opening
    kernel = cv2.getStructuringElement(KERNEL_TYPE[kernel_type2],
                                       (kernel_sz2, kernel_sz2))
    roi_i_contour_proposal = cv2.morphologyEx(roi_i_contour_proposal,
                                              cv2.MORPH_OPEN, kernel)

    return roi_i_contour_proposal


def extract_all_mask_slices(patient):
    """
    For a given patient object exrtact slice idx
    list where all arrays are present, both
    for i_contour_array and o_contour_array

    Inputs:
        patient (Patient object): patient object
    """
    # generate numpy arrays for the patient
    if not hasattr(patient, "all_numpy_dict"):
        patient.create_numpy_arrays(False)

    contour_slices = []
    for slice_no in patient.all_numpy_dict:
        slice_dict = patient.all_numpy_dict[slice_no]
        if (slice_dict['o_contour_array'] is not None) & (slice_dict['i_contour_array'] is not None):
            contour_slices.append(slice_no)
    return contour_slices

def extract_patient_arrays(patient, slice_idx):
    """
    Extract dicom_array, i_contour_array, o_contour_array
    from patient all_numpy_dict

    Inputs:
        patient (Patient object): patient object
        slice_idx (int): slice index for array extraction
    """
    dicom_array = patient.all_numpy_dict[slice_idx]['dicom_array']
    i_contour_array = patient.all_numpy_dict[slice_idx]['i_contour_array']
    o_contour_array = patient.all_numpy_dict[slice_idx]['o_contour_array']
    return dicom_array, i_contour_array, o_contour_array









