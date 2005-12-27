from nevow import rend, livepage, athena, tags

from xmantissa.webtheme import getLoader, getAllThemes

class PublicPageMixin(object):
    fragment = None
    title = ''
    username = None

    def render_navigation(self, ctx, data):
        return ""

    def render_search(self, ctx, data):
        return ""

    def render_title(self, ctx, data):
        return ctx.tag[self.title]

    def render_username(self, ctx, data):
        if self.username is not None:
            return ctx.tag.fillSlots('username', self.username)
        return ctx.tag.clear()[tags.a(href='/login')['Sign in']]

    def render_header(self, ctx, data):
        if self.staticContent is None:
            return ctx.tag

        header = self.staticContent.getHeader()
        if header is not None:
            return ctx.tag[header]
        else:
            return ctx.tag

    def render_footer(self, ctx, data):
        if self.staticContent is None:
            return ctx.tag

        header = self.staticContent.getFooter()
        if header is not None:
            return ctx.tag[header]
        else:
            return ctx.tag

    def render_content(self, ctx, data):
        return ctx.tag[self.fragment]

    def head(self):
        return None

    def render_head(self, ctx, data):
        content = list(t.head() for t in getAllThemes())
        content.append(self.head())
        return ctx.tag[filter(None, content)]

class PublicPage(PublicPageMixin, rend.Page):
    def __init__(self, original, fragment, staticContent, forUser):
        super(PublicPage, self).__init__(original, docFactory=getLoader("public-shell"))
        self.fragment = fragment
        self.staticContent = staticContent
        if forUser is not None:
            assert isinstance(forUser, unicode), forUser
        self.username = forUser

class PublicLivePage(PublicPageMixin, livepage.LivePage):
    def __init__(self, original, fragment, staticContent, forUser):
        super(PublicLivePage, self).__init__(original, docFactory=getLoader("public-shell"))
        self.fragment = fragment
        self.staticContent = staticContent
        if forUser is not None:
            assert isinstance(forUser, unicode), forUser
        self.username = forUser

    def render_head(self, ctx, data):
        tag = super(PublicLivePage, self).render_head(ctx, data)
        return tag[livepage.glue]

class PublicAthenaLivePage(PublicPageMixin, athena.LivePage):
    def __init__(self, iface, original, fragment, staticContent, forUser):
        super(PublicAthenaLivePage, self).__init__(iface, original, docFactory=getLoader("public-shell"))
        self.fragment = fragment
        self.staticContent = staticContent
        if forUser is not None:
            assert isinstance(forUser, unicode), forUser
        self.username = forUser

    def render_head(self, ctx, data):
        tag = PublicPageMixin.render_head(self, ctx, data)
        return tag[tags.directive('liveglue')]
