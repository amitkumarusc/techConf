from ..models.tag import Tag
from ..models.channel import Channel
import json
from flask import Response


def parse_user_choice(user_response):
    if user_response['callback_id'] == 'tech_subs':
        tag_name = user_response['actions'][0]['value']
        if tag_name == 'not_interested':
            print "User responded as Not Interested"
            return
        channel_text_id = user_response['channel']['id']
        channel = Channel.query.filter_by(channel_id=channel_text_id).first()
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:
            tag = Tag(tag_name)
        tag.channels.append(channel)
        tag.save()
    else:
        print "Some new category questions are being asked from user. Add the handling here also"

    resp = {'text': 'Your response has been recorded', 'replace_original': True, 'response_type': 'ephemeral'}
    js = json.dumps(resp)
    return Response(js, status=200, mimetype='application/json')
