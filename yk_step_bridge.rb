# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

require 'sketchup.rb'
require 'extensions.rb'
module YKStepBridge
  unless file_loaded?(__FILE__)
    extension = SketchupExtension.new('FreeCAD Bridge', 'yk_step_bridge/main')
    extension.description = 'Importação STEP para SketchUp com componentes nomeados, cores disponíveis no arquivo, limpeza de faces planas, suavização de curvas, reparo automático e validação de sólidos. Utiliza o FreeCAD em segundo plano.'
    extension.version = '0.4.1'
    extension.copyright = 'Copyright © 2026 Yruam Kaffer de Faria. PolyForm Noncommercial 1.0.0.'
    extension.creator = 'Yruam Kaffer de Faria'
    Sketchup.register_extension(extension, true)
    file_loaded(__FILE__)
  end
end
