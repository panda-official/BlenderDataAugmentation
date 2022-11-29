# Currently not usable
# Requires gradio to be installed in Blender's python

# from __future__ import annotations
import gradio as gr
import cv2
import bpy

from . import utils


def do_gradio(data_json, anottations, frames_preview, frames):
    images = []
    scene = bpy.data.scenes["Scene"]

    if frames_preview > frames:
        frames = frames_preview

    utils.augment_from_json(data_json)
    print("Augmentation finshed")
    utils.generate_bb_and_render(
        "bb+render", False, scene, frames, utils.count_json_classes(data_json)
    )
    print("Generation finshed")

    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
        (128, 0, 0),
        (0, 0, 0),
        (192, 192, 192),
        (255, 102, 0),
    ]

    for i in range(1, frames_preview):

        img = cv2.imread(fp + str(i) + ".png")

        if anottations == True:
            with open(fp + i + ".txt") as label:
                fp = scene.render.filepath
                lines = label.readlines()
                for line in lines:
                    values = line.split(" ")
                    c, x_norm, y_norm, w_norm, h_norm = values
                    x1, y1 = int(
                        (x_norm - w_norm / 2) * scene.render.resolution_x
                    ), int((y_norm - h_norm / 2) * scene.render.resolution_y)
                    x2, y2 = int(
                        (x_norm + w_norm / 2) * scene.render.resolution_x
                    ), int((y_norm + h_norm / 2) * scene.render.resolution_y)
                    img = cv2.rectangle(img, (x1, y1), (x2, y2), colors[c], 2)

        images.append([i, img])

    return images


def gradio_show():

    iface = gr.Interface(
        fn=do_gradio,
        inputs=[
            "file",
            "checkbox",
            gr.inputs.Slider(0, 50),
            gr.inputs.Slider(0, 10000),
        ],
        outputs=[gr.outputs.Carousel(["text", "image"], label=None)],
    )
    iface.launch()
