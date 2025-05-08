# GPT_Local

Este proyecto tiene como objetivo implementar y ejecutar un modelo GPT de manera local, sin depender de servicios en la nube. Es ideal para quienes buscan mantener el control total sobre su aplicacion y personalizar el modelo según sus necesidades.

## Características

- **Ejecución híbrida**: Aunque el modelo se ejecuta localmente, utiliza la API de OpenAI para procesar las solicitudes, lo que implica que los datos se envían a los servidores de OpenAI. Solo los modelos 100% instalados en tu local que no utilizan peticiones a la API son 100% privados.
- **Privacidad relativa**: Aunque los datos no se procesan completamente en tu máquina, OpenAI asegura medidas de privacidad en el manejo de la información.
- **Personalización**: Ajusta el modelo a tus casos de uso específicos.
- **Compatibilidad**: Diseñado para trabajar en múltiples plataformas.

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`
- GPU compatible (opcional, pero recomendado para un mejor rendimiento)

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/idm-code/gpt_local.git
    cd GPT_Local
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3. Configura el entorno según tus necesidades.

## Uso

Ejecuta el modelo con el siguiente comando:

```bash
python app.py
```


## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request para sugerir mejoras.

## Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

## Contacto

Para preguntas o soporte, contacta a ivandm.code@gmail.com.