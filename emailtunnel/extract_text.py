from . import html2text


def html_to_plain(body):
    # From regnskab.utils
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.unicode_snob = True
    h.images_to_alt = True
    h.body_width = 0
    return h.handle(str(body))


def get_body_text(message):
    text_parts = [
        part for part in message.walk() if part.get_content_maintype() == "text"
    ]
    if not text_parts:
        raise Exception("Message has no text parts")
    plain_parts = [part for part in text_parts if part.get_content_subtype() == "plain"]
    if plain_parts:
        text_part = plain_parts[0]
    else:
        text_part = text_parts[0]
    payload_bytes = text_part.get_payload(decode=True)
    charset = text_part.get_content_charset("utf8")
    try:
        payload = payload_bytes.decode(charset, errors="replace")
    except Exception:
        raise Exception("Failed to decode as %r" % (charset,))
    if text_part.get_content_subtype() == "html":
        payload = html_to_plain(payload)
    return payload
