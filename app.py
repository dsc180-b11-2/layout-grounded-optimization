# import torch
### dumb text input
# import streamlit as st

# text = st.text_area("type something")

# if text:
#     out = text
#     st.write(out)


import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("rect", "transform")
)

# stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
# if drawing_mode == 'point':
#     point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
# stroke_color = st.sidebar.color_picker("Stroke color hex: ")
# bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
# bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
# rect_color = st.sidebar.color_picker("Object color hex: ")
# realtime_update = st.sidebar.checkbox("Update in realtime", True)

label_color = (
    st.sidebar.color_picker("Annotation color: ", "#EA1010") + "77"
)  # for alpha from 00 to FF
label = st.sidebar.text_input("Label", "Default")

mode = "transform" if st.sidebar.checkbox("Move ROIs", False) else "rect"


# Create a canvas component
canvas_result = st_canvas(
    # fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    fill_color = label_color,
    # stroke_width=stroke_width,
    stroke_width=2,
    # stroke_color=stroke_color,
    background_color="#eee",
    # background_image=Image.open(bg_image) if bg_image else None,
    # update_streamlit=realtime_update,
    update_streamlit=True,
    # height=150, # default height 400, width 600
    # width=500,
    drawing_mode=mode,
    # drawing_mode,
    # point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
    key="color_annotation_app",
)

# Do something interesting with the image data and paths
if canvas_result.json_data is not None:
    df = pd.json_normalize(canvas_result.json_data["objects"])
    if len(df) != 0:
        if "color_to_label" not in st.session_state:
            st.session_state["color_to_label"] = {}
            
        st.session_state["color_to_label"][label_color] = label
        df["label"] = df["fill"].map(st.session_state["color_to_label"])
        st.dataframe(df[["top", "left", "width", "height", "fill", "label"]])

with st.expander("Color to label mapping"):
    st.json(st.session_state["color_to_label"])

# Add color and labels to input


# counter = 0
# if canvas_result.json_data is not None:
#     df = pd.json_normalize(canvas_result.json_data["objects"])
#     if len(df) != 0:
#         if "idx_to_label" not in st.session_state:
#             st.session_state["idx_to_label"] = {}
        
#         st.session_state["idx_to_label"][counter] = label # df["fill"].map(st.session_state["color_to_label"])
#         counter += 1
#         st.write(st.session_state)
#         df["label"] = label
#         # st.dataframe(df[["top", "left", "width", "height", "fill", "label"]])

#     objects = pd.json_normalize(canvas_result.json_data["objects"]) # need to convert obj to str because PyArrow
#     for col in objects.select_dtypes(include=['object']).columns:
#         objects[col] = objects[col].astype("str")
#     st.dataframe(objects)




# with st.expander("Color to label mapping"):
#     st.json(st.session_state["color_to_label"])
    

# if canvas_result.json_data is not None:
#     ### test: add object info with text box
#     # objs = canvas_result.json_data["objects"] # objs: list; objs[-1]: dict
#     # if len(objs) > 0 and 'description' not in objs[-1]: # does not have description yet
#     #     # text = st.text_area("describe this object", key = 'text box')
#         # if text:
#         #     canvas_result.json_data["objects"][-1]['description'] = text
#         #     st.write(canvas_result.json_data["objects"])
#         #     del st.session_state['text box']
            
    
#     objects = pd.json_normalize(canvas_result.json_data["objects"]) # need to convert obj to str because PyArrow
#     for col in objects.select_dtypes(include=['object']).columns:
#         objects[col] = objects[col].astype("str")
#     st.dataframe(objects)