import streamlit as st
import time
from src.utils import generate_audio_by_prompt, get_audio_information


def generate_song(description):
    # data = generate_audio_by_prompt(
    #     {"prompt": description, "make_instrumental": False, "wait_audio": False}
    # )
    # print("data=", data)
    data = True

    audio_urls = []
    songs = []
    if data:
        # audio_ids = ",".join([str(item["id"]) for item in data])

        audio_ids = [
            "137cf652-03e9-4064-8b02-fe31bffa308a",
            "c80ef39d-7276-4b97-9377-e70d4e93e3e7",
        ]
        audio_ids = ",".join(audio_ids)
        print("Audio Ids = ", audio_ids)

        for _ in range(60):
            data = get_audio_information(audio_ids)
            print("data = ", data)
            if data[0]["status"] == "streaming" or data[0]["status"] == "complete":
                audio_urls.append(data[0]["audio_url"])
                audio_urls.append(data[1]["audio_url"])
                songs.append(
                    {
                        "id": data[0]["id"],
                        "title": data[0]["title"],
                        "image_url": data[0]["image_url"],
                        "lyric": data[0]["lyric"],
                        "audio_url": data[0]["audio_url"],
                    }
                )

                songs.append(
                    {
                        "id": data[1]["id"],
                        "title": data[1]["title"],
                        "image_url": data[1]["image_url"],
                        "lyric": data[1]["lyric"],
                        "audio_url": data[1]["audio_url"],
                    }
                )

                # audio_lyrics.append(data[0]["lyrics"], data[1]["lyrics"])
                print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
                print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
                break
            # sleep 5s
            time.sleep(5)
        print("\n\n\nsong generated: \n")
        print(songs)

        # audio_info = get_audio_information(audio_ids)
        # print("Audio Info = ", audio_info)

        # Display audio widgets
        for song in songs:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(song["image_url"])
            with col2:
                st.subheader(song["title"])
                st.text(f"Song generated on {time.strftime('%Y-%m-%d %H:%M:%S')}")
            st.code(song["lyric"])
            st.audio(song["audio_url"])


def main():
    st.title("AI Music Generator")

    # User input for description
    description = st.text_area("Enter a description for the song", height=100)

    # Button to generate the song
    if st.button("Generate Song"):
        generate_song(description)


main()
