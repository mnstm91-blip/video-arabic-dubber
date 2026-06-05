from flask import Flask, render_template_string, request, send_file
import asyncio
import edge_tts
import os

app = Flask(__name__)

# واجهة مستخدم بسيطة وأنيقة مدمجة داخل الكود لتفتح في المتصفح
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>V-MAX AI Voice Generator</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f7f6; text-align: center; padding: 50px; }
        .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; max-width: 500px; width: 100%; }
        textarea { width: 100%; height: 100px; margin: 15px 0; padding: 10px; border-radius: 5px; border: 1px solid #ccc; box-sizing: border-box; font-size: 16px; }
        button { background: #28a745; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; width: 100%; font-weight: bold; }
        button:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🎬 V-MAX AI Voice Generator</h2>
        <p>اكتب النص العربي بالأسفل لتوليد ملف صوتي نقي بالذكاء الاصطناعي:</p>
        <form method="POST" action="/generate">
            <textarea name="text" placeholder="اكتب النص هنا..." required></textarea>
            <button type="submit">🔊 توليد وتحميل الصوت (MP3)</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text')
    output_audio = "arabic_voice.mp3"
    
    # دالة توليد الصوت من مايكروسوفت
    async def generate_voice():
        voice = "ar-SA-HamedNeural"
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_audio)

    # تشغيل الدالة داخل بيئة Flask
    asyncio.run(generate_voice())
    
    # إرسال ملف الصوت للمتصفح ليتم تحميله فوراً على هاتفك
    if os.path.exists(output_audio):
        return send_file(output_audio, as_attachment=True)
    return "حدث خطأ أثناء توليد الصوت", 500

if __name__ == '__main__':
    # التشغيل المتوافق مع السيرفرات
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
