from email.mime.text import MIMEText


def getNotifyUserTemplate(plan_name : str, plan_link : str):
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

                    .goto-button a:hover {
                        background-color: black !important;
                        color: white !important;
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
                    <p>Podczas codziennego sprawdzania planu zajęć napotkaliśmy zmiany w wybranym przez Ciebie planie.</p>
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
                        <h2 style='font-size: 1rem;margin: 0;float: left;'>Wybrany plan to:</h2> <span style='float: right;'>{plan_name}</span>
                    </div>
                    <div class="goto-button"
                        style='
                        clear: both;
                        margin-top: 2rem;
                        text-align: center;'
                    >
                        <a href='{plan_link}'
                            style='background-color: rgb(123, 186, 227);
                            color: black;
                            border: none;
                            padding: 0.5vh 1vw;
                            border-radius: 1vmax;
                            cursor: pointer !important;
                            transition-duration: .25s;
                            text-decoration: none;
                            margin-block: 2em;
                            font-size: 0.6rem;'
                        >
                            przejdź do planu
                        </a>
                    </div>
                </section>
                <footer style='
                        font-size: .75rem;
                        border-top: 1px solid white;
                        padding: 1em;'
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