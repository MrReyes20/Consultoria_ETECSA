#!/bin/bash

# Función para mostrar el uso del script
show_usage() {
    echo "Uso: ./db.sh [comando]"
    echo "Comandos disponibles:"
    echo "  start      - Inicia los contenedores de la base de datos"
    echo "  stop       - Detiene los contenedores de la base de datos"
    echo "  restart    - Reinicia los contenedores de la base de datos"
    echo "  status     - Muestra el estado de los contenedores"
    echo "  logs       - Muestra los logs de la base de datos"
    echo "  shell      - Abre una shell en el contenedor de PostgreSQL"
    echo "  backup     - Crea un backup de la base de datos"
    echo "  restore    - Restaura un backup de la base de datos"
}

# Verificar si Docker está corriendo
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "Error: Docker no está corriendo"
        exit 1
    fi
}

case "$1" in
    start)
        check_docker
        docker-compose -f docker-compose.dev.yml up -d
        echo "Base de datos iniciada en localhost:5432"
        echo "pgAdmin disponible en http://localhost:5050"
        ;;
    stop)
        docker-compose -f docker-compose.dev.yml down
        ;;
    restart)
        docker-compose -f docker-compose.dev.yml restart
        ;;
    status)
        docker-compose -f docker-compose.dev.yml ps
        ;;
    logs)
        docker-compose -f docker-compose.dev.yml logs -f db
        ;;
    shell)
        docker-compose -f docker-compose.dev.yml exec db psql -U postgres -d consultoria
        ;;
    backup)
        timestamp=$(date +%Y%m%d_%H%M%S)
        backup_file="backup_${timestamp}.sql"
        docker-compose -f docker-compose.dev.yml exec -T db pg_dump -U postgres -d consultoria > "backups/${backup_file}"
        echo "Backup creado: backups/${backup_file}"
        ;;
    restore)
        if [ -z "$2" ]; then
            echo "Error: Debes especificar el archivo de backup"
            echo "Uso: ./db.sh restore <archivo_backup>"
            exit 1
        fi
        if [ ! -f "$2" ]; then
            echo "Error: El archivo de backup no existe"
            exit 1
        fi
        docker-compose -f docker-compose.dev.yml exec -T db psql -U postgres -d consultoria < "$2"
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
