def updatePages():
    from .models import EnterpriseFormPage

    for page in EnterpriseFormPage.objects.all():
        page.generate()
