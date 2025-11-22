# 🔄 Solución a Problemas de Cuota de Gemini API

## ❌ Problema: Error 429 - Cuota Excedida

Si recibes un error como este:
```
429 You exceeded your current quota, please check your plan and billing details.
Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests
```

Esto significa que has excedido los límites del tier gratuito de Gemini API.

## 🔧 Solución Aplicada

### Cambio de Modelo

El código ahora usa **`gemini-1.5-flash`** en lugar de `gemini-2.0-flash-exp` porque:

- ✅ **Compatible con tier gratuito**: El modelo `gemini-1.5-flash` está disponible en el tier gratuito
- ✅ **Más rápido**: Es más eficiente y tiene mejor latencia
- ✅ **Mayor cuota**: El tier gratuito permite más solicitudes por minuto con este modelo

### Límites del Tier Gratuito

El tier gratuito de Gemini API tiene estos límites:

**Por minuto:**
- `gemini-1.5-flash`: Hasta 15 solicitudes/minuto
- `gemini-1.5-pro`: Hasta 2 solicitudes/minuto

**Por día:**
- Tokens de entrada: 1,500,000 tokens/día
- Tokens de salida: 32,000 tokens/día

## 📋 Qué Hacer si Excedes la Cuota

### 1. Esperar el Reset de Cuota

Las cuotas se resetean cada minuto. El error muestra cuánto tiempo esperar:
```
Please retry in 38.936137209s.
```

**Solución**: Espera el tiempo indicado antes de intentar nuevamente.

### 2. Verificar tu Uso Actual

Ve a: https://ai.dev/usage?tab=rate-limit

Aquí puedes ver:
- Cuántas solicitudes has hecho en el último minuto
- Cuántos tokens has usado
- Cuándo se resetean las cuotas

### 3. Implementar Rate Limiting en tu Aplicación

Para evitar exceder las cuotas, considera:

- **Limitar solicitudes por usuario**: Solo permitir X solicitudes por minuto por usuario
- **Cola de solicitudes**: Si hay muchas solicitudes, ponerlas en cola y procesarlas gradualmente
- **Caché**: Guardar respuestas similares para evitar solicitudes duplicadas

### 4. Actualizar a un Plan de Pago (Opcional)

Si necesitas más cuota, puedes actualizar tu plan en:
https://ai.google.dev/pricing

Los planes de pago ofrecen:
- Mayor cuota por minuto
- Mayor cuota de tokens
- Acceso a modelos más avanzados

## 🔍 Verificar el Modelo que Estás Usando

Para verificar qué modelo está usando tu aplicación, consulta el endpoint `/health`:

```bash
curl http://localhost:8000/health
```

Debería mostrar:
```json
{
  "gemini_api": {
    "connected": true,
    "message": "Conexión a Gemini API exitosa. Modelo gemini-1.5-flash disponible"
  }
}
```

## ⚠️ Modelos NO Disponibles en Tier Gratuito

Estos modelos **NO** están disponibles en el tier gratuito y causarán error 429:

- ❌ `gemini-2.0-flash-exp`
- ❌ `gemini-2.0-pro`
- ❌ `gemini-2.5-flash`
- ❌ `gemini-2.5-pro`

## ✅ Modelos Disponibles en Tier Gratuito

Estos modelos **SÍ** están disponibles en el tier gratuito:

- ✅ `gemini-1.5-flash` (usado por defecto ahora)
- ✅ `gemini-1.5-pro` (alternativa, pero más lento)
- ✅ `gemini-pro` (legacy, funciona pero no recomendado)

## 🔄 Cambiar el Modelo Manualmente

Si necesitas cambiar el modelo, edita `BlogAIBackend/gemini_service.py`:

```python
# Cambiar esta línea:
model_name = 'gemini-1.5-flash'

# Por ejemplo, a gemini-1.5-pro:
model_name = 'gemini-1.5-pro'
```

**Nota**: `gemini-1.5-pro` es más lento y tiene menor cuota en tier gratuito (2 solicitudes/minuto vs 15 de flash).

## 📚 Recursos Adicionales

- **Documentación de Rate Limits**: https://ai.google.dev/gemini-api/docs/rate-limits
- **Monitoreo de Uso**: https://ai.dev/usage?tab=rate-limit
- **Precios y Planes**: https://ai.google.dev/pricing
- **Documentación de Modelos**: https://ai.google.dev/models

## 💡 Tips

1. **Usa gemini-1.5-flash**: Es el mejor modelo para tier gratuito (rápido y alta cuota)
2. **Monitorea tu uso**: Revisa regularmente tu uso en https://ai.dev/usage
3. **Implementa rate limiting**: Limita cuántas solicitudes puede hacer cada usuario
4. **Caché respuestas**: Guarda respuestas similares para evitar solicitudes duplicadas
5. **Espera antes de reintentar**: Si excedes la cuota, espera el tiempo indicado en el error

---

**Con estos cambios, el error de cuota debería resolverse automáticamente** usando el modelo correcto compatible con tier gratuito. ✅

