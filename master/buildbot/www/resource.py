# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from twisted.web import resource

class Resource(resource.Resource):

    # as a convenience, subclasses have a ``master`` attribute, a
    # ``base_url`` attribute giving Buildbot's base URL,
    # and ``static_url`` attribute giving Buildbot's static files URL

    @property
    def base_url(self):
        return self.master.config.www['url']

    @property
    def static_url(self):
        """if static_url is not defined, then, we will server
        the static files via twisted static resource handler."""
        key = 'static_url'
        if self.master.config.www.has_key(key):
            return self.master.config.www[key]
        return self.base_url + "static"

    @property
    def extra_routes(self):
        return self.master.config.www['extra_routes']

    def __init__(self, master):
        resource.Resource.__init__(self)
        self.master = master

class RedirectResource(Resource):

    def __init__(self, master, basepath):
        Resource.__init__(self, master)
        self.basepath = basepath

    def render(self, request):
        redir = self.base_url + self.basepath
        request.redirect(redir)
        return redir
