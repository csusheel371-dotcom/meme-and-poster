{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyP4sKxsLPVdO3FK72VOsRY6",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/csusheel371-dotcom/meme-and-poster/blob/main/AI_POSTERS_AND_MEMES_2.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 11,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "nfH-a9uoGGPo",
        "outputId": "5556d780-0e1a-46a5-ca6b-f8f98c969d91"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: google-genai in /usr/local/lib/python3.12/dist-packages (1.41.0)\n",
            "Requirement already satisfied: pillow in /usr/local/lib/python3.12/dist-packages (11.3.0)\n",
            "Requirement already satisfied: requests in /usr/local/lib/python3.12/dist-packages (2.32.5)\n",
            "Requirement already satisfied: anyio<5.0.0,>=4.8.0 in /usr/local/lib/python3.12/dist-packages (from google-genai) (4.11.0)\n",
            "Requirement already satisfied: google-auth<3.0.0,>=2.14.1 in /usr/local/lib/python3.12/dist-packages (from google-genai) (2.38.0)\n",
            "Requirement already satisfied: httpx<1.0.0,>=0.28.1 in /usr/local/lib/python3.12/dist-packages (from google-genai) (0.28.1)\n",
            "Requirement already satisfied: pydantic<3.0.0,>=2.0.0 in /usr/local/lib/python3.12/dist-packages (from google-genai) (2.11.9)\n",
            "Requirement already satisfied: tenacity<9.2.0,>=8.2.3 in /usr/local/lib/python3.12/dist-packages (from google-genai) (8.5.0)\n",
            "Requirement already satisfied: websockets<15.1.0,>=13.0.0 in /usr/local/lib/python3.12/dist-packages (from google-genai) (15.0.1)\n",
            "Requirement already satisfied: typing-extensions<5.0.0,>=4.11.0 in /usr/local/lib/python3.12/dist-packages (from google-genai) (4.15.0)\n",
            "Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests) (3.4.3)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.12/dist-packages (from requests) (3.10)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.12/dist-packages (from requests) (2.5.0)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.12/dist-packages (from requests) (2025.8.3)\n",
            "Requirement already satisfied: sniffio>=1.1 in /usr/local/lib/python3.12/dist-packages (from anyio<5.0.0,>=4.8.0->google-genai) (1.3.1)\n",
            "Requirement already satisfied: cachetools<6.0,>=2.0.0 in /usr/local/lib/python3.12/dist-packages (from google-auth<3.0.0,>=2.14.1->google-genai) (5.5.2)\n",
            "Requirement already satisfied: pyasn1-modules>=0.2.1 in /usr/local/lib/python3.12/dist-packages (from google-auth<3.0.0,>=2.14.1->google-genai) (0.4.2)\n",
            "Requirement already satisfied: rsa<5,>=3.1.4 in /usr/local/lib/python3.12/dist-packages (from google-auth<3.0.0,>=2.14.1->google-genai) (4.9.1)\n",
            "Requirement already satisfied: httpcore==1.* in /usr/local/lib/python3.12/dist-packages (from httpx<1.0.0,>=0.28.1->google-genai) (1.0.9)\n",
            "Requirement already satisfied: h11>=0.16 in /usr/local/lib/python3.12/dist-packages (from httpcore==1.*->httpx<1.0.0,>=0.28.1->google-genai) (0.16.0)\n",
            "Requirement already satisfied: annotated-types>=0.6.0 in /usr/local/lib/python3.12/dist-packages (from pydantic<3.0.0,>=2.0.0->google-genai) (0.7.0)\n",
            "Requirement already satisfied: pydantic-core==2.33.2 in /usr/local/lib/python3.12/dist-packages (from pydantic<3.0.0,>=2.0.0->google-genai) (2.33.2)\n",
            "Requirement already satisfied: typing-inspection>=0.4.0 in /usr/local/lib/python3.12/dist-packages (from pydantic<3.0.0,>=2.0.0->google-genai) (0.4.2)\n",
            "Requirement already satisfied: pyasn1<0.7.0,>=0.6.1 in /usr/local/lib/python3.12/dist-packages (from pyasn1-modules>=0.2.1->google-auth<3.0.0,>=2.14.1->google-genai) (0.6.1)\n"
          ]
        }
      ],
      "source": [
        "!pip install --upgrade google-genai pillow requests\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import os\n",
        "import base64\n",
        "import re\n",
        "import textwrap\n",
        "import requests\n",
        "from PIL import Image, ImageDraw, ImageFont\n",
        "from IPython.display import display\n",
        "from google import genai\n",
        "from google.genai import types\n",
        "\n",
        "# Set your API key (replace with your actual key)\n",
        "os.environ[\"GOOGLE_CLOUD_API_KEY\"] = \"YOUR_API_KEY\"\n",
        "\n",
        "# Create the client\n",
        "client = genai.Client(vertexai=True, api_key=os.environ[\"GOOGLE_CLOUD_API_KEY\"])\n"
      ],
      "metadata": {
        "id": "gtQa3vbeGlOE"
      },
      "execution_count": 12,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "!wget -q -O /content/Bangers-Regular.ttf https://github.com/google/fonts/raw/main/ofl/bangers/Bangers-Regular.ttf\n",
        "!wget -q -O /content/Montserrat-SemiBold.ttf https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-SemiBold.ttf\n",
        "\n",
        "FONT_BANGERS = \"/content/Bangers-Regular.ttf\"\n",
        "FONT_MONTSERRAT = \"/content/Montserrat-SemiBold.ttf\"\n"
      ],
      "metadata": {
        "id": "GRl2woCgGqcn"
      },
      "execution_count": 13,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def draw_text_on_image(img, text, font_path=FONT_BANGERS, position='bottom', padding=40):\n",
        "    img = img.convert(\"RGBA\")\n",
        "    W, H = img.size\n",
        "    draw = ImageDraw.Draw(img)\n",
        "\n",
        "    font_size = max(18, int(W / 15))\n",
        "    font = ImageFont.truetype(font_path, font_size)\n",
        "\n",
        "    # Compute wrapped text width/height using Pillow >=10\n",
        "    avg_char_w = sum((font.getbbox(c)[2] - font.getbbox(c)[0]) for c in \"abcdefghijklmnopqrstuvwxyz\") / 26.0\n",
        "    max_chars = max(10, int((W * 0.9) / max(1, avg_char_w)))\n",
        "    wrapped = textwrap.fill(text, width=max_chars)\n",
        "\n",
        "    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font)\n",
        "    tw = bbox[2] - bbox[0]\n",
        "    th = bbox[3] - bbox[1]\n",
        "\n",
        "    x = (W - tw) / 2\n",
        "    y = (H - th - padding) if position == 'bottom' else padding\n",
        "\n",
        "    stroke = max(2, int(font_size * 0.06))\n",
        "    for dx in range(-stroke, stroke + 1):\n",
        "        for dy in range(-stroke, stroke + 1):\n",
        "            if dx == 0 and dy == 0:\n",
        "                continue\n",
        "            draw.multiline_text((x+dx, y+dy), wrapped, font=font, fill=(0,0,0,200), align='center')\n",
        "    draw.multiline_text((x, y), wrapped, font=font, fill=(255,255,255,255), align='center')\n",
        "    return img.convert(\"RGB\")\n"
      ],
      "metadata": {
        "id": "ys_XDEzeGvKk"
      },
      "execution_count": 14,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def generate_captions(keywords, n=3):\n",
        "    # Fallback captions if AI model is unavailable\n",
        "    fallback = [\n",
        "        \"Fun times at the college fest!\",\n",
        "        \"Music, food, and laughter all around!\",\n",
        "        \"Friends + Vibes = Memories!\"\n",
        "    ][:n]\n",
        "\n",
        "    # Only generate if your API key supports Gemini text models\n",
        "    model_name = \"gemini-2.5-flash-image-preview\"  # replace if you have access\n",
        "\n",
        "    prompt = f\"Generate {n} short, fun captions (1-2 lines each) for: {keywords}\"\n",
        "\n",
        "    try:\n",
        "        contents = [types.Content(role=\"user\", parts=[prompt])]\n",
        "        config = types.GenerateContentConfig(\n",
        "            temperature=1,\n",
        "            top_p=0.95,\n",
        "            max_output_tokens=1024,\n",
        "            response_modalities=[\"TEXT\", \"IMAGE\"],\n",
        "        )\n",
        "        resp = client.models.generate_content(model=model_name, contents=contents, config=config)\n",
        "        text = getattr(resp, \"text\", \"\")\n",
        "        lines = [re.sub(r'^[\\-\\d\\.\\)\\s]+', '', ln).strip() for ln in text.splitlines() if ln.strip()]\n",
        "        if not lines:\n",
        "            return fallback\n",
        "        return lines[:n]\n",
        "    except Exception as e:\n",
        "        print(\"Error generating AI captions:\", e)\n",
        "        return fallback\n"
      ],
      "metadata": {
        "id": "AJ_KgNA6G4Cv"
      },
      "execution_count": 15,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def create_meme_from_image(img, keywords, style='meme'):\n",
        "    captions = generate_captions(keywords)\n",
        "    chosen_caption = captions[0] if captions else keywords\n",
        "    font_path = FONT_BANGERS if style=='meme' else FONT_MONTSERRAT\n",
        "    position = 'bottom' if style=='meme' else 'top'\n",
        "    out_img = draw_text_on_image(img.copy(), chosen_caption, font_path=font_path, position=position)\n",
        "    return out_img, captions\n"
      ],
      "metadata": {
        "id": "-yAVMwdPG_9K"
      },
      "execution_count": 16,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def generate_captions(keywords, n=3):\n",
        "    # Fallback captions\n",
        "    fallback = [\n",
        "        \"Fun times at the college fest!\",\n",
        "        \"Music, food, and laughter all around!\",\n",
        "        \"Friends + Vibes = Memories!\"\n",
        "    ][:n]\n",
        "\n",
        "    # Only generate if API key has access\n",
        "    model_name = \"gemini-2.5-flash-image-preview\"  # replace if you have access\n",
        "\n",
        "    prompt_text = f\"Generate {n} short, fun captions (1-2 lines each) for: {keywords}\"\n",
        "\n",
        "    try:\n",
        "        contents = [\n",
        "            types.Content(\n",
        "                role=\"user\",\n",
        "                parts=[prompt_text]   # just plain string\n",
        "            )\n",
        "        ]\n",
        "        config = types.GenerateContentConfig(\n",
        "            temperature=1,\n",
        "            top_p=0.95,\n",
        "            max_output_tokens=1024,\n",
        "            response_modalities=[\"TEXT\", \"IMAGE\"],\n",
        "        )\n",
        "        resp = client.models.generate_content(\n",
        "            model=model_name,\n",
        "            contents=contents,\n",
        "            config=config\n",
        "        )\n",
        "\n",
        "        text = getattr(resp, \"text\", \"\")\n",
        "        lines = [re.sub(r'^[\\-\\d\\.\\)\\s]+', '', ln).strip() for ln in text.splitlines() if ln.strip()]\n",
        "        if not lines:\n",
        "            return fallback\n",
        "        return lines[:n]\n",
        "\n",
        "    except Exception as e:\n",
        "        print(\"Error generating AI captions:\", e)\n",
        "        return fallback\n"
      ],
      "metadata": {
        "id": "zuJcTbViHFkp"
      },
      "execution_count": 19,
      "outputs": []
    }
  ]
}