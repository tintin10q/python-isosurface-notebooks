import nibabel
from numpy import logical_and

def segment_labels(volume_file_path: str, label_file_path: str, minlabel: int = 0, maxlabel  = float("inf")) -> nibabel.Nifti1Image:
    """
    Segment bones from a ctscan volume. This function is tested with .nii.gz
    :param volume_file_path: the path to the volume file
    :param label_file_path: the path to the label file
    :param isovalue: the iso value
    :return: nibabel.Nifti1Image
    """
    if maxlabel is None:
        maxlabel = minlabel
    
    # Load the label and volume data
    volume = nibabel.load(volume_file_path).get_fdata()
    label_meta = nibabel.load(label_file_path)
    label_header = label_meta.header
    label = label_meta.get_fdata()

    if volume.shape != label.shape:
        raise ValueError('You tried to enter two files that are not the same size')

    label4 = label.copy()

    for z in range(label.shape[2]):
        ctscan = volume[:, :, z]
        label2 = label[:, :, z]
        label4[:, :, z] = logical_and(label2 > minlabel, label2 < maxlabel)

    new_image = nibabel.Nifti1Image(label4, affine=None, header=label_header)  

    return new_image
