from email.message import EmailMessage
from app.config import settings


def create_email(subject: str, to: str, html_content: str) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = settings.SMTP_USER
    email['To'] = to
    email.set_content(html_content, subtype='html')
    return email


def get_approval_email_template(name: str, user_email: str) -> EmailMessage:
    html = (
        '<div>'
        f'<h1>Здравствуйте, {name}</h1>'
        '<p>Мы получили Вашу заявку! В ближайшее время администратор её проверит, и Вы получите ответ.</p>'
        '</div>',
    )
    return create_email("Заявка", user_email, html)


def get_accepted_request_email_template(name: str, user_email: str, token: str) -> EmailMessage:
    html = (
        '<div>'
        f'<h1>Здравствуйте, {name}</h1>'
        '<p>Ваша заявка одобрена! Чтобы верифицировать аккаунт, перейдите по <b>ссылке</b><br>Ссылка будет доступна в течении 1 суток.</p>'
        f'<p>https://{settings.SERVER_DOMAIN}/logIn?token={token}</p>'
        '</div>',
    )
    return create_email("Заявка", user_email, html)


def get_rejected_request_email_template(name: str, user_email: str,) -> EmailMessage:
    html = (
        '<div>'
        f'<h1>Здравствуйте, {name}</h1>'
        '<p>Ваша заявка отклонена.</p>'
        '</div>',
    )
    return create_email("Заявка", user_email, html)


def get_forgot_email_template(name: str, user_email: str, token: str) -> EmailMessage:
    html = (
        '<div>'
        f'<h1>Здравствуйте, {name}</h1>'
        '<p>Чтобы сбросить пароль, перейдите по <b>ссылке</b></p>'
        f'<p>https://{settings.SERVER_DOMAIN}/reset_password?token={token}</p>'
        '</div>',
    )
    return create_email("Сброс пароля", user_email, html)


def get_admin_approval_email_template(name: str, surname: str, user_email: str) -> EmailMessage:
    html = (
    '<div>'
    '<h1>Уважаемый администратор,</h1>'
    '<p>Поступила новая заявка на регистрацию. Ниже приведены данные пользователя:</p>'
    '<table border="1" cellpadding="5" cellspacing="0">'
    '<tr>'
    '<th>Имя</th>'
    '<th>Фамилия</th>'
    '<th>Email</th>'
    '<th>Роль</th>'
    '</tr>'
    '<tr>'
    f'<td>{name}</td>'
    f'<td>{surname}</td>'
    f'<td>{user_email}</td>'
    '<td>Представитель организации</td>'
    '</tr>'
    '</table>'
    '</div>',
)
    return create_email("Новая заявка на регистрацию", settings.ADMIN_EMAIL, html)


def get_time_limit_qa_template(
    filename: str, 
    tokens: int, 
    total_time: float, 
    gigachat_time: float, 
    question: str, 
    answer: str
) -> EmailMessage:
    html = (
    '<div>'
    '<h1>Уважаемый администратор,</h1>'
    '<p>Один из запросов в вопросно-ответной системе превысил временной лимит (15 секунд)</p>'
     '<table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">'
    '<tr>'
    '<th style="text-align: left; width: 30%;">Операция</th>'
    '<th style="text-align: left;">Вопросно-ответная система</th>'
    '</tr>'
    '<tr>'
    f'<td>Документация</td>'
    f'<td>{filename}</td>'
    '</tr>'
    '<tr>'
    f'<td>Потраченные токены</td>'
    f'<td>{tokens}</td>'
    '</tr>'
    '<tr>'
    f'<td>Общее время</td>'
    f'<td>{total_time}</td>'
    '</tr>'
    '<tr>'
    f'<td>Время работы GigaChat</td>'
    f'<td>{gigachat_time}</td>'
    '</tr>'
    '<tr>'
    f'<td>Вопрос</td>'
    f'<td style="word-break: break-word;">{question}</td>'
    '</tr>'
    '<tr>'
    f'<td>Ответ</td>'
    f'<td style="word-break: break-word;">{answer.replace(chr(10), "<br>")}</td>'
    '</tr>'
    '</table>'
    '</div>',
)
    return create_email("Превышен временной лимит в вопросно-ответной системе!", settings.ADMIN_EMAIL, html)


def get_time_limit_test_template(
    filename: str, 
    tokens: int, 
    total_time: float, 
    gigachat_time: float,
    generation_attemps: int,
    question: str, 
    options: str, 
    right_answer: str
) -> EmailMessage:
    html = (
    '<div>'
    '<h1>Уважаемый администратор,</h1>'
    '<p>Один из запросов в тестовой системе превысил временной лимит (15 секунд)</p>'
     '<table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">'
    '<tr>'
    '<th style="text-align: left; width: 30%;">Операция</th>'
    '<th style="text-align: left;">Тестовая система</th>'
    '</tr>'
    '<tr>'
    f'<td>Документация</td>'
    f'<td>{filename}</td>'
    '</tr>'
    '<tr>'
    f'<td>Потраченные токены</td>'
    f'<td>{tokens}</td>'
    '</tr>'
    '<tr>'
    f'<td>Общее время</td>'
    f'<td>{total_time}</td>'
    '</tr>'
    '<tr>'
    f'<td>Время работы GigaChat</td>'
    f'<td>{gigachat_time}</td>'
    '</tr>'
    '<tr>'
    f'<td>Кол-во попыток генерации</td>'
    f'<td style="word-break: break-word;">{generation_attemps}</td>'
    '</tr>'
    '<tr>'
    f'<td>Вопрос</td>'
    f'<td style="word-break: break-word;">{question}</td>'
    '</tr>'
    '<tr>'
    f'<td>Варианты ответа</td>'
    f'<td style="word-break: break-word;">{options}</td>'
    '</tr>'
    '<tr>'
    f'<td>Правильный ответ</td>'
    f'<td style="word-break: break-word;">{right_answer}</td>'
    '</tr>'
    '</table>'
    '</div>',
)
    return create_email("Превышен временной лимит в тестовой системе!", settings.ADMIN_EMAIL, html)
