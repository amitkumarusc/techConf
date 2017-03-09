from ..models.tag import Tag
from ..models.slackinfo import SlackInfo


def parse_user_choice(user_response):
    if user_response['callback_id'] == 'tech_subs':
        tag_name = user_response['actions'][0]['value']
        if tag_name == 'not_interested':
            print "User responded as Not Interested"
            return
        channel_text_id = user_response['channel']['id']
        channel_id = SlackInfo.query.filter_by(channel_id=channel_text_id).first().id
        tag = Tag(tag_name, channel_id)
        tag.save()
    else:
        print "Some new category questions are being asked from user. Add the handling here also"
