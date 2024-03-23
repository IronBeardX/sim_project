
# Proyecto: Simulación de Eventos Discretos

# Orientación
---

Este proyecto tiene como objetivo desarrollar una simulación de eventos discretos para analizar y entender mejor ciertos fenómenos. A través de este trabajo, buscamos aplicar los principios de la simulación de eventos discretos para modelar y experimentar con estos fenómenos, y obtener resultados que nos ayuden a tomar decisiones informadas.

El proyecto debe ser entregado en un repositorio público de GitHub. Este repositorio debe contener tanto el código fuente de tu simulación como el informe del proyecto en LaTeX. Asegúrese de que el repositorio esté bien organizado y que tanto el código como el informe sean fácilmente accesibles.

## Estructura del informe

### S1 Introducción

- Breve descripción del proyecto
- Objetivos y metas
- El sistema específico a simular y las variables de interés que cada equipo debe analizar se les hará saber por esta misma vía.
- Variables que describen el problema

### S2 Detalles de Implementación

- Pasos seguidos para la implementación

### S3 Resultados y Experimentos

- Hallazgos de la simulación
- Interpretación de los resultados
- Necesidad de realizar el análisis estadístico de la simulación (Variables de interés)
- Análisis de parada de la simulación

### S4 Modelo Matemático

- Descripción del modelo de simulación
- Supuestos y restricciones

## Sistema de eventos discretos 3: Inventario

Para satisfacer las demandas, el tendero debe mantener una cantidad del producto a mano, y siempre que el inventario a mano se vuelve bajo, se ordenan unidades adicionales al distribuidor. El tendero utiliza una política de pedido llamada (s, S); es decir, siempre que el inventario a mano es menor que s y no hay un pedido pendiente, entonces se ordena una cantidad para llevarlo hasta S, donde $s<S$. Es decir, si el nivel de inventario actual es x y no hay un pedido pendiente, entonces si $x<s$ se ordena la cantidad S−x.
El costo de pedir y unidades del producto es una función especificada c(y), y toma L unidades de tiempo hasta que se entrega el pedido, con el pago realizado a la entrega. Además, la tienda paga un costo de mantenimiento de inventario de h por unidad de artículo por unidad de tiempo.
Supongamos además que siempre que un cliente demanda más del producto de lo que está disponible actualmente, entonces se vende la cantidad a mano y el resto del pedido se pierde para la tienda.

# Solución
---