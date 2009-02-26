# -*- coding: utf-8 -*-
#
#  Copyright (c) 2008 The Django Brasil Community Website Authors
#
#  This file is part of Django Brasil Project Site.
#
#  Django Brasil Project is free software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3 of
#  the License, or (at your option) any later version.
#
#  Django Brasil Project is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the implied warranty
#  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import twitter
import urllib, urllib2
from django.conf import settings

def post_to_twitter(sender, instance, *args, **kwargs):
    """
    Post new saved objects to Twitter.
    """

    # avoid to post the same object twice
    if not kwargs.get('created'):
        return False

    # check if there's a twitter account configured
    try:
        username = settings.TWITTER_USERNAME
        password = settings.TWITTER_PASSWORD
    except AttributeError:
        print 'WARNING: Twitter account not configured.'
        return False
    
    # tinyurl'ze the object's link
    create_api = 'http://tinyurl.com/api-create.php'
    data = urllib.urlencode(dict(url=instance.get_absolute_url()))
    link = urllib2.urlopen(create_api, data=data).read().strip()

    # create the twitter message
    text = str(instance).decode('utf-8')
    mesg = '%s - %s' % (text, link)
    if len(mesg) > settings.TWITTER_MAXLENGTH:
        size = len(mesg + '...') - settings.TWITTER_MAXLENGTH
        mesg = '%s... - %s' % (text[:-size], link)

    try:
        twitter_api = twitter.Api(username, password)
        twitter_api.PostUpdate(twitter_msg)
    except urllib2.HTTPError, ex:
        print 'ERROR:', str(ex)
        return False