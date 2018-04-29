import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from .heuristics import extract_patient_arrays


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


def show_all_masks(dicom_array, i_contour_array, o_contour_array):
    sz = 30
    cmap="Wistia"
    alpha=0.5
    plt.figure(figsize=(sz, sz))

    # raw image
    plt.subplot(1, 3, 1)
    plt.imshow(dicom_array)

    # i-contour
    plt.subplot(1, 3, 2)
    plt.imshow(dicom_array)
    mask_arr = np.ma.masked_where(i_contour_array == 0, i_contour_array)
    plt.imshow(mask_arr, cmap=cmap, alpha=alpha)

    # o-contour
    plt.subplot(1, 3, 3)
    plt.imshow(dicom_array)
    mask_arr = np.ma.masked_where(o_contour_array == 0, o_contour_array)
    plt.imshow(mask_arr, cmap=cmap, alpha=alpha)

def plot_roi_densities(patient, slice_idxs, patient_idx=0, save_path=None):
    """
    Plot or save ROI intensity distributions bounded
    by o-contour masks.

    Inputs:
        patient (Patient): patient object
        slice_idxs (list): list of indexes for roi slices
        patient_idx (int, str): patient index or name for title and filename
        save_path (str): file destination for saving the figure
    """
    # set subplots and title
    fig, axes = plt.subplots(nrows=len(slice_idxs) // 3 +\
                                   len(slice_idxs) % 3, ncols=3, figsize=(15, 10))
    fig.suptitle(f'Patient {patient_idx}', fontsize=20)
    # plot for all given slices
    for i, (ax, slice_idx) in enumerate(zip(axes.flat, slice_idxs)):
        # extract numpy arrays for given slices
        dicom_array, i_contour_array, o_contour_array =\
            extract_patient_arrays(patient, slice_idx)
        # get roi by bounding the raw image with o-contour
        roi_array = (dicom_array * o_contour_array).astype('int32')
        ax.set_title(f'ROI slice {slice_idx}')
        ax.set_xlabel('pixel intensity')
        # filter for roi and plot density
        sns.distplot(roi_array.flatten()[roi_array.flatten() > 0], bins=50, ax=ax)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    if save_path is None:
        fig.show()
    else:
        plt.savefig(save_path)
        plt.close()