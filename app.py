from flask import Flask, request, render_template, session
from instagrapi import Client

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None

    if request.method == 'POST':
        # Обработка основной формы
        username = request.form.get('username')
        password = request.form.get('password')
        proxy_address = request.form.get('proxy_address')
        proxy_port = request.form.get('proxy_port')
        proxy_user = request.form.get('proxy_user')
        proxy_pass = request.form.get('proxy_pass')
        post_url = request.form.get('post_url')

        if not all([username, password, proxy_address, proxy_port, proxy_user, proxy_pass, post_url]):
            message = 'Ошибка: недостаточно данных для аутентификации.'
        else:
            proxy = {
                "http": f"http://{proxy_user}:{proxy_pass}@{proxy_address}:{proxy_port}",
                "https": f"http://{proxy_user}:{proxy_pass}@{proxy_address}:{proxy_port}"
            }

            client = Client()
            client.proxy = proxy

            try:
                client.login(username, password)
                media_id = client.media_pk_from_url(post_url)
                client.media_like(media_id)
                message = 'Пост успешно лайкнут!'
            except Exception as e:
                message = f"Произошла ошибка: {e}"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
