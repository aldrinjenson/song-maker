import streamlit as st
import time
from src.utils import generate_audio_by_prompt, get_audio_information
from src.misc import generate_qr

st.set_page_config(
    page_title="Echoes of AI",
    page_icon="🎸",
)


def generate_song(description=""):
    print("description = ", description)

    # default song ids. gpt wizards theme song :)
    data = [
        {"id": "388d5922-47b9-43b7-beba-386ec859dcbc"},
        {"id": "2b243407-be62-491c-be50-d39da00869e9"},
    ]
    if description:
        data = generate_audio_by_prompt(
            {"prompt": description, "make_instrumental": False, "wait_audio": False}
        )
    else:
        print("no description given. Using defaults")

    print("data=", data)

    audio_urls = []
    songs = []
    if data:

        audio_ids = ",".join([str(item["id"]) for item in data])

        print("Audio Ids = ", audio_ids)

        for _ in range(60):
            data = get_audio_information(audio_ids)
            print("data = ", data)

            # todo: overwrite this each time using session state
            with st.expander("Audio Information", expanded=False):
                st.write(data[0])
                st.code(data[0]["lyric"])
            if data[0]["status"] == "streaming" or data[0]["status"] == "complete":
                # if data[1]["status"] == "streaming":
                audio_urls.append(data[0]["audio_url"])
                audio_urls.append(data[1]["audio_url"])
                songs.extend(
                    [
                        {
                            "id": data[0]["id"],
                            "title": data[0]["title"],
                            "image_url": data[0]["image_url"]
                            or "https://placehold.co/600x400?text=No+preview+image",
                            "lyric": data[0]["lyric"],
                            "audio_url": data[0]["audio_url"],
                            "video_url": data[0]["video_url"],
                            "tags": data[0]["tags"],
                        },
                        {
                            "id": data[1]["id"],
                            "title": data[1]["title"],
                            "image_url": data[1]["image_url"]
                            or "https://placehold.co/600x400?text=No+preview+image",
                            "lyric": data[1]["lyric"],
                            "audio_url": data[1]["audio_url"],
                            "video_url": data[1]["video_url"],
                            "tags": data[1]["tags"],
                        },
                    ]
                )

                print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
                print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
                break
            # sleep 5s
            time.sleep(5)
        print("\n\n\nsong generated: \n")
        print(songs)

        for song in songs:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(song["image_url"])
            with col2:
                st.subheader(song["title"])
                st.text(f"Song generated on {time.strftime('%Y-%m-%d %H:%M:%S')}")
            st.code(song["lyric"])
            st.audio(song["audio_url"])

            song_video_url = f"https://cdn1.suno.ai/{song['id']}.mp4"
            qr_img = generate_qr(song_video_url)

            st.markdown(f"[View Video]({song_video_url})")
            with st.expander("Download by QR", expanded=False):
                st.image(qr_img, caption="QR Code", use_column_width=True)


def main():
    st.title("Echoes of AI")
    st.write("Powered by Suno.AI")
    description = st.text_area("Enter a description for a song", height=100)

    if st.button("Generate Song"):
        generate_song(description)


main()
