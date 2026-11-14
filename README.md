# 🎨 Rachna Studio

**Free aur open-source design editor — sabke liye, hamesha free.**
Posters, YouTube thumbnails, Instagram posts/stories, invitations, business cards, menus, presentation slides — sab kuch seedha browser mein. Koi login nahi, koi ads nahi, koi watermark nahi.

> Ek hi `index.html` file. Koi server, koi database, koi build step nahi. GitHub Pages par 2 minute mein live.

## ✨ Features

| | |
|---|---|
| 🧩 **Templates** | YouTube thumbnail, Sale post, Diwali, Birthday story, Quote, Business card, Presentation, Event poster, Story promo, Food menu |
| 🔤 **Text** | 24 fonts (Hindi/Devanagari bhi), size, weight, italic, underline, CAPS, align, line height, letter spacing, gradient text |
| 🌈 **Text effects** | Shadow, Lift, Outline, Hollow, Neon, Background, Splice |
| ⬟ **Shapes** | 17 shapes (star, heart, speech bubble, cloud, burst, badge...), gradient fill, border, rounded corners |
| ➖ **Lines** | Solid, dashed, dotted, arrows |
| 🖼 **Photos** | Upload, drag-drop, paste (Ctrl+V), shaped frames (circle, heart, star...), crop, 8 filter presets + 7 adjust sliders |
| 😊 **Stickers** | 70+ emoji stickers aur symbols |
| ✏️ **Draw** | Pen, marker, highlighter |
| 🎨 **Background** | Rang, 12 gradients, photo background |
| ✨ **AI Magic** | AI image banao (6 styles) aur Magic Write (AI text) — free, bina API key ([Pollinations.ai](https://pollinations.ai)) |
| ☰ **Layers** | Aage/peeche, chhupao (hide), lock |
| 📄 **Pages** | Multi-page, page copy, reorder |
| 📐 **Magic Resize** | 12 size presets + custom; content apne aap fit |
| 🧲 **Smart editing** | Snap guides, multi-select, marquee select, align & distribute, rotate, flip, undo/redo (100 steps) |
| ⬇ **Export** | PNG (transparent bhi), JPG, PDF (multi-page), SVG, 1x/2x/3x quality |
| 💾 **Save** | Browser mein auto-save + project file (`.rachna.json`) download/open |
| 🤖 **Rachna Agent** | Hindi/Hinglish mein bolo — "Diwali post banao", "background hatao", "PDF download karo" — agent khud design banata hai |
| ✂️ **Background Remover** | AI (BiRefNet-lite, MIT) browser ke andar hi — koi upload nahi; plus offline "plain background" remover |
| 🔤 **3D & Gradient text**, ▦ **QR code** | |
| 📱 **Mobile** | Phone par bhi chalta hai; app ki tarah install (PWA) aur offline |

## 🎬 Rachna Video (video.html) — VN/CapCut jaisa editor

| | |
|---|---|
| 🎞 **Timeline** | Video/Photo main track, Overlay (PiP) track, Text track, Audio track; drag karke time badlo, zoom |
| ✂️ **Editing** | Split, trim (frame-accurate numbers), speed 0.25×–3×, volume, reorder, duplicate, frame-by-frame ◀▮ ▮▶ |
| 🎨 **Look** | 8 filters + brightness/contrast/saturation/hue/blur, zoom/position/rotate/mirror, Ken Burns motion |
| 🔀 **Transitions** | Fade, Dip to black, Slide, Zoom, Wipe |
| 🖼 **Overlay / PiP** | Video ya photo upar rakho: size, position, rotate, opacity, gol kone, border, animation |
| 🟩 **Green screen** | Chroma key: koi bhi rang hatao, tolerance control |
| T **Text** | 13 fonts (Hindi bhi), Pop/Fade/Slide/Typewriter animation, outline, glow, background |
| 🎵 **Audio** | Copyright-free music browser mein hi banta hai (5 moods), apni voiceover record karo, apna gaana, fade in/out |
| ✨ **AI Movie Maker** | Kahani likho → AI script + har scene ki image + captions + transitions + music = movie |
| 🤖 **Video Agent** | "happy music lagao", "sab mein fade", "har photo 3 second ki karo", "export karo" |
| ⬇ **Export** | MP4 (jahan browser support kare) ya WebM, HD, audio ke saath |
| 🎨→🎬 | Design editor se pages seedha video mein (File → Video Editor mein bhejo) |

## 🚀 GitHub Pages par deploy (free)

1. GitHub par naya **public** repo banao, jaise `rachna-studio`.
2. Is folder ki saari files upload karo (**Add file → Upload files**), `.github` folder bhi. Commit karo.
3. Repo mein **Settings → Pages → Source: GitHub Actions** chuno.
4. 1-2 minute baad site live: `https://<aapka-username>.github.io/rachna-studio/`

(Asaan tareeka: Settings → Pages → *Deploy from a branch* → `main` / `root` bhi chalega.)

## 💻 Apne computer par chalao

Bas `index.html` ko browser mein kholo. Ya:

```bash
python3 -m http.server 8000
# phir http://localhost:8000 kholo
```

## ⌨️ Shortcuts

`T` text · `R` rectangle · `O` circle · `L` line · `P` draw · double-click = text edit · `Shift+click` multi-select · `Ctrl+Z/Y` undo/redo · `Ctrl+C/V/X/D` copy/paste/cut/duplicate · `Delete` · arrows (Shift = 10px) · `[ ]` layer order · `Ctrl+S` project save · `+ − 0` zoom

## 🗺 Roadmap (contributions welcome!)

- [ ] Group / ungroup
- [ ] Keyframe animation, auto-captions (speech-to-text), AI voice (TTS)
- [ ] GIF export
- [ ] Charts, tables, QR code
- [ ] Real-time collaboration
- [ ] Brand kit (logo, colors, fonts save)
- [ ] Zyada templates (community se)

## 🤝 Contribute

Fork karo → sudhaar karo → Pull Request bhejo. Naye templates `TEMPLATES` array (`index.html`) mein jodo — har template simple JS object hai.

## 📜 License

[MIT](LICENSE) — free to use, modify, and share. Fonts: Google Fonts (SIL Open Font License).
