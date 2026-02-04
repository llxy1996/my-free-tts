from flask import Flask, request, Response
import edge_tts
import asyncio

app = Flask(__name__)

async def _do_tts(text, voice, rate, pitch):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

@app.route('/api/tts', methods=['GET'])
def tts_handler():
    text = request.args.get('text', '')
    voice = request.args.get('voice', 'zh-CN-XiaoxiaoNeural')
    rate = request.args.get('rate', '+0%')
    pitch = request.args.get('pitch', '+0Hz')

    if not text:
        return "Please provide text", 400

    try:
        audio_content = asyncio.run(_do_tts(text, voice, rate, pitch))
        return Response(audio_content, mimetype='audio/mpeg')
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run()
