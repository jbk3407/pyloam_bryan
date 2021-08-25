import math
import numpy as np

print('★')


class FeatureExtract:
    def __init__(self, config=None):
        self.config = config
        self.used_line_num = None

        if config is None:
            self.LINE_NUM = 16  # NUM of LIDAR channel
            self.RING_INDEX = 4
            self.RING_INIT = True
            self.THRESHOLD = 0.2

        else:
            self.LINE_NUM = config['feature']['line_num']
            self.RING_INDEX = config['feature']['ring_index']
            self.RING_INIT = config['feature']['ring_init']
            self.THRESHOLD = config['feature']['dist_threshold']

    print('★★')

    def get_scan_id(self, cloud):
        xy_dist = np.sqrt(np.sum(np.square(cloud[:, :2]), axis=1))
        angles = np.arctan(cloud[:, 2]/xy_dist) * 180/math.pi  # tan(angles) = cloud[:, 2] / xy_dist

        if self.LINE_NUM == 16:
            scan_ids = (angles + 15)/2 + 0.5

        elif self.LINE_NUM == 32:
            scan_ids = int((angles + 93./3) * 3./4.)

        elif self.LINE_NUM == 64:
            scan_ids = self.LINE_NUM / 2 + (-8.83 - angles) * 2. + 0.5
            upper = np.where(angles >= -8.83)
            scan_ids[upper] = (2 - angles[upper]) * 3.0 + 0.5

        else:
            print("Specific line number not supported")
            return

        scan_ids = scan_ids.astype(int)
        if self.LINE_NUM == 64:
            correct_idx = np.where(np.logical_and(scan_ids >= 0, scan_ids < 50))  # why Only use 50 lines ??

        else:
            correct_idx = np.where(np.logical_and(scan_ids >= 0, scan_ids < self.LINE_NUM))

        scan_ids = scan_ids[correct_idx]
        cloud = cloud[correct_idx]
        scan_ids = np.expand_dims(scan_ids, axis=1)
        return cloud, scan_ids


print('★★★')

print('★★★★')