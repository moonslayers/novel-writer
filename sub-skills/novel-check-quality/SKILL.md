# novel-check-quality

**Versión**: 2.0
**Función**: Verificación de calidad

---

## Entrada

```yaml
chapter_content: string
chapter_number: number
framework: object
project_path: string
```

---

## Salida

```yaml
status: "success"
passed: boolean
warnings:
- type: "consistency" | "structure" | "style"
message: string
severity: "low" | "medium" | "high"
errors:
- type: string
message: string
severity: "critical"
details:
word_count: number
structure_ratio:
setup: number
climax: number
aftermath: number
```

---

## Dimensiones de verificación

| Dimensión | Elemento a verificar | Método de gestión |
|-----------|------------|-----------------|
| Consistencia | Conflictos de ambientación, personaje fuera de carácter (OOC) | Advertencia; no bloquea el proceso |
| Estructura | Proporción 60-20-20 | Error; requiere corrección |
| Estilo | Adjetivos excesivos | Advertencia; no bloquea el proceso |
| Integridad | Elementos obligatorios faltantes | Error; requiere corrección |

Los resultados de la verificación son orientativos; solo los errores estructurales críticos bloquean el proceso.
