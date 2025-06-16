import edge_tts


async def tts(text, voice="en-US-JennyNeural", outfile="output.mp3"):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(outfile)


async def fetch_voices():
    return await edge_tts.list_voices()
