from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
import logging

from .models import DealershipReview, Dealership

logger = logging.getLogger(__name__)


def _recalculate_dealership_rating(dealership_id):
    try:
        dealership = Dealership.objects.get(id=dealership_id)
        avg = dealership.reviews.aggregate(Avg('rating'))['rating__avg']
        # If there are no reviews, don't overwrite any admin-set rating
        if avg is None:
            return
        normalized = round(float(avg), 1)
        if dealership.rating != normalized:
            dealership.rating = normalized
            dealership.save(update_fields=['rating'])
    except Dealership.DoesNotExist:
        logger.warning('Dealership %s not found while recalculating rating', dealership_id)
    except Exception:
        logger.exception('Failed to recalculate rating for dealership %s', dealership_id)


@receiver(post_save, sender=DealershipReview)
def dealership_review_saved(sender, instance, **kwargs):
    # When a review is created or updated, recalc rating
    if instance.dealership_id:
        _recalculate_dealership_rating(instance.dealership_id)


@receiver(post_delete, sender=DealershipReview)
def dealership_review_deleted(sender, instance, **kwargs):
    # When a review is deleted, recalc rating
    if instance.dealership_id:
        _recalculate_dealership_rating(instance.dealership_id)
