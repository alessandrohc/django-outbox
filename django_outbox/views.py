from django.views.generic import TemplateView
from django.http import HttpResponse
import base64
from .outbox import Outbox


class OutboxTemplateView(TemplateView):
    template_name = 'django_outbox/outbox.html'

    def get_context_data(self, **kwargs):
        context = super(OutboxTemplateView, self).get_context_data(**kwargs)
        context['mails'] = Outbox().all()
        return context


class MailTemplateView(TemplateView):
    template_name = 'django_outbox/mail.html'

    def render_to_response(self, context, **kwargs):
        contenttype = context['content_type']
        if contenttype == "text/html" or contenttype == "text/plain":
            return super(MailTemplateView, self).render_to_response(context, **kwargs)
        return HttpResponse(base64.b64decode(context['mail'].body[contenttype]), content_type=contenttype)

    def get_context_data(self, id, **kwargs):
        context = super(MailTemplateView, self).get_context_data(**kwargs)
        mail = Outbox().get(id)
        context['mail'] = mail
        context['content_type'] = self.request.GET['content_type']
        context['content'] = mail.body[self.request.GET['content_type']]

        return context
