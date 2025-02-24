from youtube_transcript_api import YouTubeTranscriptApi
import os
from datetime import datetime


def get_transcript(video_id, lang="en", output_dir="transcripts"):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/transcript_{video_id}_{lang}_{timestamp}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            for entry in transcript:
                time = entry['start']
                text = entry['text']
                f.write(f"[{time:.2f}s] {text}\n")

        print(f"Transcript in {lang} has been created and stored into {filename}. You're welcome.")
        return filename

    except Exception as e:
        print(f"Error: {str(e)}. No transcript in {lang}.")
        return None


def list_available_languages(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        languages = [t.language_code for t in transcript_list]
        print(f"Availablelanguages: {', '.join(languages)}")
        return languages
    except Exception as e:
        print(f"Error: {str(e)}. No languages found.")
        return []


def main():
    video_url = input("Enter a YouTube video URL: ").strip()

    if "youtube.com" in video_url or "youtu.be" in video_url:
        if "v=" in video_url:
            video_id = video_url.split("v=")[1].split("&")[0]
        elif "youtu.be" in video_url:
            video_id = video_url.split("/")[-1].split("?")[0]
    else:
        video_id = video_url

    available_langs = list_available_languages(video_id)
    if not available_langs:
        print("No languages found.")
        return

    lang = input(f"Pick a language code (like 'en', 'es', 'fr') from {', '.join(available_langs)}: ").strip()

    get_transcript(video_id, lang)


if __name__ == "__main__":
    main()