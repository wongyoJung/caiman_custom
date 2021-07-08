from read_roi import read_roi_file
from read_roi import read_roi_zip

ex = "D:/twophoton/test/test.roi"
rois = read_roi_file(ex)
print(rois)