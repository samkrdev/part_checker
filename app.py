import streamlit as st
import pandas as pd

# Utils
import base64
import time

st.set_page_config(layout="wide")
timestr = time.strftime("%Y%m%d-%H%M%S")


class FileDownloader(object):
    """docstring for FileDownloader
    >>> download = FileDownloader(data,filename,file_ext).download()
    """

    def __init__(self, data, filename="results", file_ext="txt"):
        super(FileDownloader, self).__init__()
        self.data = data
        self.filename = filename
        self.file_ext = file_ext

    def download(self):
        b64 = base64.b64encode(self.data.encode()).decode()
        new_filename = "{}_{}_.{}".format(self.filename, timestr, self.file_ext)
        st.markdown("#### Download File ###")
        href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">Click Here!!</a>'
        st.markdown(href, unsafe_allow_html=True)


st.title("Part Filter")
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Master String ")
    txt = st.text_area("Enter the master text here")
    st.write(txt)
    checkstring = set(map("".join, zip(*[iter(txt)] * 5)))
with col2:
    st.markdown("### File upload")
    uploaded_file = st.file_uploader("Choose an xlsx file")


if len(txt) > 0 and uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    # part_dict = data.set_index("Part No").T.to_dict("list")

    col3, col4 = st.columns(2)
    with col3:
        part = st.selectbox("Select parts column", (data.columns))
        st.write("parts:", part)
    with col4:
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

        df = pd.DataFrame()
        results_list = []

        for k, v in part_dict_cleaned.items():
            if all([part in checkstring for part in v]):
                results_list.append(k)
                st.write(k)
        if len(results_list) > 0:
            st.balloons()
        df["parts"] = results_list
        FileDownloader(df.to_csv(), file_ext="csv").download()

    # st.write('You selected:', options)
