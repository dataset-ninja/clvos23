import os
import shutil
import numpy as np
import supervisely as sly
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s
from dataset_tools.convert import unpack_if_archive


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # Possible structure for bbox case. Feel free to modify as you needs.

    images_path = "/home/alex/DATASETS/IMAGES/CLVOS23/JPEGImages"
    masks_path = "/home/alex/DATASETS/IMAGES/CLVOS23/Annotations"

    images_ext = ".jpg"
    masks_ext = ".png"

    batch_size = 30
    ds_name = "ds"


    def create_ann(image_path):
        labels = []

        mask_path = image_path.replace("JPEGImages", "Annotations").replace(images_ext, masks_ext)
        if file_exists(mask_path):
            ann_np = sly.imaging.image.read(mask_path)[:, :, 0]

            if len(np.unique(ann_np)) > 1:
                obj_mask = ann_np == 128
                curr_bitmap = sly.Bitmap(obj_mask)
                curr_label = sly.Label(curr_bitmap, obj_class)
                labels.append(curr_label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=[tag])


    person = sly.ObjClass("person", sly.Bitmap)
    rat = sly.ObjClass("rat", sly.Bitmap)
    car = sly.ObjClass("car", sly.Bitmap)
    dog = sly.ObjClass("dog", sly.Bitmap)
    dressage = sly.ObjClass("dressage", sly.Bitmap)

    folder_to_class = {
        "skiing": person,
        "parkour_boy": person,
        "rat": rat,
        "car": car,
        "dog": dog,
        "skiing_slalom": person,
        "blueboy": person,
        "dressage": dressage,
        "skating": person,
    }

    video_name_meta = sly.TagMeta(
        "video name",
        sly.TagValueType.ONEOF_STRING,
        possible_values=[
            "skiing",
            "parkour boy",
            "rat",
            "car",
            "dog",
            "skiing slalom",
            "blueboy",
            "dressage",
            "skating",
        ],
    )


    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    meta = sly.ProjectMeta(obj_classes=[rat, car, dog, dressage, person], tag_metas=[video_name_meta])
    api.project.update_meta(project.id, meta.to_json())


    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    for subfolder in os.listdir(images_path):
        obj_class = folder_to_class[subfolder]
        tag_value = subfolder.replace("_", " ")
        tag = sly.Tag(video_name_meta, value=tag_value)

        curr_images_path = os.path.join(images_path, subfolder)

        images_names = os.listdir(curr_images_path)

        image_np = sly.imaging.image.read(os.path.join(curr_images_path, images_names[0]))[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for images_names_batch in sly.batched(images_names, batch_size=batch_size):
            img_pathes_batch = [
                os.path.join(curr_images_path, image_name) for image_name in images_names_batch
            ]

            anns_batch = [create_ann(image_path) for image_path in img_pathes_batch]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(images_names_batch))

    return project
