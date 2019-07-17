from uceasy.adapters import assembly
from uceasy.adapters import quality_control
from uceasy.controller import env_manager


class Facade:


    def __init__(self, context):
        self.__context = context


    def quality_control(self):

        config_dict = env_manager.prepare_illumiprocessor_conf(self.__context.sheet,
                                                               self.__context.adapter_i7,
                                                               self.__context.adapter_i5)

        config = env_manager.render_conf_file(self.__context.output + '/illumiprocessor.conf', config_dict)

        return quality_control.run_illumiprocessor(config, self.__context.input,
                                                   self.__context.output + '/illumiprocessor')


    def assembly(self):
        config_dict = env_manager.prepare_assembly_conf(self.__context)
        config = env_manager.render_conf_file(self.__context.output + '/assembly.conf', config_dict)

        return assembly.run_trinity(config, self.__context.output + '/assembly')


    def process_uce(self):
        pass
