set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py makemigrations

python manage.py migrate

python manage.py loaddata facultades.json

# Agregar un superusuario
#echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('Kevin_Martin', 'correo@ejemplo.com', '12345678')" | python manage.py shell

