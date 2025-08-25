#!/bin/bash

# Función para mostrar el uso del script
show_usage() {
    echo "Uso: ./dev.sh [comando]"
    echo "Comandos disponibles:"
    echo "  start       - Inicia todos los servicios"
    echo "  stop        - Detiene todos los servicios"
    echo "  restart     - Reinicia todos los servicios"
    echo "  logs        - Muestra los logs de todos los servicios"
    echo "  web-logs    - Muestra los logs del servidor web"
    echo "  db-logs     - Muestra los logs de la base de datos"
    echo "  shell       - Abre una shell en el contenedor web"
    echo "  dbshell     - Abre una shell de PostgreSQL"
    echo "  makemigrations - Crea nuevas migraciones"
    echo "  migrate     - Aplica las migraciones"
    echo "  test        - Ejecuta las pruebas"
    echo "  createsuperuser - Crea un superusuario"
}

case "$1" in
    start)
        docker-compose -f docker-compose.yml up -d
        ;;
    stop)
        docker-compose -f docker-compose.yml down
        ;;
    restart)
        docker-compose -f docker-compose.yml restart
        ;;
    logs)
        docker-compose -f docker-compose.yml logs -f
        ;;
    web-logs)
        docker-compose -f docker-compose.yml logs -f web
        ;;
    db-logs)
        docker-compose -f docker-compose.yml logs -f db
        ;;
    shell)
        docker-compose -f docker-compose.yml exec web bash
        ;;
    dbshell)
        docker-compose -f docker-compose.yml exec db psql -U postgres -d consultoria
        ;;
    makemigrations)
        docker-compose -f docker-compose.yml exec web python manage.py makemigrations
        ;;
    migrate)
        docker-compose -f docker-compose.yml exec web python manage.py migrate
        ;;
    test)
        docker-compose -f docker-compose.yml exec web python manage.py test
        ;;
    createsuperuser)
        docker-compose -f docker-compose.yml exec web python manage.py createsuperuser
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
