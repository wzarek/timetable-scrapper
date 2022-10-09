from array import array
from email.mime.text import MIMEText


def getUpdateReportTemplate(plan_names : array):

    notification_text = ''

    for plan in plan_names:
        notification_text += f"<div style='clear:both;'><h2 style='font-size: 1rem;margin: 0;float: left;'>Zmieniono:</h2> <span style='float: right;'>{plan}</span></div>"
    
    if not plan_names:
        notification_text = "<div><h2 style='font-size: 1rem;margin: 0;text-align:center;clear: both;'>Brak znalezionych zmian.</h2></div>"

    css_styles = """
                    a {
                        cursor: pointer !important;
                    }

                    a:hover {
                        color: rgb(80, 178, 244) !important;
                    }

                    header {
                        text-align: center;
                        border-bottom: 1px solid white;
                        padding: .5rem;
                    }

                    header h1 {
                        font-weight: 400;
                    }
    """

    html_body = f"""\
        <html>
            <head>
                <style>
                    {css_styles}
                </style>
            </head>
            <body 
                style='background-color: rgba(76, 106, 178, 1);
                color: white;
                font-family: sans-serif;
                font-weight: lighter;'
                        >
                <header>
                    <h1>Witaj!</h1>
                    <p>Oto raport z codziennego sprawdzania planów zajęć.</p>
                </header>
                <section style='padding:1em;'>
                    <div class="chosen"
                        style='
                        max-width: 400px;
                        margin: auto;
                        text-align: center;
                        height: 2rem;
                        line-height: 2rem;'
                    >
                        {notification_text}
                    </div>
                </section>
                <footer style='
                        font-size: .75rem;
                        border-top: 1px solid white;
                        padding: 1em;
                        clear: both;'
                >
                    <p style='
                        float: left;'
                    >
                        Pozdrawiam<br> Maciej Krawczyk, <a href='wzarek.me' style='color: rgb(123, 186, 227); text-decoration: none;'>wzarek.me</a>
                    </p>
                    <p
                        style='
                        text-align: right;'
                    >
                        Nie chcesz otrzymywać takich wiadomości? <br>
                        <a style='color: rgb(123, 186, 227); text-decoration: none;' href='#'>Odsubskrybuj powiadomienia</a>
                    </p>
                </footer>
            </body>
        </html>
    """

    return MIMEText(html_body, 'html')