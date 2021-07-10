from django.db import models

class TestCaseManager(models.Manager):
    def insert_case(self, belong_module, **kwargs):
        case_info = kwargs.get('test').pop('case_info')
        self.create(name=kwargs.get('test').get('name'), belong_project=case_info.pop('project'),
                    belong_module=belong_module,
                    author=case_info.pop('author'), include=case_info.pop('include'), request=kwargs)

    def update_case(self, belong_module, **kwargs):
        case_info = kwargs.get('test').pop('case_info')
        obj = self.get(id=case_info.pop('test_index'))
        obj.belong_project = case_info.pop('project')
        obj.belong_module = belong_module
        obj.name = kwargs.get('test').get('name')
        obj.author = case_info.pop('author')
        obj.include = case_info.pop('include')
        obj.request = kwargs
        obj.save()

    def get_case_name(self, name, module_name, belong_project):
        return self.filter(belong_module__id=module_name).filter(name__exact=name).filter(
            belong_project__exact=belong_project).count()