import streamlit as st
import pandas as pd

st.title("Part Filter")
st.markdown("### Master String ")
txt = st.text_area("Enter the master text here")
st.write(txt)
checkstring = set(map("".join, zip(*[iter(txt)] * 5)))

st.markdown("### File upload")
uploaded_file = st.file_uploader("Choose an xlsx file")
if len(txt) > 0 and uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    # part_dict = data.set_index("Part No").T.to_dict("list")
    part = st.selectbox("Select parts column", (data.columns))
    st.write("parts:", part)
    config_options = st.multiselect(
        "Select Config Columns", options=data.columns, default=None
    )
    if len(config_options) > 0:
        data_new = data[[part] + config_options].copy()
        st.table(data_new.head(2))
        part_dict = data_new.set_index(part).T.to_dict("list")
        part_dict_cleaned = {
            k: [x for x in v if str(x) != "nan"] for k, v in part_dict.items()
        }

        for k, v in part_dict_cleaned.items():
            if all([part in checkstring for part in v]):
                st.write(k)

    # st.write('You selected:', options)
