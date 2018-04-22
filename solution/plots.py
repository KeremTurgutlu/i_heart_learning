import os
import matplotlib.pyplot as plt
import numpy as np


def show_img_msk_fromarray(img_arr, msk_arr, alpha=0.35, sz=7, cmap='inferno',
                           save_path=None):

    """
    Show original image and masked on top of image
    next to each other in desired size

    Inputs:
        img_arr (np.array): array of the image
        msk_arr (np.array): array of the mask
        alpha (float): a number between 0 and 1 for mask transparency
        sz (int): figure size for display
        save_path (str): path to save the figure
    """

    msk_arr = np.ma.masked_where(msk_arr == 0, msk_arr)
    plt.figure(figsize=(sz, sz))
    plt.subplot(1, 2, 1)
    plt.imshow(img_arr)
    plt.imshow(msk_arr, cmap=cmap, alpha=alpha)
    plt.subplot(1, 2, 2)
    plt.imshow(img_arr)
    if save_path is None:
        plt.show()
    else:
        plt.savefig(save_path)
        plt.close()


def save_images(all_patients, contour_type='i_contour',
                main_dir='final_data/images/'):
    """
    Save dicom images and images with masks on top of the corresponding images.
    All files will will be saved under main_dir by creating a new folder
    for contour type and then by creating a folder for each patient separately.

    Inputs:
        all_patients (list): list of Patient objects
        contour_type (str): either "i_contour" or "o_contour"
    """

    # create folder for contour_type
    dirname = main_dir + f'{contour_type}/'
    os.makedirs(dirname, exist_ok=True)

    for patient in all_patients:
        # create patient folders for saving
        dirname = main_dir + f'{contour_type}/{patient.dicom_id}/'
        os.makedirs(dirname, exist_ok=True)

        # create numpy arrays for the patient
        patient.create_numpy_arrays()

        # loop over slices in numpy array dict
        for slice_no in patient.all_numpy_dict:
            slice_dict = patient.all_numpy_dict[slice_no]

            # only show image for given contour type
            if slice_dict[f'{contour_type}_array'] is not None:

                img_array = slice_dict['dicom_array']
                msk_array = slice_dict[f'{contour_type}_array']

                show_img_msk_fromarray(img_array,
                                       msk_array,
                                       cmap='Wistia',
                                       sz=10, alpha=0.7,
                                       save_path=dirname +f'slice_{slice_no}.png')