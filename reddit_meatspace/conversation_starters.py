from pylons.i18n import _

from r2.models import Subreddit


TOPICS = {}


def conversation_starter(title):
    def conversation_starter_decorator(fn):
        TOPICS[fn.__name__] = fn
        fn.title = title
        return fn
    return conversation_starter_decorator


@conversation_starter(_("april fools' team"))
def f2p_team(user):
    return "orangered" if user._id % 2 == 0 else "periwinkle"


@conversation_starter(_("most active in"))
def top_sr(user):
    all_karmas = user.all_karmas()
    if not all_karmas:
        return _("lurker")
    top_sr = all_karmas[0]
    return "/r/" + top_sr[0]


@conversation_starter(_("snoo-o-logical sign"))
def zodiac(user):
    zodiac_signs = [
        _("capricorn"),
        _("aquarius"),
        _("pisces"),
        _("aries"),
        _("taurus"),
        _("gemini"),
        _("cancer"),
        _("leo"),
        _("virgo"),
        _("libra"),
        _("scorpio"),
        _("sagittarius"),
    ]
    return zodiac_signs[user._date.month % 12]


@conversation_starter(_("most obscure"))
def obscure(user):
    all_karmas = user.all_karmas()
    if not all_karmas:
        return _("lurker")
    srnames = [x[0] for x in all_karmas]
    srs = [sr for sr in Subreddit._by_name(srnames).values()
           if sr.type in ("public", "restricted")]
    if not srs:
        return _("something secret")
    srs.sort(key=lambda sr: sr._downs)
    most_obscure = srs[0]
    return "/r/" + most_obscure.name
