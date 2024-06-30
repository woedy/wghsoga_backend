from django.contrib import admin

from projects.models import ProjectSupporter, ProjectImage, Project, ProjectVideo

admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(ProjectVideo)
admin.site.register(ProjectSupporter)
