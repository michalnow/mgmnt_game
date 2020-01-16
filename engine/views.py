# -*- coding: UTF-8 -*-

from json import loads

from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView

from process.models import Round, Game
from .tools.game_engine import GameEngine, RoundEngine

class PostTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest('Bad GET request!')

    def post(self, request, *args, **kwargs):
        p = dict(request.POST)
        for key in p.keys():
            if type(p[key]) is list:
                if key.startswith("fields"):
                    continue
                p[key] = p[key][0]
        self.post = p

        context = self.get_context_data()
        rendered = self.render_to_response(context)
        return rendered


class InitGame(PostTemplateView):
    # this class creates game object and round 1
    template_name = "game/init_game.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ge = GameEngine()
        context['game'] = ge.init_game(self.request.user)
        context['game_id'] = context['game'].id

        re = RoundEngine(context['game'])
        r = re.init_round()
        context['round'] = r
        context['round_data'] = loads(r.possibilities)
        context['round_iterator'] = list(range(context['round_data']['projekty']))

        return context


class RoundSubmit(PostTemplateView):
    # this class is finishing the round
    template_name = "game/submit_round.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        rd = Round.objects.get(pk=self.post['roundId'])
        context['round'] = rd
        context['round_data'] = loads(rd.possibilities)
        context['round_iterator'] = list(range(context['round_data']['projekty']))
        context['game_id'] = rd.game_id

        self.add_checkboxes_to_context(context)

        return context

    def add_checkboxes_to_context(self, context):
        checkboxes = []
        for itr in range(context['round_data']['projekty']):
            name = str(itr)
            if name in self.post['fields[]']:
                checkboxes.append(" checked")
            else:
                checkboxes.append(" ")

        context['checkboxes'] = checkboxes

        return context


class InitRound(PostTemplateView):
    # this class creates round to known game
    template_name = "game/init_round.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        g = Game.objects.get(id=self.post['gameId'])
        context['game'] = g
        context['game_id'] = g.id

        re = RoundEngine(context['game'])
        r = re.init_round()
        context['round'] = r
        context['round_data'] = loads(r.possibilities)
        context['round_iterator'] = list(range(context['round_data']['projekty']))

        return context

class ProjectView(PostTemplateView):
    # this class creates single project plot
    template_name = "game/project_plot.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class WalletAnalysisView(PostTemplateView):
    # this class is plotting wallet analysis
    template_name = "game/wallet_plot.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
