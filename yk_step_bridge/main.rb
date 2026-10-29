# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

require 'json'
require 'tmpdir'
require 'fileutils'
require 'cgi'
module YKStepBridge
  def self.import_json(path = nil)
    path ||= UI.openpanel('Importar geometria FreeCAD', nil, 'JSON|*.json||')
    return unless path
    data = JSON.parse(File.read(path, encoding: 'UTF-8'))
    raise 'Formato incompatível' unless data['format'] == 'yk-step-bridge-1' && data['units'] == 'mm'
    parts = data.fetch('parts')
    raise 'Arquivo sem peças' if parts.empty?
    # Validate before touching the model.
    parts.each do |part|
      vertices = part.fetch('vertices')
      if data['strict'] && (part['geometry_type'] == 'surface' || part['cad_has_solid'] == false || part['cad_valid'] == false || part['mesh_closed'] == false)
        raise "#{part['name'] || 'Peça'}: não aprovada para importação estrita. Use Visualização para inspecionar."
      end
      colors = part['triangle_colors']
      raise 'Quantidade de cores incompatível' if colors && colors.size != part.fetch('triangles').size
      ([part['color']] + (colors || [])).compact.each do |color|
        raise 'Cor inválida' unless color.size == 3 && color.all? { |n| n.is_a?(Numeric) && n.finite? && n.between?(0, 255) }
      end
      raise 'Vértices inválidos' unless vertices.all? { |v| v.size == 3 && v.all? { |n| n.is_a?(Numeric) && n.finite? } }
      raise 'Triângulos inválidos' unless part.fetch('triangles').all? { |t| t.size == 3 && t.uniq.size == 3 && t.all? { |i| i.is_a?(Integer) && i >= 0 && i < vertices.size } }
    end
    model = Sketchup.active_model
    model.start_operation('Importar FreeCAD', true)
    started = true
    report = []
    imported = []
    material_cache = {}
    container = parts.size > 1 ? model.active_entities.add_group : nil
    container.name = File.basename(data['source'].to_s, '.step') if container
    target = container ? container.entities : model.active_entities
    parts.each do |part|
      group = target.add_group
      group.name = part['name'] || 'Peça FreeCAD'
      mesh = Geom::PolygonMesh.new
      # Build large to avoid SketchUp's small-edge creation tolerance.
      indices = part['vertices'].map { |v| mesh.add_point(v.map { |n| n.to_f / 25.4 * 1000.0 }) }
      part['triangles'].each { |t| mesh.add_polygon(t.map { |i| indices[i] }) }
      group.entities.fill_from_mesh(mesh, true, 0)
      created_faces = group.entities.grep(Sketchup::Face).size
      raise "#{group.name}: falha ao criar todas as faces (#{created_faces}/#{part['triangles'].size})." unless created_faces == part['triangles'].size
      paint_part(group.entities, part, material_cache, model)
      restore = proc do
        group.entities.clear!
        group.entities.fill_from_mesh(mesh, true, 0)
        restored_faces = group.entities.grep(Sketchup::Face).size
        raise "#{group.name}: falha ao restaurar todas as faces (#{restored_faces}/#{part['triangles'].size})." unless restored_faces == part['triangles'].size
        paint_part(group.entities, part, material_cache, model)
      end
      if part['geometry_type'] == 'surface'
        # Preserve open surfaces: smoothing changes display attributes only.
        smooth_edges(group.entities)
      else
        clean_and_smooth(group, report, &restore)
      end
      group.transform!(Geom::Transformation.scaling(0.001))
      component = group.to_component
      component.definition.name = group_name = part['name'] || 'Peça FreeCAD'
      component.name = group_name
      status = part_status(component, part)
      component.name += ((part['geometry_type'] == 'surface' || part['cad_has_solid'] == false) ? ' [SUPERFÍCIE]' : ' [VERIFICAR]') unless status == 'SÓLIDO'
      component.set_attribute('YKStepBridge', 'source', data['source'].to_s)
      component.set_attribute('YKStepBridge', 'source_index', part['source_index']) if part['source_index']
      component.set_attribute('YKStepBridge', 'geometry_type', part['geometry_type'] || 'unknown')
      component.set_attribute('YKStepBridge', 'repairs', JSON.generate(part['repairs'] || []))
      imported << component
      raise "#{group_name}: o SketchUp não reconheceu como sólido. Importação estrita desfeita." if data['strict'] && !component.manifold?
      report << "#{group_name}: #{status}; #{component.definition.entities.grep(Sketchup::Face).size} faces"
      check = part['check'] || {}
      unless check.empty?
        report << "#{group_name}: bordas abertas #{check['boundary']}; arestas não manifold #{check['nonmanifold']}; vértices problemáticos #{check.fetch('nonmanifold_vertices', 'não informado')}; triângulos muito estreitos #{check.fetch('thin_triangles', 'não informado')}."
      end
      (part['repairs'] || []).each do |repair|
        operation = repair['operation'] == 'merge_near_vertices' ? 'união de vértices próximos' : 'separação local de superfícies em contato'
        limit = repair['tolerance_mm'] || repair['max_displacement_mm']
        change = repair['relative_volume_change'].to_f * 100.0
        report << "#{group_name}: #{operation}; limite #{limit} mm; variação de volume da malha #{format('%.8f', change)}%."
      end
      (part['repair_attempts'] || []).each { |message| report << "#{group_name}: #{message}" }
    end
    report.concat(data['warnings'] || [])
    model.commit_operation
    started = false
    show_report(model, imported, container, report, data)
  rescue StandardError => e
    model.abort_operation if started && model
    UI.messagebox("Falha na importação: #{e.message}")
  end

  def self.part_status(component, part)
    if part['geometry_type'] == 'surface' || part['cad_has_solid'] == false
      return component.manifold? ? 'SUPERFÍCIE — malha fechada' : 'SUPERFÍCIE ABERTA'
    end
    return 'SÓLIDO' if component.manifold? && part['mesh_closed'] != false && part['cad_valid'] != false
    'VERIFICAR'
  end
  # Keep topology edits separate from display attributes: a restored mesh
  # must receive the same smoothing as a mesh whose planar cleanup succeeded.
  def self.clean_and_smooth(group, report)
    closed_before_cleanup = group.manifold?
    group.entities.grep(Sketchup::Edge).each do |edge|
      next unless edge.valid? && edge.faces.size == 2
      a, b = edge.faces
      if a.material == b.material && a.normal.dot(b.normal) > 1.0 - 1.0e-10 && b.vertices.all? { |v| v.position.distance_to_plane(a.plane).abs < 1.0e-7 }
        edge.erase!
      end
    end
    if closed_before_cleanup && !group.manifold?
      yield
      raise 'Falha ao restaurar o fechamento do sólido' unless group.manifold?
      report << "#{group.name}: limpeza de faces revertida para preservar sólido; suavização reaplicada."
    end
    smooth_edges(group.entities)
  end

  def self.smooth_edges(entities)
    threshold = Math.cos(20.0 * Math::PI / 180.0)
    entities.grep(Sketchup::Edge).each do |edge|
      next unless edge.valid? && edge.faces.size == 2
      next unless edge.faces[0].normal.dot(edge.faces[1].normal) > threshold
      edge.soft = true
      edge.smooth = true
    end
  end

  def self.material_for(color, cache, model)
    key = color.map { |v| v.round }.join('_')
    cache[key] ||= begin
      name = "FCB_RGB_#{key}"
      mat = model.materials[name] || model.materials.add(name)
      mat.color = Sketchup::Color.new(*color.map { |v| v.round })
      mat
    end
  end

  def self.paint_part(entities, part, cache, model)
    faces = entities.grep(Sketchup::Face)
    if part['color']
      mat = material_for(part['color'], cache, model)
      faces.each { |face| face.material = mat; face.back_material = mat }
    elsif part['triangle_colors']
      colors = {}
      part['triangles'].each_with_index do |triangle, i|
        col = part['triangle_colors'][i]
        next unless col
        key = triangle.map { |v| part['vertices'][v].map { |x| x.round(6) } }.sort
        colors[key] = col
      end
      faces.each do |face|
        key = face.vertices.map { |v| v.position.to_a.map { |n| (n * 25.4 / 1000.0).round(6) } }.sort
        col = colors[key]
        next unless col
        mat = material_for(col, cache, model)
        face.material = mat
        face.back_material = mat
      end
    end
  end

  def self.show_report(model, imported, container, report, data)
    @report_dialog.close if @report_dialog
    @report_dialog = UI::HtmlDialog.new(dialog_title: 'FreeCAD Bridge — Resultado', width: 760, height: 600, resizable: true)
    escape = ->(value) { CGI.escapeHTML(value.to_s) }
    rows = imported.each_with_index.map do |component, i|
      source_index = data['parts'][i]['source_index'] || i + 1
      status = part_status(component, data['parts'][i])
      "<tr><td>#{source_index}</td><td>#{escape.call(component.name)}</td><td>#{escape.call(status)}</td><td><button onclick='sketchup.locate(#{i})'>Localizar</button></td></tr>"
    end.join
    text_report = "FreeCAD Bridge 0.5.0\nArquivo: #{data['source']}\n" + report.join("\n")
    solids = imported.each_with_index.count { |c, i| part_status(c, data['parts'][i]) == 'SÓLIDO' }
    skipped = data.fetch('skipped_parts', []).size
    html = "<!doctype html><meta charset='utf-8'><style>body{font:15px Arial;padding:20px;color:#243447}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:9px;border-bottom:1px solid #ddd}button{padding:6px 12px;cursor:pointer}pre{white-space:pre-wrap;font:12px monospace}</style><h2>FreeCAD Bridge</h2><p>#{escape.call(data['source'])} · #{imported.size} componentes · #{solids} sólidos · #{skipped} omitidas</p><table><tr><th>Índice</th><th>Componente</th><th>Resultado</th><th></th></tr>#{rows}</table><p><button onclick='sketchup.save_report()'>Salvar relatório</button></p><details><summary>Detalhes da conversão</summary><pre>#{escape.call(text_report)}</pre></details>"
    context = (model.active_path || []).dup
    context << container if container
    @report_dialog.add_action_callback('locate') do |_dialog, index|
      next unless Sketchup.active_model == model
      component = imported[index.to_i]
      next unless component && component.valid?
      model.active_path = context.empty? ? nil : context
      model.selection.clear
      model.selection.add(component)
      model.active_view.zoom(component)
    end
    @report_dialog.add_action_callback('save_report') do |_dialog|
      path = UI.savepanel('Salvar relatório', nil, 'FreeCAD_Bridge_relatorio.txt')
      File.write(path, text_report, encoding: 'UTF-8') if path
    end
    @report_dialog.set_html(html)
    @report_dialog.show
  end

  def self.config_file
    File.join(Sketchup.find_support_file('Plugins'), 'yk_step_bridge_settings.json')
  end

  def self.normalize_executable(path)
    path = path.to_s.strip.tr('\\', '/')
    path += '.exe' if !File.file?(path) && File.file?(path + '.exe')
    path
  end

  def self.saved_executable
    return @executable if @executable && File.file?(@executable)
    if File.file?(config_file)
      @executable = normalize_executable(JSON.parse(File.read(config_file))['freecadcmd'])
    else
      @executable = normalize_executable(Sketchup.read_default('YKStepBridge', 'freecadcmd', ''))
    end
    @executable
  rescue StandardError
    ''
  end

  def self.configure
    selected = UI.openpanel('Selecione FreeCADCmd.exe (pasta bin do FreeCAD)', nil, 'Executável|*.exe||')
    return nil unless selected
    path = normalize_executable(selected)
    raise "Arquivo não encontrado: #{path}" unless File.file?(path)
    raise 'Selecione FreeCADCmd.exe, não FreeCAD.exe' unless File.basename(path).downcase == 'freecadcmd.exe'
    # Use the selected value immediately, without relying on registry readback.
    @executable = path
    begin
      File.write(config_file, JSON.generate({freecadcmd: path}))
    rescue StandardError => error
      UI.messagebox("Caminho válido para esta sessão, mas não foi possível salvar: #{error.message}")
    end
    path
  rescue StandardError => e
    UI.messagebox("Configuração não concluída: #{e.message}")
    nil
  end

  def self.diagnostics
    path = saved_executable
    UI.messagebox("FreeCAD Bridge 0.5.0\nExecutável: #{path}\nExiste: #{File.file?(path)}\nConfiguração: #{config_file}")
  end

  def self.import_step
    return UI.messagebox('Já existe uma conversão em andamento.') if @job
    source = UI.openpanel('Escolha o STEP', nil, 'STEP|*.step;*.stp||')
    return unless source
    start_conversion(source, 'step')
  end

  def self.reprocess_json
    return UI.messagebox('Já existe uma conversão em andamento.') if @job
    source = UI.openpanel('Tratar JSON existente', nil, 'JSON|*.json||')
    return unless source
    start_conversion(source, 'json')
  end

  def self.start_conversion(source, input_type)
    executable = saved_executable
    executable = configure unless File.file?(executable)
    return unless executable
    raise "Executável não encontrado: #{executable}" unless File.file?(executable)
    modes = 'Estrito|Visualização|Sólidos disponíveis'
    treatments = 'Completo (até 0,001 mm)|Conservador|Sem reparos'
    if input_type == 'json'
      options = UI.inputbox(['Modo:', 'Tratamento da malha:'], ['Estrito', 'Completo (até 0,001 mm)'], [modes, treatments], 'Tratar JSON')
      return unless options
      tolerance = 0.05
      mode, treatment_label = options
    else
      options = UI.inputbox(['Desvio linear (mm; 0,001 a 100):', 'Modo:', 'Tratamento da malha:'], [0.05, 'Estrito', 'Completo (até 0,001 mm)'], ['', modes, treatments], 'Qualidade e validação')
      return unless options
      tolerance = Float(options[0])
      mode, treatment_label = options[1], options[2]
    end
    raise 'Use desvio entre 0,001 e 100 mm.' unless tolerance.between?(0.001, 100.0)
    policy = {'Estrito' => 'strict', 'Visualização' => 'visualization', 'Sólidos disponíveis' => 'solids_only'}.fetch(mode)
    treatment = {'Completo (até 0,001 mm)' => 'complete', 'Conservador' => 'conservative', 'Sem reparos' => 'none'}.fetch(treatment_label)
    directory = Dir.mktmpdir('yk-step-')
    output = File.join(directory, 'geometry.json')
    config = File.join(directory, 'job.json')
    File.write(config, JSON.generate({source: source, output: output, input_type: input_type, tolerance: tolerance, policy: policy, allow_open: policy == 'visualization', mesh_treatment: treatment, repair: treatment != 'none'}))
    log = File.join(directory, 'conversion.log')
    pid = Process.spawn({'YK_STEP_JOB' => config}, executable, File.join(__dir__, 'convert.py'), out: log, err: log, in: File::NULL)
    @job = {pid: pid, directory: directory, output: output, model: Sketchup.active_model, path: Sketchup.active_model.active_path, started: Time.now}
    Sketchup.status_text = 'Convertendo STEP com FreeCAD…'
    poll_job
  rescue StandardError => e
    FileUtils.remove_entry(directory) if directory && File.directory?(directory) && !@job
    UI.messagebox("Falha ao iniciar conversão: #{e.message}")
  end

  def self.poll_job
    UI.start_timer(0.5, false) do
      next unless @job
      begin
        job = @job
        state = Process.waitpid2(job[:pid], Process::WNOHANG)
        unless state
          if Time.now - job[:started] > 600
            Process.kill('KILL', job[:pid]) rescue nil
            Process.waitpid(job[:pid]) rescue nil
            raise 'Conversão excedeu 10 minutos.'
          end
          poll_job
          next
        end
        @job = nil
        Sketchup.status_text = ''
        error_file = job[:output] + '.error'
        raise File.read(error_file, encoding: 'UTF-8') if File.file?(error_file)
        raise 'Conversor não gerou geometria. Confira FreeCADCmd e sua instalação.' unless state[1].success? && File.file?(job[:output])
        raise 'Modelo ou contexto de edição mudou. Repita a importação no contexto desejado.' unless Sketchup.active_model == job[:model] && Sketchup.active_model.active_path == job[:path]
        import_json(job[:output])
      rescue StandardError => e
        @job = nil
        Sketchup.status_text = ''
        UI.messagebox("Falha na conversão: #{e.message}")
      ensure
        FileUtils.remove_entry(job[:directory]) if job && !@job && File.directory?(job[:directory])
      end
    end
  end

  # Share the same command objects between the menu and toolbar.
  def self.toolbar_command(title, icon, help, &action)
    command = UI::Command.new(title, &action)
    command.tooltip = title
    command.status_bar_text = help
    command.small_icon = File.join(__dir__, 'icons', "#{icon}_24.png")
    command.large_icon = File.join(__dir__, 'icons', "#{icon}_32.png")
    command
  end

  def self.show_about
    UI.messagebox("FreeCAD Bridge 0.5.0\nYruam Kaffer de Faria\nCopyright © 2026\nPolyForm Noncommercial 1.0.0\nUso e modificações sem fins comerciais, conforme LICENSE.txt.")
  end

  def self.register_interface
    @commands = [
      toolbar_command('Importar STEP automaticamente', 'step', 'Selecionar STEP e converter com o FreeCAD em segundo plano.') { import_step },
      toolbar_command('Importar geometria FreeCAD (.json)', 'json', 'Importar um JSON compatível já convertido.') { import_json },
      toolbar_command('Configurar FreeCADCmd', 'settings', 'Selecionar o executável FreeCADCmd.exe usado na conversão.') { configure },
      toolbar_command('Diagnóstico (0.5.0)', 'diagnostics', 'Conferir versão, caminho do executável e arquivo de configuração.') { diagnostics },
      toolbar_command('Sobre / licença', 'about', 'Autoria, versão e licença do FreeCAD Bridge.') { show_about }
    ]
    @commands.first(2).each do |command|
      command.set_validation_proc { @job ? MF_GRAYED : MF_ENABLED }
    end
    menu = UI.menu('Extensions').add_submenu('FreeCAD Bridge')
    @toolbar = UI::Toolbar.new('FreeCAD Bridge')
    @commands.each_with_index do |command, index|
      @toolbar.add_separator if index == 2
      @toolbar.add_item(command)
      menu.add_item(command)
    end
    menu.add_separator
    menu.add_item('Tratar JSON existente...') { reprocess_json }
    menu.add_item('Mostrar barra de ferramentas') { @toolbar.show }
    menu.add_item('Como importar') do
      UI.messagebox('Configure FreeCADCmd uma vez; depois use o ícone de STEP. Para arquivos já convertidos, use JSON. Arraste a barra para encaixá-la nas bordas da janela.')
    end
    if @toolbar.get_last_state == -1
      @toolbar.show
    else
      @toolbar.restore
    end
  end

  unless file_loaded?(__FILE__)
    register_interface
    file_loaded(__FILE__)
  end
end
