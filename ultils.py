from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import cv2
import os
import imutils

# Style Models Data
style_models_file = ['candy.t7', 'composition_vii.t7', 'feathers.t7', 'la_muse.t7', 'mosaic.t7', 'starry_night.t7', 'the_scream.t7', 'the_wave.t7', 'udnie.t7']
style_models_name = ['Candy', 'Composition_vii', 'Feathers', 'La_muse', 'Mosaic', 'Starry_night', 'The_scream', 'The_wave', 'Udnie']
model_path = 'models'
style_models_dict = {name: os.path.join(model_path, file) for name, file in zip(style_models_name, style_models_file)}

model_name = pd.DataFrame({
    'model': ['Candy', 'Composition_vii', 'Feathers', 'La_muse', 'Mosaic', 'Starry_night', 'The_scream', 'The_wave', 'Udnie']
    })

def get_model_from_path(style_model_path):
    model = cv2.dnn.readNetFromTorch(style_model_path)
    return model

def style_transfer(image, model):
    (h, w) = image.shape[:2]
    # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) #PIL Jpeg to Opencv image

    blob = cv2.dnn.blobFromImage(image, 1.0, (w, h), (103.939, 116.779, 123.680), swapRB=False, crop=False)
    model.setInput(blob)
    output = model.forward()

    output = output.reshape((3, output.shape[2], output.shape[3]))
    output[0] += 103.939
    output[1] += 116.779
    output[2] += 123.680
    output /= 255.0
    output = output.transpose(1, 2, 0)
    output = np.clip(output, 0.0, 1.0)
    output = imutils.resize(output, width=500)
    return output

def generate_image(input_image, style_model):
    style_model_path = style_models_dict[style_model]
    model = get_model_from_path(style_model_path)

    if input_image is not None:
        content = Image.open(input_image)
        content = np.array(content) #pil to cv
        content = cv2.cvtColor(content, cv2.COLOR_RGB2BGR)
    else:
        st.warning("Please upload image for generating new image!")
        st.stop()

    WIDTH = st.select_slider('Affected style', list(range(100, 1001, 10)), value=400)
    content = imutils.resize(content, width=WIDTH)
    generated = style_transfer(content, model)
    st.image(generated, width=300)
    
    if generated is not None:
        from io import BytesIO
        animage = Image.fromarray((generated * 255).astype(np.uint8))
        imagefile = BytesIO()
        animage.save(imagefile, format='png')
        imagedata = imagefile.getvalue()
        
        st.download_button(
            label="Download image",
            data=imagedata,
            file_name="flower.png",
            mime="image/png"
        )