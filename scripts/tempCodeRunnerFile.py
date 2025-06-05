            if especialidad_element is not None and nombre_element is not None:
                try:
                    especialidad_id = int(especialidad_element.text)
                    
                    # decodificación manual
                    nombre_raw = nombre_element.text
                    nombre = nombre_raw.encode('latin1').decode('cp1252', errors='ignore')

                    existing = EspecialidadModel.query.get(especialidad_id)
                    if existing:
                        print(f"Registro duplicado ID {especialidad_id}: {nombre}")
                        registros_duplicados += 1
                        continue

                    new_entry = EspecialidadModel(
                        id=especialidad_id,
                        especialidad=especialidad_id,
                        nombre=nombre,
                        letra=item.find('letra').text.encode('latin1').decode('cp1252', errors='ignore') if item.find('letra') is not None else None,
                        observacion=item.find('observacion').text.encode('latin1').decode('cp1252', errors='ignore') if item.find('observacion') is not None else None
                    )