def run_analysis():
    from .models import Gitlab
    from ..ops_enterprise.services import updatePages

    # analyse all gitlabs
    for i in Gitlab.objects.all():
        i.analyse_gitlab()

    # update enterprise pages
    updatePages()
