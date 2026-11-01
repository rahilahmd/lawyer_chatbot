from django.shortcuts import render

import openai
api_key="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"
openai.api_key = api_key
# Create your views here.
# def chatbot(request):
#     context = {
#         'res': ""
#     }
#     if request.method == "POST":
#             chat=request.POST.get('Chatbot')
#             res=chat_with_gpt(chat)
#             context={
#                 'res':res
#             }
#     return render(request,'chatbot/Chatbot.html',context)
#
#
# def chat_with_gpt(prompt):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" for a lighter model
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=2000,  # Limit the length of the response
#             temperature=0.7,  # Controls creativity (0-1)
#         )
#         return response['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         return f"An error occurred: {e}"
#

#web chabot
# from django.shortcuts import render
# from datetime import date
# from .models import Chatbot
# import openai
#
#
# def chatbot(request):
#     user_id = request.session['uid']  # replace with request.user.id if auth is enabled
#
#     if request.method == "POST":
#         chat = request.POST.get('Chatbot')
#         res = chat_with_gpt(chat)
#
#         # SAVE TO DATABASE
#         Chatbot.objects.create(
#             message=chat,
#             replay=res,
#             date=date.today(),
#             user_id=user_id
#         )
#
#     # FETCH CHAT HISTORY
#     chats = Chatbot.objects.filter(user_id=user_id).order_by('chatbot_id')
#
#     context = {
#         'chats': chats
#     }
#
#     return render(request, 'chatbot/Chatbot.html', context)
#
#
# def chat_with_gpt(prompt):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=200,
#             temperature=0.7,
#         )
#
#         return response['choices'][0]['message']['content'].strip()
#
#     except Exception as e:
#         return f"Error: {e}"
import os
from django.utils import timezone

import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Chatbot

# Works on Python 3.7. No "openai" or "anthropic" package is needed, only:
#   python3 -m pip install requests
#
# Put your key in settings.py (the file next to urls.py) like this:
#   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-5-5"     # if the terminal shows a 404 "model not found", use the name from your Anthropic console

SYSTEM_PROMPT = """You are the legal assistant inside Advocate.NOW, a platform that connects people with lawyers.
Users are mainly in India, so default to Indian law (for example the Motor Vehicles Act, the Bharatiya Nyaya Sanhita and
the Bharatiya Nagarik Suraksha Sanhita). If the user's facts point to another jurisdiction, say so and adapt.

You help with: checking case details, the pros and cons of a case, explaining challans and police fines, and general
legal questions.

Style: plain, calm language a non-lawyer can follow. Use short headings and bullet points. Keep answers focused.

Rules:
- Give general legal information, not personal legal advice. Never claim to be a lawyer.
- Do not invent case numbers, case-law citations, section numbers or fine amounts. If you are not sure, say so.
- For serious matters (arrest, criminal charges, court summons, large money claims, family disputes), recommend
  speaking to a licensed lawyer and mention they can book one on Advocate.NOW.
- If the message is not about law, police, courts or fines, politely steer back to what you can help with.
"""

ERROR_PREFIX = "Error:"


def chatbot(request):
    user_id = request.session['uid']  # replace with request.user.id if auth is enabled

    if request.method == "POST":
        chat = (request.POST.get('Chatbot') or "").strip()

        if chat:
            res = chat_with_ai(chat, user_id)

            # SAVE TO DATABASE
            Chatbot.objects.create(
                message=chat,
                replay=res,
                date=timezone.now(),
                user_id=user_id
            )

        # Redirect so that refreshing the page does not send the message again
        return HttpResponseRedirect(request.path)

    # FETCH CHAT HISTORY
    chats = Chatbot.objects.filter(user_id=user_id).order_by('chatbot_id')

    context = {
        'chats': chats
    }

    return render(request, 'chatbot/Chatbot.html', context)


def chat_with_ai(prompt, user_id):
    api_key = getattr(settings, "ANTHROPIC_API_KEY", None) or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return ERROR_PREFIX + " the assistant is not set up yet (missing API key)."

    # Give the assistant the last few saved turns so it remembers the conversation
    messages = []
    recent = Chatbot.objects.filter(user_id=user_id).order_by('-chatbot_id')[:6]
    for c in reversed(list(recent)):
        if c.message and c.replay and not c.replay.startswith(ERROR_PREFIX):
            messages.append({"role": "user", "content": c.message})
            messages.append({"role": "assistant", "content": c.replay})
    messages.append({"role": "user", "content": prompt[:4000]})

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": MODEL,
        "max_tokens": 1200,
        "system": SYSTEM_PROMPT,
        "messages": messages,
    }

    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=90)
    except requests.RequestException:
        return ERROR_PREFIX + " could not reach the assistant. Check your internet connection."

    if r.status_code != 200:
        print("Anthropic API error", r.status_code, r.text[:500])   # also shown in your terminal

        try:
            detail = r.json().get("error", {}).get("message", "")[:200]
        except ValueError:
            detail = ""

        hints = {
            401: "your API key was rejected. Create a new key on the API Keys page of console.anthropic.com and put it in settings.py.",
            403: "this key is not allowed to use the API. Create a new key on the API Keys page.",
            404: "the model name was not accepted. Change MODEL at the top of views.py to the name shown in your Anthropic console.",
            429: "too many requests. Wait a minute and try again.",
        }
        hint = hints.get(r.status_code, "the service had a problem. Try again in a moment.")
        if r.status_code == 400 and "credit" in detail.lower():
            hint = "your account has no credit. Add credit under Billing in console.anthropic.com."
        return ERROR_PREFIX + " (code %s) %s" % (r.status_code, hint)

    blocks = r.json().get("content", [])
    reply = "".join(b.get("text", "") for b in blocks if b.get("type") == "text").strip()
    return reply or (ERROR_PREFIX + " no answer was produced. Please try again.")