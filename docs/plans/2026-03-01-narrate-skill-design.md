# Narrate Skill Design

**Goal:** Create a `/narrate` skill that converts Hugo blog posts to audio using Edge-TTS, storing audio alongside the post in a Page Bundle.

**Architecture:** Skill reads post markdown, converts to speech-friendly text, generates audio via Edge-TTS, compresses with ffmpeg, and embeds an `<audio>` player in the post.

**Key decisions:**
- Audio stored in Page Bundle (same directory as post)
- 64kbps mono mp3 for small file size
- User selects TTS voice at runtime
- Auto-converts standalone .md to Page Bundle format
