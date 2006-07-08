
from twisted.trial.unittest import TestCase

from nevow.athena import LivePage
from nevow.context import WovenContext
from nevow.testutil import FakeRequest
from nevow.loaders import stan
from nevow.tags import html, head, body, directive
from nevow.inevow import IRequest

from axiom.store import Store
from axiom.userbase import LoginSystem

from xmantissa.webadmin import (
    LocalUserBrowser, UserInteractionFragment, EndowDepriveFragment)

class UserInteractionFragmentTestCase(TestCase):
    def setUp(self):
        """
        Create a site store and a user store with a L{LocalUserBrowser}
        installed on it.
        """
        self.sitedir = self.mktemp()
        self.siteStore = Store(self.sitedir)
        self.loginSystem = LoginSystem(store=self.siteStore)
        self.loginSystem.installOn(self.siteStore)

        self.userStore = Store()
        self.userStore.parent = self.siteStore
        self.browser = LocalUserBrowser(store=self.userStore)


    def test_createUser(self):
        """
        Test that L{webadmin.UserInteractionFragment.createUser} method
        actually creates a user.
        """
        userInteractionFragment = UserInteractionFragment(self.browser)
        userInteractionFragment.createUser(
            u'testuser', u'localhost', u'password')

        account = self.loginSystem.accountByAddress(u'testuser', u'localhost')
        self.assertEquals(account.password, u'password')


    def test_rendering(self):
        """
        Test that L{webadmin.UserInteractionFragment} renders without raising
        any exceptions.
        """
        f = UserInteractionFragment(self.browser)

        p = LivePage(
            docFactory=stan(
                html[
                    head(render=directive('liveglue')),
                    body(render=lambda ctx, data: f)]))
        f.setFragmentParent(p)

        ctx = WovenContext()
        req = FakeRequest()
        ctx.remember(req, IRequest)

        d = p.renderHTTP(ctx)
        def rendered(ign):
            p.action_close(None)
        d.addCallback(rendered)
        return d



class EndowDepriveTestCase(TestCase):
    def test_rendering(self):
        sitedir = self.mktemp()
        siteStore = Store(sitedir)

        loginSystem = LoginSystem(store=siteStore)
        loginSystem.installOn(siteStore)

        account = loginSystem.addAccount(u'testuser', u'localhost', None)

        f = EndowDepriveFragment(None, u'testuser', account, 'endow')

        p = LivePage(
            docFactory=stan(
                html[
                    head(render=directive('liveglue')),
                    body(render=lambda ctx, data: f)]))
        f.setFragmentParent(p)

        ctx = WovenContext()
        req = FakeRequest()
        ctx.remember(req, IRequest)

        d = p.renderHTTP(ctx)
        def rendered(ign):
            p.action_close(None)
        d.addCallback(rendered)
        return d