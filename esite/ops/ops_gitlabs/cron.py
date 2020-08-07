def run_analysis():
    print("test")
    from .models import Gitlab
    from ..ops_scpages.services import updatePages

    # for i in Gitlab.objects.all():
    #     i.analyse_gitlab()

    updatePages()
