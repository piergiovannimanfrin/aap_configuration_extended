#!/usr/bin/python

from ansible.errors import AnsibleFilterError
from ansible.module_utils._text import to_native

class FilterModule(object):
 
    def filters(self):
        return {
            'surveys_cleanup': self.surveys_cleanup
        }
 
    def surveys_cleanup(self, controller_templates):

        if not isinstance(controller_templates, list):
            raise AnsibleFilterError("Input value must be a list")
        
        try:
            for template in controller_templates:
                if "survey_spec" in template:
                    for question in template["survey_spec"]["spec"]:
                        if question.get("type") not in ("integer", "float"):
                            if "default" in question:
                                question["default"] = str(question["default"])
                        if "choices" in question:
                            question["choices"] = [str(x) for x in question["choices"]]

            return controller_templates

        except Exception as e:
            raise AnsibleFilterError("Failed! Original exception was: %s" % to_native(e))
