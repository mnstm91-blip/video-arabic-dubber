import streamlit as st
import os
import whisper
import asyncio
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip

st.title("🎬 V-MAX AI Video Dubber")
st.write("ارفع فيديو وسيقوم الذكاء الاصطناعي بدبلجته للعربية مجاناً!")

uploaded_file = st.file_uploader("اختر ملف الفيديو (MP4)", type=["mp4"])

async def process_video(video_path, output_path):
    # 1. تفريغ وترجمة
    model = whisper.load_model("tiny")
    result = model.transcribe(video_path, task="translate")
    arabic_text = result["text"]
    
    # 2. توليد الصوت العربي
    voice = "ar-SA-HamedNeural"
    communicate = edge_tts.Communicate(arabic_text, voice)
    temp_audio = "temp_voice.mp3"
    await communicate.save(temp_audio)
    
    # 3. دمج الفيديو
    video = VideoFileClip(video_path)
    arabic_audio = AudioFileClip(temp_audio)
    final_video = video.set_audio(arabic_audio)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    video.close()
    arabic_audio.close()
    os.remove(temp_audio)

if uploaded_file is not None:
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())
        
    st.info("⏳ جاري معالجة الفيديو ودبلجته... انتظر قليلاً.")
    
    try:
        asyncio.run(process_video("input.mp4", "output.mp4"))
        st.success("✅ تم دبلجة الفيديو بنجاح!")
        
        with open("output.mp4", "rb") as file:
            st.download_button(label="📥 تحميل الفيديو المدبلج", data=file, file_name="arabic_video.mp4", mime="video/mp4")
    except Exception as e:
        st.error(f"حدث خطأ أثناء المعالجة: {e}")
