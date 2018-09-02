from django.conf.urls import url

from oscar.apps.promotions.app import PromotionsApplication as CorePromotionAplication
from oscar.core.loading import get_class


class PromotionsApplication(CorePromotionAplication):

    def get_urls(self):
        urls = super(PromotionsApplication, self).get_urls()        
        return self.post_process_urls(urls)

        
application = PromotionsApplication()
