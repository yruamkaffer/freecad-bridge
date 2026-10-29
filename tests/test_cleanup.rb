# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Behavioral regression of the actual cleanup methods using small API doubles.
# No geometry kernel or SketchUp UI is simulated.
def file_loaded?(_path)
  true
end
module Sketchup
  class Edge
    attr_accessor :soft, :smooth
    attr_reader :faces, :erased
    def initialize(faces, &on_erase)
      @faces = faces
      @on_erase = on_erase
      @soft = @smooth = @erased = false
    end
    def valid?; !@erased; end
    def erase!
      @erased = true
      @on_erase.call if @on_erase
    end
  end
end
require_relative '../yk_step_bridge/main'
Normal = Struct.new(:angle) do
  def dot(other); Math.cos((angle - other.angle) * Math::PI / 180.0); end
end
Point = Struct.new(:distance) do
  def distance_to_plane(_plane); distance; end
end
Vertex = Struct.new(:position)
Face = Struct.new(:normal, :material, :vertices, :plane)
Group = Struct.new(:entities, :closed, :name) do
  def manifold?; closed; end
end
def face(angle, material = :white)
  Face.new(Normal.new(angle), material, [Vertex.new(Point.new(0.0))], :plane)
end
def assert(condition, message)
  raise message unless condition
end

def test_restored_mesh_receives_smoothing
  group = Group.new([], true, 'Restored solid')
  erased = Sketchup::Edge.new([face(0), face(0)]) { group.closed = false }
  group.entities << erased
  restored = Sketchup::Edge.new([face(0), face(10)])
  reports = []
  restored_materials = false
  YKStepBridge.clean_and_smooth(group, reports) do
    group.entities.replace([restored])
    group.closed = true
    restored_materials = true
  end
  assert(erased.erased, 'Fixture must trigger topology cleanup')
  assert(restored_materials, 'Restoration block must repaint')
  assert(group.manifold?, 'Restored solid must remain closed')
  assert(restored.soft && restored.smooth, 'Regression: restored edges lost smoothing')
  assert(reports.join.include?('suavização reaplicada'), 'Report must identify smoothing after restoration')
end

def test_successful_cleanup_keeps_smoothing
  planar = Sketchup::Edge.new([face(0), face(0)])
  curved = Sketchup::Edge.new([face(0), face(10)])
  group = Group.new([planar, curved], true, 'Closed solid')
  reports = []
  YKStepBridge.clean_and_smooth(group, reports) { raise 'Unexpected restoration' }
  assert(planar.erased, 'Coplanar cleanup must still run')
  assert(curved.soft && curved.smooth, 'Successful cleanup must smooth remaining curved edges')
  assert(reports.empty?, 'No restoration warning expected')
end

def test_sharp_open_and_material_boundaries
  sharp = Sketchup::Edge.new([face(0), face(45)])
  boundary = Sketchup::Edge.new([face(0)])
  nonmanifold = Sketchup::Edge.new([face(0), face(5), face(10)])
  colors = Sketchup::Edge.new([face(0, :red), face(0, :blue)])
  group = Group.new([sharp, boundary, nonmanifold, colors], false, 'Open mesh')
  YKStepBridge.clean_and_smooth(group, []) { raise 'Originally open mesh must not restore' }
  [sharp, boundary, nonmanifold].each do |e|
    assert(!e.erased && !e.soft && !e.smooth, 'Sharp/open/nonmanifold edges must stay unchanged')
  end
  assert(!colors.erased, 'Material boundary must not be erased')
  assert(colors.faces.map(&:material) == [:red, :blue], 'Materials must remain intact')
end

def test_invalid_restoration_stops_import
  group = Group.new([], true, 'Broken restore')
  group.entities << Sketchup::Edge.new([face(0), face(0)]) { group.closed = false }
  begin
    YKStepBridge.clean_and_smooth(group, []) { group.entities.clear }
  rescue RuntimeError => error
    assert(error.message.include?('restaurar o fechamento'), 'Expected restoration error')
    return
  end
  raise 'Failed restoration must raise before import continues'
end

def test_closed_surface_is_not_reported_as_cad_solid
  component = Group.new([], true, 'Closed shell')
  status = YKStepBridge.part_status(component, {'geometry_type' => 'surface'})
  assert(status.include?('SUPERFÍCIE'), 'Closed shell must stay classified as surface')
end

def test_invalid_cad_is_not_reported_as_approved_solid
  component = Group.new([], true, 'Unapproved CAD')
  assert(YKStepBridge.part_status(component, {'cad_valid' => false}) == 'VERIFICAR', 'Invalid CAD must be flagged')
end

def test_approved_solid_status
  component = Group.new([], true, 'Approved solid')
  assert(YKStepBridge.part_status(component, {'cad_valid' => true, 'mesh_closed' => true}) == 'SÓLIDO', 'Approved solid status')
end

tests = private_methods.grep(/^test_/).sort
tests.each do |test|
  send(test)
  puts "PASS #{test}"
end
raise 'No tests executed' unless tests.size == 7
puts "#{tests.size} cleanup regression tests passed (API doubles, not SketchUp)."
