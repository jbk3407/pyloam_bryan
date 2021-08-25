import os
import numpy as np
import open3d as o3d
from pypcd import pypcd  # Python module to read and write point clouds
'''
<fixed error>
changed cStringIO -> io @ "/home/bryan/anaconda3/envs/pyloam_bryan/lib/python3.6/site-packages/pypcd/pypcd.py"

<before fix>
ModuleNotFoundError: No module named 'cStringIO
'''


class DataLoader:
    def __init__(self, path): # 원래 코드에서는 name이 있는데 필요 없어보여서 뺏음.
        self.path = path
        self.data_list = os.listdir(path)
        self.data_list_length = len(self.data_list)
        self.sort_files()

    def get_pcd(self, index):   #상속해서 구현하라고 비워두는 함수
        pass

    def sort_files(self):   #상속해서 구현하라고 비워두는 함수
        pass

    def __getitem__(self, index):
        return self.get_pcd(index)

    def __len__(self):
        return self.data_list_length


class KittiLoader(DataLoader):
    def get_pcd(self, index):
        if index < self.data_list_length:
            scan = np.fromfile(os.path.join(self.path, self.data_list[index]), dtype=np.float32).reshape(-1, 4)
            return scan
        else:
            print('list out of range!! check scan @ KITTI_LOADER.py.KittiLoader.get_pcd')

    def sort_files(self):
        self.data_list.sort(key=lambda file: int(file[:4]))  #아직 file 이 뭔지 모르겠네.

    # def visualize(self):
    #     for i in range(self.data_list_length):
    #         scan =self.get_pcd(i)
    #         visualize_scan(scan)


class PcdLoader(DataLoader):
    def get_pcd(self, index):
        if index < self.data_list_length:
            pcd = pypcd.PointCloud.from_path(os.path.join(self.path, self.data_list[index]))
            raw_data = pcd.pc_data
            return raw_data
        else:
            print('something wrong @ KITTI_LOADER.py.PcdLoader.get_pcd')

    def sort_files(self):
        self.data_list.sort(key=lambda file: int(file[:-4]))

    # def visualize(self):
    #     for i in range(self.data_list_length):
    #         scan =self.get_pcd(i)
    #         visualize_scan(scan)


def visualize_scan(self, scan):
    point_cloud_from_open3d = o3d.geometry.PointCloud()
    point_cloud_from_open3d.points = o3d.utility.Vector3dVector(scan[:, :3])
    o3d.visualization.draw_geometries([point_cloud_from_open3d])      # show 1 pic

#     vis = o3d.visualization.Visualizer
#     vis.add_geometry(self.point_cloud_from_open3d)
#     vis.poll_events(self)
#     vis.update_renderer(self)
#
# time.sleep(1)
# save_img_folder = "/home/bryan/PycharmProjects/LOAM/image/"
# vis.capture_screen_image(save_img_folder + "00_3000_end.png")
#
#
# vis.destroy_window()

