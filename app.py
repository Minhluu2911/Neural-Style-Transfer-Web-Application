from ultils import *
st.set_page_config(
    page_title="Style Tranfer Network App",
    layout="wide"
)

st.title('NEURAL STYLE TRANSFER: CREATING YOUR ART WITH DEEP LEARNING')
st.write("""
 ***Description***: Neural style transfer is an optimization technique used to take your image and a style reference (such as an artwork by a famous painter) — and blend them together such that the input image is transformed to look like the style reference.
         """)

col1, col2 = st.columns(2)

# choosing & loading image
with col1:
    style_model = st.selectbox(
        'Choose your style',
        model_name['model'])

    'You selected: ', style_model
    input_image = st.file_uploader("Choose a Content Image", type=["png", "jpg", "jpeg"])
    if input_image is not None:
        caption = input_image.name
        st.image(input_image, caption=caption, width=300)
    

with col2:
    generate_image(input_image, style_model)
