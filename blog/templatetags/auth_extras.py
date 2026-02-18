from django import template

register = template.Library()


@register.filter
def has_any_group(user, group_names):
    groups = [g.strip() for g in group_names.split(",")]
    return user.groups.filter(name__in=groups).exists()
