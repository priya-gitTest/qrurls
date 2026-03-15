"""
QRURLs — Streamlit web app
Deploy for free on Streamlit Community Cloud: https://share.streamlit.io
"""

import io

import streamlit as st

from qrurls import QRGenerator, QRURLs, ShorteningError
from qrurls.exceptions import InvalidURLError

st.set_page_config(page_title="QRURLs", page_icon=":link:", layout="centered")

st.title("QRURLs")
st.markdown("Generate QR codes and shorten URLs — powered by open source services.")

url = st.text_input("Enter a URL", placeholder="https://example.com/your/long/url")

col1, col2 = st.columns(2)
with col1:
    action = st.selectbox("Action", ["Shorten + QR Code", "Shorten Only", "QR Code Only"])
with col2:
    service = st.selectbox("Service", ["tinyurl", "isgd", "vgd"])

with st.expander("QR Code Options"):
    box_size = st.slider("Box size", min_value=5, max_value=20, value=10)
    border = st.slider("Border", min_value=1, max_value=10, value=4)

if st.button("Generate", type="primary"):
    if not url:
        st.warning("Please enter a URL.")
    else:
        try:
            qrurls = QRURLs(service=service, box_size=box_size, border=border)

            if action == "Shorten + QR Code":
                with st.spinner("Shortening URL and generating QR code..."):
                    short_url, _ = qrurls.process(url, "qr_output.png")

                st.success(f"Shortened URL: **{short_url}**")

                # Generate image in memory for display
                qr_gen = QRGenerator(box_size=box_size, border=border)
                img = qr_gen.generate(short_url)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)

                st.image(buf, caption=f"QR code for {short_url}", width=300)
                st.download_button(
                    "Download QR Code",
                    data=buf.getvalue(),
                    file_name="qrurls_output.png",
                    mime="image/png",
                )

            elif action == "Shorten Only":
                with st.spinner("Shortening URL..."):
                    short_url = qrurls.shorten_only(url)

                st.success(f"Shortened URL: **{short_url}**")
                st.code(short_url, language=None)

            elif action == "QR Code Only":
                qr_gen = QRGenerator(box_size=box_size, border=border)
                img = qr_gen.generate(url)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)

                st.image(buf, caption=f"QR code for {url}", width=300)
                st.download_button(
                    "Download QR Code",
                    data=buf.getvalue(),
                    file_name="qrurls_output.png",
                    mime="image/png",
                )

        except InvalidURLError:
            st.error("Invalid URL. Please enter a valid URL starting with http:// or https://")
        except ShorteningError as e:
            st.error(f"Shortening failed: {e}")

st.divider()
st.caption(
    "Built with [QRURLs](https://github.com/priya-gitTest/qrurls) "
    "by [Priyanka O](https://orcid.org/0000-0002-6844-6493) · "
    "[Install via PyPI](https://pypi.org/project/qrurls/) · MIT License"
)
