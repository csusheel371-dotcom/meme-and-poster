import json
import io
import time
import requests
import gradio as gr
from PIL import Image, ImageDraw, ImageFont

# -------------------------
# Base44 credentials
# -------------------------
BASE44_KEY = "a73335842f7948e0abe2c58374850a82"
BASE44_APP_ID = "68ea3fda8a977b8a8cc808aa"
BASE_API = "https://app.base44.com/api"

HEADERS = {
    "api_key": BASE44_KEY,
    "Content-Type": "application/json"
}

# -------------------------
# Base44 API helpers
# -------------------------
def make_api_request(api_path, method='GET', data=None):
    url = f'{BASE_API}/{api_path}'
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=HEADERS, params=data, timeout=20)
        else:
            response = requests.request(method, url, headers=HEADERS, json=data, timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("API request error:", e)
        return {"error": str(e)}

def list_creations():
    return make_api_request(f'apps/{BASE44_APP_ID}/entities/Creation')

def create_creation(payload):
    return make_api_request(f'apps/{BASE44_APP_ID}/entities/Creation', method='POST', data=payload)

def update_creation(entity_id, payload):
    return make_api_request(f'apps/{BASE44_APP_ID}/entities/Creation/{entity_id}', method='PUT', data=payload)

# -------------------------
# Image composition
# -------------------------
def get_font(size=40):
    for font_name in ["Impact.ttf", "arial.ttf"]:
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            continue
    return ImageFont.load_default()

def load_image_from_input(image_url=None, image_file=None):
    """
    Loads an image from a URL or uploaded file path.
    """
    if image_file:
        try:
            img = Image.open(image_file).convert("RGBA")
            return img
        except Exception as e:
            raise Exception(f"Image file load error: {e}")

    if image_url:
        try:
            resp = requests.get(image_url.strip(), stream=True, timeout=20)
            resp.raise_for_status()
            img = Image.open(resp.raw).convert("RGBA")
            return img
        except Exception as e:
            raise Exception(f"Image URL load error: {e}")

    raise Exception("No image source provided")

def compose_image(image_source, text_elements_json, out_size=(1024, 1024)):
    try:
        img = image_source
        img.thumbnail(out_size, Image.LANCZOS)
    except Exception as e:
        raise Exception(f"Image processing error: {e}")

    canvas = Image.new("RGBA", out_size, (255, 255, 255, 255))
    x = (out_size[0] - img.width) // 2
    y = (out_size[1] - img.height) // 2
    canvas.paste(img, (x, y))

    draw = ImageDraw.Draw(canvas)

    try:
        text_elements = json.loads(text_elements_json) if isinstance(text_elements_json, str) else text_elements_json or []
    except Exception:
        text_elements = []

    for el in text_elements:
        content = el.get("content", "")
        position = el.get("position", "middle")
        font_size = int(el.get("fontSize", 40))
        color = el.get("color", "#FFFFFF")
        stroke = el.get("strokeColor", "#000000")
        font = get_font(max(12, font_size))

        cx = out_size[0] // 2
        cy = {
            "top": int(out_size[1] * 0.12 + font_size // 2),
            "bottom": int(out_size[1] * 0.88 - font_size // 2),
            "middle": out_size[1] // 2
        }.get(position, out_size[1] // 2)

        stroke_w = max(1, font_size // 12)
        draw.text((cx, cy), content, font=font, fill=color, anchor="mm", stroke_width=stroke_w, stroke_fill=stroke)

    buf = io.BytesIO()
    canvas.convert("RGB").save(buf, format="PNG", quality=95)
    buf.seek(0)
    return buf.getvalue()

# -------------------------
# Gradio callbacks
# -------------------------
def test_connection():
    result = list_creations()
    return "✅ Base44 connection OK" if isinstance(result, list) else f"❌ Connection failed: {result.get('error')}"

def preview_image_action(image_url, image_file, text_elements_json):
    if not image_url and not image_file:
        return None, "⚠️ Please upload or provide a public image URL"

    try:
        img = load_image_from_input(image_url, image_file)
        img_bytes = compose_image(img, text_elements_json)
        return img_bytes, "✅ Preview generated"
    except Exception as e:
        return None, f"❌ Preview error: {e}"

def create_entity_action(title, entity_type, image_url, image_file, text_elements_json, background_url=None, template_name=None):
    if not title or not entity_type:
        return "⚠️ Title and type are required"

    try:
        img = load_image_from_input(image_url, image_file)
        final_bytes = compose_image(img, text_elements_json)
    except Exception as e:
        return f"❌ Error composing image: {e}"

    filename = f"creation_{entity_type}_{int(time.time())}.png"
    with open(filename, "wb") as f:
        f.write(final_bytes)

    payload = {
        "title": title,
        "type": entity_type,
        "image_url": image_url or "local_upload",
        "background_url": background_url or image_url,
        "text_elements": json.loads(text_elements_json) if text_elements_json else [],
        "template_name": template_name
    }

    result = create_creation(payload)
    return f"✅ Created entity: {result}\nSaved local file: {filename}" if "error" not in result else f"❌ Error: {result['error']}"

def list_entities_action():
    result = list_creations()
    if not isinstance(result, list):
        return [], f"❌ Error: {result.get('error')}"
    images = [e.get("image_url") for e in result if e.get("image_url")]
    captions = [f"{e.get('title', 'Untitled')} — {e.get('type', '')}\nID:{e.get('id')}" for e in result]
    return images, "\n".join(captions)

def update_entity_action(entity_id, new_title, new_image_url, new_type):
    if not entity_id:
        return "⚠️ Provide entity ID"
    data = {k: v for k, v in [("title", new_title), ("image_url", new_image_url), ("type", new_type)] if v}
    if not data:
        return "⚠️ Nothing to update"
    result = update_creation(entity_id, data)
    return f"✅ Updated: {result}" if "error" not in result else f"❌ Update failed: {result['error']}"

# -------------------------
# Gradio UI
# -------------------------
def build_ui():
    with gr.Blocks(title="AI Meme and Poster (Base44)") as demo:
        gr.Markdown("# 🖼️ AI Meme and Poster Creator")

        # --- Test Tab ---
        with gr.Tab("Test"):
            tbtn = gr.Button("Test Base44 connection")
            tout = gr.Textbox(lines=2)
            tbtn.click(fn=test_connection, outputs=tout)

        # --- Creator / Preview Tab ---
        with gr.Tab("Creator / Preview"):
            with gr.Row():
                with gr.Column(scale=2):
                    preview = gr.Image(label="Preview")
                    preview_status = gr.Textbox(label="Status", lines=2)
                    render_btn = gr.Button("Render preview")
                    create_btn = gr.Button("Create & Save (Base44)")
                with gr.Column(scale=1):
                    title_in = gr.Textbox(label="Title")
                    type_in = gr.Dropdown(["meme", "poster"], value="meme", label="Type")
                    image_url_in = gr.Textbox(label="Image URL (optional)")
                    image_file_in = gr.Image(label="Or Upload Image", type="filepath")
                    texts_in = gr.Textbox(
                        label="Text elements (JSON list)",
                        value='[{"content":"TOP TEXT","position":"top","fontSize":48,"color":"#FFFFFF","strokeColor":"#000000"},{"content":"BOTTOM TEXT","position":"bottom","fontSize":48,"color":"#FFFFFF","strokeColor":"#000000"}]',
                        lines=8
                    )
                    template_in = gr.Textbox(label="Template name (optional)")

            create_out = gr.Textbox(label="Create result", lines=6)
            render_btn.click(fn=preview_image_action, inputs=[image_url_in, image_file_in, texts_in], outputs=[preview, preview_status])
            create_btn.click(fn=create_entity_action, inputs=[title_in, type_in, image_url_in, image_file_in, texts_in, image_url_in, template_in], outputs=create_out)

        # --- Gallery Tab ---
        with gr.Tab("Gallery"):
            load_btn = gr.Button("Load creations")
            gallery = gr.Gallery(label="Creations", columns=3, height="auto")
            captions = gr.Textbox(label="Captions", lines=6)
            load_btn.click(fn=list_entities_action, outputs=[gallery, captions])

            upd_id = gr.Textbox(label="Entity ID to update")
            upd_title = gr.Textbox(label="New title (optional)")
            upd_image = gr.Textbox(label="New image URL (optional)")
            upd_type = gr.Dropdown(["meme", "poster"], value=None, label="New type (optional)")
            upd_btn = gr.Button("Update")
            upd_out = gr.Textbox(label="Update result", lines=3)
            upd_btn.click(fn=update_entity_action, inputs=[upd_id, upd_title, upd_image, upd_type], outputs=upd_out)

    return demo

if __name__ == "__main__":
    demo = build_ui()
    demo.launch()
