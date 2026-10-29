# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Inventory preserves surfaces outside solids rather than silently dropping them."""
def inventory(shape):
    solids=list(shape.Solids);shells=list(shape.Shells);items=[('solid',s) for s in solids]
    owned_shells=[shell for solid in solids for shell in solid.Shells]
    for shell in shells:
        if not any(shell.isSame(owned) for owned in owned_shells):items.append(('surface',shell))
    owned_faces=[face for shell in shells for face in shell.Faces]
    owned_faces += [face for solid in solids for face in solid.Faces]
    for face in shape.Faces:
        if not any(face.isSame(owned) for owned in owned_faces):items.append(('surface',face))
    return items
