import hashlib
import os

from PIL import Image, ImageOps
import torch
import numpy as np

import folder_paths
from .openai_client import convert_bson_to_image, OpenAiClient
from .settings import load_settings
import openai


class CyberDolphinImageneering:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "prompt": ('STRING', {'default': 'a white siamese cat'}),
            "size": (["256x256", "512x512", "1024x1024"], {'default': "1024x1024"}),
        }}

    CATEGORY = "🐬 CyberDolphin"
    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image"

    def load_image(self, prompt: str, size: str):
        """
        Loads an image from api.openai.com.
        https://platform.openai.com/docs/api-reference/images/create

        Args:
            prompt: A text description of the desired image. The maximum length is 1000 characters.
            size: Must be one of: 256x256, 512x512, 1024x1024

        Returns:

        """
        i = OpenAiClient.image_create(prompt=prompt, size=size)
        i = ImageOps.exif_transpose(i)

        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
        return (image, mask.unsqueeze(0))

    @classmethod
    def IS_CHANGED(s, image):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    # @classmethod
    # def VALIDATE_INPUTS(s, image):
    #     # if not folder_paths.exists_annotated_filepath(image):
    #     #     return "Invalid image file: {}".format(image)
    #
    #     return True
