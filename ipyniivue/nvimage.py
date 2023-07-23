import enum

class NVIMAGE_TYPE(int, enum.Enum):
    UNKNOWN = 0
    NII = 1
    DCM = 2
    DCM_MANIFEST = 3
    MIH = 4
    MIF = 5
    NHDR = 6
    NRRD = 7
    MHD = 8
    MHA = 9
    MGH = 10
    MGZ = 11
    V = 12
    V16 = 13
    VMR = 14
    HEAD = 15
    DCM_FOLDER = 16

class NVImage:
    def __init__(self, input_dict={}, **kwargs):
        kwargs.update(input_dict)
        self.data_buffer = kwargs.get("data_buffer", b"") # isnt dataBuffer required?
        self.name = kwargs.get("name", "")
        self.colormap = kwargs.get("colormap", "gray")
        self.opacity = kwargs.get("opacity", 1.0)
        self.paired_img_data = kwargs.get("paired_img_data", None)
        self.cal_min = kwargs.get("cal_min", float("nan"))
        self.cal_max = kwargs.get("cal_max", float("nan"))
        self.trust_cal_min_max = kwargs.get("trust_cal_min_max", True)
        self.percentile_frac = kwargs.get("percentile_frac", 0.02)
        self.ignore_zero_voxels = kwargs.get("ignore_zero_voxels", False)
        self.visible = kwargs.get("visible", True)
        self.use_qform_not_sform = kwargs.get("use_qform_not_sform", False)
        self.colormap_negative = kwargs.get("colormap_negative", "")
        self.frame_4d = kwargs.get("frame_4d", 0)
        self.image_type = kwargs.get("image_type", NVIMAGE_TYPE.UNKNOWN)
        self.cal_min_neg = kwargs.get("cal_min_neg", float("nan"))
        self.cal_max_neg = kwargs.get("cal_max_neg", float("nan"))
        self.colorbar_visible = kwargs.get("colorbar_visible", True)
        self.colormap_label = kwargs.get("colormap_label", [])

        self.id = kwargs.get("id", "")
    
    def __iter__(self):
        yield 'dataBuffer', self.data_buffer
        yield 'name', self.name
        yield 'colormap', self.colormap
        yield 'opacity', self.opacity
        yield 'pairedImgData', self.paired_img_data
        yield 'cal_min', self.cal_min
        yield 'cal_max', self.cal_max
        yield 'trustCalMinMax', self.trust_cal_min_max
        yield 'percentileFrac', self.percentile_frac
        yield 'ignoreZeroVoxels', self.ignore_zero_voxels
        yield 'visible', self.visible
        yield 'useQFormNotSForm', self.use_qform_not_sform
        yield 'colormapNegative', self.colormap_negative
        yield 'frame4D', self.frame_4d
        yield 'imageType', int(self.image_type)
        yield 'cal_minNeg', self.cal_min_neg
        yield 'cal_maxNeg', self.cal_max_neg
        yield 'colorbarVisible', self.colorbar_visible
        yield 'colormapLabel', self.colormap_label

    def clone(self):
        #to be implemented
        pass