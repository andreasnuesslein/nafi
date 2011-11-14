from django.shortcuts import render_to_response as _render_to_response
from django.template import RequestContext


def render_to_response(request, template, context={}):
    return _render_to_response(template,
        context_instance = RequestContext(request, context))

